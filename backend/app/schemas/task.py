from typing import Optional
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="クリーニング")
    description: Optional[str] = Field(None, example="詳細")

class Task(TaskBase):
    # class TaskBase(BaseModel):
    # title: Optional[str] = Field(None, example="クリーニング")
    # description: Optional[str] = Field(None, example="詳細")
    id: str
    isFinished: bool = Field(False, description="完了フラグ")