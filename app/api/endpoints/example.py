from fastapi import APIRouter

from app.api.models.example import ExampleModel

router = APIRouter()


@router.get("/example/{item_id}", response_model=ExampleModel)
async def read_example(item_id: int):
    return {"item_id": item_id, "name": "Example Item"}
