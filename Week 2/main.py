import os
import json
import csv
import re
import argparse
from datetime import datetime
import asyncio
from rich.console import Console
from src.config import MAX_CONCURRENT_REQUESTS
from src.prompt_builder import build_extraction_prompt
from src.bedrock_client import extract_data_with_bedrock
from src.rate_limiter import process_with_retry
from src.parser import parse_and_validate

console = Console()

async def process_text(semaphore: asyncio.Semaphore, user_text: str):
    """
    The full pipeline for a single piece of text:
    1. Build prompt
    2. Send to model (with rate limits)
    3. Parse & Validate
    """
    prompt = build_extraction_prompt(user_text)
    
    # We pass the semaphore to our rate limiter
    raw_response = await process_with_retry(
        semaphore, 
        extract_data_with_bedrock, 
        prompt
    )
    
    # Parse and validate the JSON using Pydantic
    validated_record = parse_and_validate(raw_response)
    return validated_record

def save_to_history(user_input: str, extracted_data, filepath: str = os.path.join("output", "results.json")):
    """
    Appends the input and extracted JSON output to a history file.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    history = []
    
    # Read existing history if the file exists
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            # If the file is empty or corrupted, start fresh
            pass
            
    # Create the new record
    new_record = {
        "timestamp": datetime.now().isoformat(),
        "input_text": user_input,
        "extracted_output": extracted_data.model_dump()
    }
    
    history.append(new_record)
    
    # Write back to the file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

async def run_batch(conversations, output_path):
    if not conversations:
        console.print("[red]No valid records found. Exiting.[/red]")
        return
        
    console.print(f"\n[yellow]Processing {len(conversations)} records concurrently...[/yellow]")
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    tasks = [process_text(semaphore, text) for text in conversations]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    success_count = 0
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            console.print(f"[bold red]Record {i+1} Failed:[/bold red] {result}")
            log_failed_record(conversations[i], str(result))
        else:
            save_to_history(conversations[i], result, filepath=output_path)
            success_count += 1
            
    console.print(f"\n[bold green]Finished processing! {success_count}/{len(tasks)} successful.[/bold green]")
    console.print(f"[dim]Successful records appended to {output_path}[/dim]")
    if success_count < len(tasks):
        console.print("[dim]Failed records logged to output/failed_records.json[/dim]")

def log_failed_record(user_input: str, error_message: str, filepath: str = os.path.join("output", "failed_records.json")):
    """
    Logs failed extraction attempts to a JSON file for later review.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    history = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            pass
            
    new_record = {
        "timestamp": datetime.now().isoformat(),
        "input_text": user_input,
        "error": error_message
    }
    
    history.append(new_record)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

async def main():
    parser = argparse.ArgumentParser(description="Automated Data Extractor & JSON Parser")
    parser.add_argument("-i", "--input", type=str, help="Path to input text file")
    parser.add_argument("-o", "--output", type=str, help="Path to output JSON file")
    args = parser.parse_args()

    console.print("[bold cyan]Automated Data Extractor & JSON Parser[/bold cyan]")
    
    if args.input:
        if not os.path.exists(args.input):
            console.print(f"[red]Error: Input file '{args.input}' not found.[/red]")
            return
            
        output_path = args.output if args.output else os.path.join("output", "results.json")
        
        # Batch processing for CSV files
        if args.input.endswith('.csv'):
            conversations = []
            with open(args.input, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0].strip():
                        conversations.append(row[0].strip())
            console.print(f"[dim]Read {len(conversations)} conversations from CSV {args.input}[/dim]")
            await run_batch(conversations, output_path)
            return
            
        # Standard text file handling
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                user_input = f.read().strip()
                
            # Batch processing for large TXT files separated by '=== RECORD'
            if "=== RECORD" in user_input:
                raw_records = re.split(r'===\s*RECORD\s*\d+\s*===', user_input)
                conversations = [r.strip() for r in raw_records if r.strip()]
                console.print(f"[dim]Read {len(conversations)} distinct records from TXT {args.input}[/dim]")
                await run_batch(conversations, output_path)
                return
                
            console.print(f"[dim]Read single input from {args.input}[/dim]")
    else:
        console.print("Paste customer conversation or log below (Type 'END' on a new line and press Enter to submit):")
        # Read multiline input from user
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        user_input = "\n".join(lines).strip()
    
    if not user_input:
        console.print("[red]No input provided. Exiting.[/red]")
        return
        
    output_path = args.output if args.output else os.path.join("output", "results.json")
        
    console.print("\n[yellow]Processing single record...[/yellow]")
    
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    try:
        result = await process_text(semaphore, user_input)
        
        console.print("\n[bold green]Validated JSON Output:[/bold green]")
        console.print(result.model_dump_json(indent=2))
        
        save_to_history(user_input, result, filepath=output_path)
        console.print(f"\n[dim]Record successfully saved to {output_path}[/dim]")
        
    except Exception as e:
        console.print(f"\n[bold red]Pipeline Error:[/bold red] {e}")
        log_failed_record(user_input, str(e))
        console.print("[dim]Error logged to output/failed_records.json[/dim]")

if __name__ == "__main__":
    asyncio.run(main())