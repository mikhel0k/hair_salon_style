from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.models import Cell
from app.schemas.Cell import CellCreate


async def create_cell(
        cell_data: CellCreate,
        session: AsyncSession,
) -> Cell:
    cell = Cell(**cell_data.model_dump())
    session.add(cell)
    await session.flush()
    await session.refresh(cell)
    return cell


async def create_cells(
        sells_list: list[CellCreate],
        session: AsyncSession
):
    for cell_data in sells_list:
        cell = Cell(**cell_data.model_dump())
        session.add(cell)
    await session.flush()


async def read_cell(
        cell_id: int,
        session: AsyncSession
) -> Cell | None:
    cell = await session.get(Cell, cell_id)
    return cell


async def read_cells(
        cells_id: list[int],
        session: AsyncSession
):
    stmt = select(Cell).where(Cell.id.in_(cells_id))
    cells = await session.execute(stmt)
    return cells.scalars().all()


async def read_free_cells_by_master_id_and_date(
        master_id: int,
        cell_date: date,
        session: AsyncSession
):
    stmt = select(Cell).order_by(Cell.time).where(Cell.date == cell_date,
                              Cell.master_id == master_id,
                              Cell.status == 'free')
    cells = await session.execute(stmt)
    return cells.scalars().all()


async def read_cells_by_master_id_and_date(
        master_id: int,
        cell_date: date,
        session: AsyncSession
):
    stmt = select(Cell).order_by(Cell.time).where(Cell.date == cell_date,
                              Cell.master_id == master_id,)
    cells = await session.execute(stmt)
    return cells.scalars().all()


async def read_cells_by_master_id(
        master_id: int,
        session: AsyncSession
):
    stmt = select(Cell).order_by(Cell.date, Cell.time).where(
        Cell.master_id == master_id,
    )
    cells = await session.execute(stmt)
    return cells.scalars().all()


async def update_cell(
        cell: Cell,
        session: AsyncSession
):
    session.add(cell)
    await session.flush()
    await session.refresh(cell)
    return cell


async def update_cells(
        cells: list[Cell],
        session: AsyncSession
):
    for cell in cells:
        session.add(cell)
    await session.flush()
