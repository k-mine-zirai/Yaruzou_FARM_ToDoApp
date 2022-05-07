# Base Import
from http.client import HTTPException
from typing import List
from fastapi import APIRouter, Response, Request
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED
# Schema Class Import
from app.schemas.common import SuccesMsg
import app.schemas.task as task_schema
# Database Function Import
from app.database import db_create_task, db_get_tasks, db_get_single_task, db_update_task, db_delete_task

router = APIRouter()

# Task情報取得
@router.get("/task", response_model=List[task_schema.Task])
async def get_tasks():
    res = await db_get_tasks()
    return res

@router.get("/task/{task_id}", response_model=task_schema.Task)
async def get_single_task(task_id: str):
    res = await db_get_single_task(task_id)
    if res:
        return res
    raise HTTPException(
        status_code = 404, detail = f"Task of ID:{task_id} doesn't exist"
    )

# Task作成
@router.post("/task", response_model=task_schema.Task)
async def create_task( request: Request, response: Response, data: task_schema.TaskBase ):
    task = jsonable_encoder(data)
    res = await db_create_task(task)
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    raise HTTPException(
        status_code = 404, detail="Create task failed"
    )

# Task更新
@router.put("/task/{task_id}", response_model=task_schema.Task)
async def update_task( task_id: str, data: task_schema.TaskBase ):
    task = jsonable_encoder(data)
    res = await db_update_task(task_id, task)
    if res:
        return res
    raise HTTPException(
        status_code = 404, detail="Update task failed"
    )

# Task削除
@router.delete("/task/{task_id}", response_model=SuccesMsg)
async def delete_task( task_id: str ):
    res = await db_delete_task(task_id)
    if res:
        return {"message": "Successfully Deleted"}
    raise HTTPException(
        status_code = 404, detail="Delete task failed"
    )


# @router.put("/tasks/{task_id}/done", response_model=None)
# async def mark_task_as_done( task_id: int ):
#     return

# @router.delete("/tasks/{task_id}/done", response_model=None)
# async def unmark_task_as_done( task_id: int ):
#     return