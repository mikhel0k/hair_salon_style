from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger(__name__)
from app.models.Worker import Worker


async def create_worker(
        worker: Worker,
        session: AsyncSession,
):
    session.add(worker)
    await session.flush()
    await session.refresh(worker)
    logger.info("Worker created: id=%s, username=%s", worker.id, worker.username)
    return worker


async def get_worker(
        worker_id: int,
        session: AsyncSession
):
    worker = await session.get(Worker, worker_id)
    logger.debug("Worker read: id=%s, username=%s", worker.id, worker.username)
    return worker


async def get_worker_by_username(
        username: str,
        session: AsyncSession
):
    stmt = select(Worker).where(Worker.username == username)
    worker = await session.execute(stmt)
    logger.debug("Worker read: id=%s, username=%s", worker.id, worker.username)
    return worker.scalar_one_or_none()


async def get_worker_full(
        worker_id: int,
        session: AsyncSession
):
    stmt = select(Worker).options(joinedload(Worker.master)).where(Worker.id == worker_id)
    worker = await session.execute(stmt)
    logger.debug("Worker read: id=%s, username=%s", worker.id, worker.username)
    return worker.scalar_one_or_none()


async def update_worker(
        worker: Worker,
        session: AsyncSession,
):
    session.add(worker)
    await session.flush()
    await session.refresh(worker)
    logger.info("Worker updated: id=%s, username=%s", worker.id, worker.username)
    return worker
