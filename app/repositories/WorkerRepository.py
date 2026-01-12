from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Master
from app.models.Worker import Worker


async def create_worker(
        worker: Worker,
        session: AsyncSession,
):
    session.add(worker)
    await session.commit()
    await session.refresh(worker)
    return worker


async def get_worker(
        worker_id: int,
        session: AsyncSession
):
    worker = await session.get(Worker, worker_id)
    return worker


async def update_worker(
        worker: Worker,
        session: AsyncSession,
):
    session.add(worker)
    await session.commit()
    await session.refresh(worker)
    return worker


async def get_worker_full(
        worker_id: int,
        session: AsyncSession
):
    stmt = select(Worker).options(joinedload(Worker.master)).where(Worker.id == worker_id)
    worker = await session.execute(stmt)
    return worker.scalar_one_or_none()
