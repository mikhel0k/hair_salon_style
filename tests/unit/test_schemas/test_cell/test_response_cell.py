import datetime

import pytest
from pydantic import ValidationError

from app.models import Cell
from app.schemas.Cell import CellResponse
from conftest import Time, Status, Date
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestResponseCell:
    time = Time()
    status = Status()
    date = Date()
    data_for_id = DataForId()

    @pytest.mark.parametrize("cell, date, time, status, master_id, cell_id", [
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.right_today, time.right_morning, status.right_free, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.right_tomorrow, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.right_tomorrow, time.right_morning, status.right_free, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.right_on_week_bigger, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.right_on_week_bigger, time.right_morning, status.right_free, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.right_date_string, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.right_date_string, time.right_morning, status.right_free, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.right_today, time=time.right_evening, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.right_today, time.right_evening, status.right_free, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.right_today, time=time.right_afternoon, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.right_today, time.right_afternoon, status.right_free, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.right_today, time=time.right_string, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.right_today, time.right_string, status.right_free, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.right_today, time=time.wrong_time_integer, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.right_today, time.wrong_time_integer, status.right_free, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.right_today, time=time.wrong_time_float, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.right_today, time.wrong_time_float, status.right_free, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.right_today, time=time.right_evening, status=status.right_occupied, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.right_today, time.right_evening, status.right_occupied, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.wrong_yesterday, time=time.right_evening, status=status.right_occupied, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.wrong_yesterday, time.right_evening, status.right_occupied, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.wrong_on_week_smaller, time=time.right_evening, status=status.right_occupied, master_id=data_for_id.right_id, id=data_for_id.right_id),
        date.wrong_on_week_smaller, time.right_evening, status.right_occupied, data_for_id.right_id, data_for_id.right_id),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.big_right_id, id=data_for_id.right_id),
        date.right_today, time.right_morning, status.right_free, data_for_id.big_right_id, data_for_id.right_id),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.big_right_id),
        date.right_today, time.right_morning, status.right_free, data_for_id.right_id, data_for_id.big_right_id),
    ])
    def test_response_cell(self, cell, date, time, status, master_id, cell_id):
        cell = CellResponse.model_validate(cell)
        assert isinstance(cell, CellResponse)
        assert cell.id == cell_id
        assert cell.master_id == master_id
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

    @pytest.mark.parametrize("cell, error_loc, error_type, error_msg",[
        (Cell(date=date.wrong_type_string, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("date",), ErrorTypes.DATE_FROM_DATETIME_PARSING, ErrorMessages.SHORT_DATE),
        (Cell(date=date.wrong_type_integer, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("date",), ErrorTypes.DATE_FROM_DATETIME_INEXACT, ErrorMessages.WRONG_DATE),
        (Cell(date=date.wrong_type_float, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("date",), ErrorTypes.DATE_FROM_DATETIME_INEXACT, ErrorMessages.WRONG_DATE),
        (Cell(date=date.wrong_type_boolean, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("date",), ErrorTypes.DATE_TIPE, ErrorMessages.VALID_DATE),
        (Cell(date=date.wrong_type_empty, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("date",), ErrorTypes.DATE_FROM_DATETIME_PARSING, ErrorMessages.SHORT_DATE),
        (Cell(date=date.wrong_type_none, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("date",), ErrorTypes.DATE_TIPE, ErrorMessages.VALID_DATE),
        (Cell(date=date.right_today, time=time.wrong_time_string, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("time",), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME),
        (Cell(date=date.right_today, time=time.wrong_time_boolean, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("time",), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME),
        (Cell(date=date.right_today, time=time.wrong_time_empty, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("time",), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME),
        (Cell(date=date.right_today, time=time.wrong_time_none, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("time",), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status_empty, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status_none, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status_float, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status_integer, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.right_today, time=time.right_morning, status=status.wrong_status_boolean, master_id=data_for_id.right_id, id=data_for_id.right_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.wrong_id_zero, id=data_for_id.right_id),
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.wrong_negative_id, id=data_for_id.right_id),
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.big_wrong_negative_id, id=data_for_id.right_id),
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.wrong_id_str, id=data_for_id.right_id),
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.wrong_id_none, id=data_for_id.right_id),
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.wrong_id_float, id=data_for_id.right_id),
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.wrong_id_true, id=data_for_id.right_id),
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.wrong_id_false, id=data_for_id.right_id),
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.wrong_id_zero),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.wrong_negative_id),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.big_wrong_negative_id),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.wrong_id_str),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.wrong_id_none),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.wrong_id_float),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.wrong_id_true),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.right_today, time=time.right_morning, status=status.right_free, master_id=data_for_id.right_id, id=data_for_id.wrong_id_false),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
    ])
    def test_response_cell_wrong(self, cell, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            cell = CellResponse.model_validate(cell)
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]
