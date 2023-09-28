from typing import List

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

import src.models as models
import src.schemas as schemas
from src.db import get_session
from src.schemas import DatetimeQueryParams


class DomainService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.model = models.Domain
        self.schema = schemas.Domain
        self.session = session

    async def retrieve_or_create(self, domain: str) -> schemas.Domain:
        statement = select(self.model).where(self.model.name == domain)
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            new_model = self.model(name=domain)
            self.session.add(new_model)
            await self.session.commit()
            await self.session.refresh(new_model)
            result = new_model
        return schemas.Domain.model_validate(result)

    async def list(self, dp: DatetimeQueryParams) -> List[str]:
        statement = (
            select(self.model.name.distinct())
            .join(models.LinkView, self.model.id == models.LinkView.domain_id)
            .order_by(self.model.name)
        )
        if dp.from_timestamp:
            statement = statement.where(models.LinkView.viewed_at >= dp.from_timestamp)
        if dp.to_timestamp:
            statement = statement.where(models.LinkView.viewed_at <= dp.to_timestamp)
        results = await self.session.execute(statement)
        return results.scalars().all()


class LinkViewService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.model = models.LinkView
        self.schema = schemas.LinkView
        self.session = session

    async def insert(self, links: List[schemas.LinkView]):
        statement = insert(self.model)
        await self.session.execute(statement, [link.model_dump() for link in links])
        await self.session.commit()
