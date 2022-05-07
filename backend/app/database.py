from fastapi import HTTPException
from typing import Union
import motor.motor_asyncio
from bson import ObjectId

MONGO_URI = 'mongodb://root:example@mongo:27017/'

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.yaruzou_db
collection_task = database.task
collection_user = database.user


def task_serializer(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "isFinished": False
    }

async def db_create_task(data: dict) -> Union[dict, bool]:
    task = await collection_task.insert_one(data)
    new_task = await collection_task.find_one({"_id": task.inserted_id})
    if new_task:
        return task_serializer(new_task)
    return False

async def db_get_tasks() -> list:
    tasks = []
    for task in await collection_task.find().to_list(length=100):
        tasks.append(task_serializer(task))
    return tasks


async def db_get_single_task(id: str) -> Union[dict, bool]:
    task = await collection_task.find_one({"_id": ObjectId(id)})
    if task:
        return task_serializer(task)
    return False


async def db_update_task(id: str, data: dict) -> Union[dict, bool]:
    task = await collection_task.find_one({"_id": ObjectId(id)})
    if task:
        updated_task = await collection_task.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if (updated_task.modified_count > 0):
            new_task = await collection_task.find_one({"_id": ObjectId(id)})
            return task_serializer(new_task)
    return False


async def db_delete_task(id: str) -> bool:
    task = await collection_task.find_one({"_id": ObjectId(id)})
    if task:
        deleted_task = await collection_task.delete_one({"_id": ObjectId(id)})
        if (deleted_task.deleted_count > 0):
            return True
    return False

async def db_create_user(data: dict):
    overlap_user = await collection_user.find_one({"email": data.get("email")})
    if overlap_user:
        raise HTTPException(status_code=400, detail='Email is already taken')
    user = await collection_user.insert_one(data)
    new_user = await collection_user.find_one({"_id": user.inserted_id})
    if not new_user:
        raise HTTPException(status_code=400, detail='Create User Failed')
    return True

async def db_get_user(email: str) -> dict:
    user = await collection_user.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail='User Not Found')
    return user
