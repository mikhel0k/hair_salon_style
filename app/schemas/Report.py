from datetime import date, time
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict, StrictInt


class MasterReportRow(BaseModel):
    """Одна строка выгрузки: запись с датой/временем из ячейки, услуга, клиент, статус."""

    record_id: Annotated[int, Field(..., ge=1, description="ID записи")]
    date: Annotated[date, Field(..., description="Дата приёма")]
    time: Annotated[time, Field(..., description="Время начала")]
    service_name: Annotated[str, Field(..., description="Название услуги")]
    service_price: Annotated[Decimal, Field(..., description="Цена услуги")]
    status: Annotated[str, Field(..., description="Статус записи")]
    client_phone: Annotated[str, Field(..., description="Телефон клиента")]
    notes: Annotated[Optional[str], Field(None, description="Заметки")]

    model_config = ConfigDict(from_attributes=False)


class MasterReportResponse(BaseModel):
    """Отчёт по мастеру за период: метаданные и список записей."""

    master_id: Annotated[int, Field(..., ge=1, description="ID мастера")]
    master_name: Annotated[str, Field(..., description="Имя мастера")]
    date_from: Annotated[date, Field(..., description="Начало периода")]
    date_to: Annotated[date, Field(..., description="Конец периода")]
    total_records: Annotated[int, Field(..., ge=0, description="Количество записей")]
    records: list[MasterReportRow] = Field(default_factory=list, description="Строки выгрузки")
