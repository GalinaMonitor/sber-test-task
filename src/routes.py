from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from pydantic import AnyHttpUrl

from src.dependencies import parse_timestamp_query_params
from src.schemas import DatetimeQueryParams, LinkView, ResponseDomains, ResponseStatus
from src.services import DomainService, LinkViewService

router = APIRouter()


@router.post("/visited_links")
async def add_links(
    links: List[AnyHttpUrl],
    domain_service: DomainService = Depends(),
    link_view_service: LinkViewService = Depends(),
) -> ResponseStatus:
    received_at = datetime.now()
    link_schemas_list = []
    for link in links:
        domain = await domain_service.retrieve_or_create(link.host)
        link_schemas_list.append(
            LinkView(link=str(link), domain_id=domain.id, viewed_at=received_at)
        )
    await link_view_service.insert(link_schemas_list)
    return ResponseStatus(status="ok")


@router.get("/visited_domains")
async def list_domains(
    dp: DatetimeQueryParams = Depends(parse_timestamp_query_params),
    domain_service: DomainService = Depends(),
) -> ResponseDomains:
    return ResponseDomains(domains=await domain_service.list(dp), status="ok")
