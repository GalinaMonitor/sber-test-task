from datetime import datetime
from typing import List

from fastapi import APIRouter
from pydantic import AnyHttpUrl
from starlette.requests import Request

from services import DomainService, LinkViewService
from schemas import LinkView
from utils import parse_timestamp_query_params

router = APIRouter()


@router.post("/visited_links")
async def add_links(links: List[AnyHttpUrl]):
    received_at = datetime.utcnow()
    link_schemas_list = []
    for link in links:
        domain = await DomainService().retrieve_or_create(link.host)
        link_schemas_list.append(LinkView(link=str(link), domain_id=domain.id, viewed_at=received_at))
    await LinkViewService().insert(link_schemas_list)
    return {"status": "ok"}


@router.get("/visited_domains")
async def list_domains(request: Request):
    dp = parse_timestamp_query_params(request.query_params)
    return {"domains": await DomainService().list(dp), "status": "ok"}
