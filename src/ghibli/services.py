from enum import Enum
from dataclasses import dataclass

import httpx


class Role(Enum):
    FILMS = "films"
    PEOPLE = "people"
    LOCATIONS = "locations"
    SPECIES = "species"
    VEHICLES = "vehicles"


@dataclass
class GhibliParams:
    endpoint: Role | str
    limit: int | None = None
    fields: list[str] | None = None
    uuid: str | None = None


class GhibliService:
    BASE_URL = "https://ghibliapi.vercel.app"

    @staticmethod
    async def _fetch_data(params: GhibliParams):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{GhibliService.BASE_URL}/{params.endpoint.value}"
                if params.uuid:
                    url = f"{url}/{params.uuid}"
                query_params = {}
                if params.limit:
                    query_params["limit"] = params.limit
                if params.fields:
                    query_params["fields"] = ",".join(params.fields)
                response = await client.get(url, params=query_params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"}
            except httpx.RequestError as e:
                return {"error": f"Request error occurred: {e}"}

    @staticmethod
    async def get_films(params: GhibliParams):
        return await GhibliService._fetch_data(params)

    @staticmethod
    async def get_people(params: GhibliParams):
        return await GhibliService._fetch_data(params)

    @staticmethod
    async def get_locations(params: GhibliParams):
        return await GhibliService._fetch_data(params)

    @staticmethod
    async def get_species(params: GhibliParams):
        return await GhibliService._fetch_data(params)

    @staticmethod
    async def get_vehicles(params: GhibliParams):
        return await GhibliService._fetch_data(params)


class GhibliProvider:
    def __init__(self, ghibli_params: GhibliParams):
        self.service = GhibliService()
        self.params = ghibli_params

    async def get_data_by_role(self):
        role = Role(self.params.endpoint)
        if role == Role.FILMS:
            return await self.service.get_films(self.params)
        if role == Role.PEOPLE:
            return await self.service.get_people(self.params)
        if role == Role.LOCATIONS:
            return await self.service.get_locations(self.params)
        if role == Role.SPECIES:
            return await self.service.get_species(self.params)
        if role == Role.VEHICLES:
            return await self.service.get_vehicles(self.params)
        return {"error": "Role not found"}


def get_ghibli_provider(params: GhibliParams) -> GhibliProvider:
    return GhibliProvider(params)
