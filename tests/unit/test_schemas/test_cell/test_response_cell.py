import datetime

import pytest
from pydantic import ValidationError

from app.models import Cell
from app.schemas.Cell import CellResponse
from conftest import Time, Status, Date
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes


class TestCreateCell:
    time = Time()
    status = Status()
    date = Date()

    @pytest.mark.parametrize("cell, date, time, status", [
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=1, id=1),
        date.right_today, time.right_morning, status.right_free),
        (Cell(date=date.right_tomorrow, time=time.right_morning, status=status.right_free, master_id=1, id=1),
        date.right_tomorrow, time.right_morning, status.right_free),
        (Cell(date=date.right_on_week_bigger, time=time.right_morning, status=status.right_free, master_id=1, id=1),
        date.right_on_week_bigger, time.right_morning, status.right_free),
        (Cell(date=date.right_date_string, time=time.right_morning, status=status.right_free, master_id=1, id=1),
        date.right_date_string, time.right_morning, status.right_free),
        (Cell(date=date.right_today, time=time.right_evening, status=status.right_free, master_id=1, id=1),
        date.right_today, time.right_evening, status.right_free),
        (Cell(date=date.right_today, time=time.right_afternoon, status=status.right_free, master_id=1, id=1),
        date.right_today, time.right_afternoon, status.right_free),
        (Cell(date=date.right_today, time=time.right_string, status=status.right_free, master_id=1, id=1),
        date.right_today, time.right_string, status.right_free),
        (Cell(date=date.right_today, time=time.wrong_time_integer, status=status.right_free, master_id=1, id=1),
        date.right_today, time.wrong_time_integer, status.right_free),
        (Cell(date=date.right_today, time=time.wrong_time_float, status=status.right_free, master_id=1, id=1),
        date.right_today, time.wrong_time_float, status.right_free),
        (Cell(date=date.right_today, time=time.right_evening, status=status.right_occupied, master_id=1, id=1),
        date.right_today, time.right_evening, status.right_occupied),
        (Cell(date=date.wrong_yesterday, time=time.right_evening, status=status.right_occupied, master_id=1, id=1),
        date.wrong_yesterday, time.right_evening, status.right_occupied),
        (Cell(date=date.wrong_on_week_smaller, time=time.right_evening, status=status.right_occupied, master_id=1, id=1),
        date.wrong_on_week_smaller, time.right_evening, status.right_occupied),
    ])
    def test_response_cell(self, cell, date, time, status):
        cell = CellResponse.model_validate(cell)
        assert isinstance(cell, CellResponse)
        assert cell.id == 1
        assert cell.master_id == 1
        assert cell.status == status

        actual_time = cell.time.replace(tzinfo=None)

        if isinstance(time, datetime.time):
            assert actual_time == time
        elif isinstance(time, str):
            assert actual_time == datetime.time.fromisoformat(time)
        elif isinstance(time, (int, float)):
            assert actual_time == datetime.time(second=int(time))

        if isinstance(date, datetime.date):
            assert cell.date == date
        elif isinstance(date, str):
            assert cell.date == datetime.date.fromisoformat(date)

    @pytest.mark.parametrize("cell, error_type, error_msg",[
        (Cell(date=date.wrong_type_string, time=time.right_morning, status=status.right_free, master_id=1, id=1),
         ErrorTypes.DATE_FROM_DATETIME_PARSING , ErrorMessages.SHORT_DATE ),
        (Cell(date=date.wrong_type_integer, time=time.right_morning, status=status.right_free, master_id=1, id=1),
         ErrorTypes.DATE_FROM_DATETIME_INEXACT , ErrorMessages.WRONG_DATE ),
        (Cell(date=date.wrong_type_float, time=time.right_morning, status=status.right_free, master_id=1, id=1),
         ErrorTypes.DATE_FROM_DATETIME_INEXACT , ErrorMessages.WRONG_DATE ),
        (Cell(date=date.wrong_type_boolean, time=time.right_morning, status=status.right_free, master_id=1, id=1),
         ErrorTypes.DATE_TIPE , ErrorMessages.VALID_DATE ),
        (Cell(date=date.wrong_type_empty, time=time.right_morning, status=status.right_free, master_id=1, id=1),
         ErrorTypes.DATE_FROM_DATETIME_PARSING , ErrorMessages.SHORT_DATE ),
        (Cell(date=date.wrong_type_none, time=time.right_morning, status=status.right_free, master_id=1, id=1),
         ErrorTypes.DATE_TIPE , ErrorMessages.VALID_DATE ),
        (Cell(date=date.right_today, time=time.wrong_time_string, status=status.right_free, master_id=1, id=1),
         ErrorTypes.TIME_PARSING , ErrorMessages.SHORT_TIME ),
        (Cell(date=date.right_today, time=time.wrong_time_boolean, status=status.right_free, master_id=1, id=1),
         ErrorTypes.TIME_TYPE , ErrorMessages.VALID_TIME ),
        (Cell(date=date.right_today, time=time.wrong_time_empty, status=status.right_free, master_id=1, id=1),
         ErrorTypes.TIME_PARSING , ErrorMessages.SHORT_TIME ),
        (Cell(date=date.right_today, time=time.wrong_time_none, status=status.right_free, master_id=1, id=1),
         ErrorTypes.TIME_TYPE , ErrorMessages.VALID_TIME ),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status, master_id=1, id=1),
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status_empty, master_id=1, id=1),
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status_none, master_id=1, id=1),
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status_float, master_id=1, id=1),
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status_integer, master_id=1, id=1),
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status_boolean, master_id=1, id=1),
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
    ])
    def test_response_cell_wrong(self, cell, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            cell = CellResponse.model_validate(cell)
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["type"] == error_type
        assert error_msg in error.value.errors()[0]["msg"]
