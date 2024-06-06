from typing import Annotated, Union
from fastapi import APIRouter, Security, Query
from src.dependencies import get_current_user
from src.users.schemas import User, Role
from pydantic import UUID4
from .services import get_ghibli_provider, GhibliParams, Role

ghibli_router = APIRouter()


@ghibli_router.get("/")
async def read_ghibli(
        limit: Annotated[int, Query(..., description="Limit of items to return")] = 10,
        fields: Annotated[Union[list[str]], Query()] = None,
        current_user: User = Security(get_current_user)
):
    params = GhibliParams(
        endpoint=Role(current_user.role.name),
        limit=limit,
        fields=fields
    )
    ghibli_provider = get_ghibli_provider(params)
    data = await ghibli_provider.get_data_by_role()
    return data


@ghibli_router.get("/{ghibli_id}")
async def read_ghibli_by_id(ghibli_id: UUID4, fields: Annotated[Union[list[str]], Query()] = None,
                            current_user: User = Security(get_current_user)):
    params = GhibliParams(
        endpoint=Role(current_user.role.name),
        fields=fields,
        uuid=ghibli_id
    )
    ghibli_provider = get_ghibli_provider(params)
    data = await ghibli_provider.get_data_by_role()
    return data
