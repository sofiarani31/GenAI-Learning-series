import streamlit as st
import asyncio
import json
import csv
import re
import io

from src.config import MAX_CONCURRENT_REQUESTS
from src.rate_limiter import process_with_retry
from src.bedrock_client import extract_data_with_bedrock
from src.parser import parse_and_validate
from src.prompt_builder import build_extraction_prompt
from main import save_to_history, log_failed_record

# Ensure asyncio works nicely within Streamlit threads
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

async def process_text(semaphore, text):
    prompt = build_extraction_prompt(text)
    raw = await process_with_retry(semaphore, extract_data_with_bedrock, prompt)
    return parse_and_validate(raw)
st.set_page_config(
    page_title="Enterprise Data Extractor",

)

st.title("Enterprise Data Extractor")
st.write("Extract structured JSON data from messy customer conversations.")

tab1, tab2 = st.tabs(["📝 Paste Text", "📂 Upload File"])

with tab1:
    user_input = st.text_area("Paste a single customer conversation here:", height=200)
    
    if st.button("Process Text", type="primary"):
        if user_input.strip():
            with st.spinner("Processing with AWS Bedrock..."):
                try:
                    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
                    result = loop.run_until_complete(process_text(semaphore, user_input))
                    
                    st.success("Extraction Complete!")
                    st.json(result.model_dump())
                    save_to_history(user_input, result, filepath="output/results.json")
                except Exception as e:
                    st.error(f"Error processing record: {e}")
                    log_failed_record(user_input, str(e), filepath="output/failed_records.json")
        else:
            st.error("Please paste some text first.")

with tab2:
    uploaded_files = st.file_uploader("Upload .txt or .csv files", type=['txt', 'csv'], accept_multiple_files=True)
    
    if st.button("Process Batch Files", type="primary") and uploaded_files:
        with st.spinner("Processing multiple records concurrently..."):
            
            conversations = []
            
            for uploaded_file in uploaded_files:
                string_data = uploaded_file.getvalue().decode("utf-8")
                
                if uploaded_file.name.endswith('.csv'):
                    reader = csv.reader(io.StringIO(string_data))
                    for row in reader:
                        if row and row[0].strip():
                            conversations.append(row[0].strip())
                elif "=== RECORD" in string_data:
                    raw_records = re.split(r'===\s*RECORD\s*\d+\s*===', string_data)
                    conversations.extend([r.strip() for r in raw_records if r.strip()])
                else:
                    st.warning(f"File '{uploaded_file.name}' must contain '=== RECORD X ===' markers. Skipping this file.")
                
            if not conversations: 
                st.error("No valid records found in the uploaded files.")
                st.stop()
            
            st.info(f"Found {len(conversations)} records across {len(uploaded_files)} file(s). Sending to AWS Bedrock...")
            
            semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
            tasks = [process_text(semaphore, text) for text in conversations]
            
            # Execute concurrently
            results = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            
            final_json_list = []
            failed_count = 0
            
            for i, res in enumerate(results):
                if isinstance(res, Exception):
                    failed_count += 1
                    log_failed_record(conversations[i], str(res), filepath="output/failed_records.json")
                else:
                    final_json_list.append(res.model_dump())
                    save_to_history(conversations[i], res, filepath="output/results.json")
            
            if failed_count > 0:
                st.warning(f"Processed {len(final_json_list)} records successfully, but {failed_count} failed.")
            else:
                st.success(f"Successfully processed all {len(final_json_list)} records!")
            
            if final_json_list:
                json_string = json.dumps(final_json_list, indent=2)
                st.download_button(
                    label="⬇️ Download Extracted JSON",
                    file_name="extracted_results.json",
                    mime="application/json",
                    data=json_string
                )

                st.subheader("Extracted Records Preview")
                table_data = []
                for record in final_json_list:
                    # Flatten the action items into a readable string
                    action_items = record.get("action_items", [])
                    action_str = "; ".join([f"{item.get('task', '')} ({item.get('owner', '')})" for item in action_items]) if action_items else "None"
                    
                    table_data.append({
                        "Customer Name": record.get("customer_name", ""),
                        "Issue Type": record.get("issue_type", ""),
                        "Priority": record.get("priority", ""),
                        "Sentiment": record.get("sentiment", ""),
                        "Summary": record.get("summary", ""),
                        "Action Items": action_str
                    })
                
                # Render the table
                st.dataframe(table_data, use_container_width=True)