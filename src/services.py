from typing import List

from sqlalchemy import insert, select

import models
import schemas
from db import async_session
from schemas import DatetimeQueryParams


class DomainService:
    model = models.Domain
    schema = schemas.Domain

    async def retrieve_or_create(self, domain: str) -> schemas.Domain:
        async with async_session() as session:
            statement = select(self.model).where(self.model.name == domain)
            results = await session.execute(statement)
            result = results.scalar_one_or_none()
            if not result:
                new_model = self.model(name=domain)
                session.add(new_model)
                await session.commit()
                await session.refresh(new_model)
                result = new_model
            return schemas.Domain.model_validate(result)

    async def list(self, dp: DatetimeQueryParams) -> List[str]:
        async with async_session() as session:
            statement = select(self.model.name.distinct()).join(
                models.LinkView, self.model.id == models.LinkView.domain_id
            )
            if dp.from_timestamp:
                statement = statement.where(
                    models.LinkView.viewed_at >= dp.from_timestamp
                )
            if dp.to_timestamp:
                statement = statement.where(
                    models.LinkView.viewed_at <= dp.to_timestamp
                )
            results = await session.execute(statement)
            return results.scalars().all()


class LinkViewService:
    model = models.LinkView
    schema = schemas.LinkView

    async def insert(self, links: List[schemas.LinkView]):
        async with async_session() as session:
            statement = insert(self.model)
            await session.execute(statement, [link.model_dump() for link in links])
            await session.commit()
