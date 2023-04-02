from celery import group
from fastapi import APIRouter
from starlette.responses import JSONResponse

from api import universities
from celery_tasks.tasks import get_all_universities_task, get_university_task
from config.celery_utils import get_task_info
from schemas.schemas import Country

router = APIRouter(prefix='/universities', tags=['University'], responses={404: {"description": "Not found"}})

@router.post("/")
def get_universities(country: Country) -> dict:
    data: dict = {}
    for cnt in country.countries:
        data.update(universities.get_all_universities_for_country(cnt))
    return data

@router.post("/async")
async def get_universities_async(country: Country):
    task = get_all_universities_task.apply_async(args=[country.countries])
    return JSONResponse({"task_id": task.id})

@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    return get_task_info(task_id)


