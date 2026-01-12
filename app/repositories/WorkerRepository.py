from sqlalchemy.ext.asyncio import AsyncSession

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
