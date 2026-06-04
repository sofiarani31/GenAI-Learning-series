from pydantic import BaseModel


class ActionItem(BaseModel):
    task: str
    owner: str
    deadline: str


class ExtractedRecord(BaseModel):
    customer_name: str | None
    issue_type: str
    priority: str
    summary: str
    sentiment: str
    action_items: list[ActionItem]