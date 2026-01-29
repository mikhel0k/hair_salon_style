import pytest
from pydantic import ValidationError

from conftest import Bool, Name, Password
from tests.unit.test_schemas.conftest_exceptions import DataForId, ErrorMessages, ErrorTypes

from app.schemas.Worker import WorkerCreate


class TestCreateWorker:
    bool_test = Bool()
    name_test = Name()
    password_test = Password()
    data_for_id = DataForId()


    @pytest.mark.parametrize(
        "master_id, username, password, is_master, is_admin, is_active",
        [
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true),
            (data_for_id.wrong_id_none, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true),
            (data_for_id.big_right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true),
            (data_for_id.right_id, name_test.wright_name_short, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true),
            (data_for_id.right_id, name_test.wright_name_long, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password_short,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password_long,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password_integers,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_false, bool_test.wright_true, bool_test.wright_true),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_false, bool_test.wright_true),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_false),
        ]
    )
    def test_create_worker_wright(self, master_id, username, password, is_master, is_admin, is_active):
        worker = WorkerCreate(
            master_id=master_id,
            username=username,
            password=password,
            is_master=is_master,
            is_admin=is_admin,
            is_active=is_active
        )
        assert worker.master_id == master_id
        assert worker.username == username
        assert worker.password == password
        assert worker.is_master == is_master
        assert worker.is_admin == is_admin
        assert worker.is_active == is_active


    @pytest.mark.parametrize(
        "master_id, username, password, is_master, is_admin, is_active, error_loc, error_type, error_msg",
        [
            (data_for_id.wrong_negative_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (data_for_id.big_wrong_negative_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (data_for_id.wrong_id_zero, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (data_for_id.wrong_id_str, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (data_for_id.wrong_id_true, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (data_for_id.wrong_id_false, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (data_for_id.wrong_id_float, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (data_for_id.right_id, name_test.wrong_empty_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("username",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (data_for_id.right_id, name_test.wrong_short_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("username",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (data_for_id.right_id, name_test.wrong_long_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("username",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG_30),
            (data_for_id.right_id, name_test.wrong_float, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("username",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (data_for_id.right_id, name_test.wrong_none, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("username",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (data_for_id.right_id, name_test.wrong_false, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("username",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (data_for_id.right_id, name_test.wrong_true, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("username",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (data_for_id.right_id, name_test.wrong_int, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("username",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wrong_none,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("password",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wrong_int,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("password",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wrong_float,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("password",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wrong_true,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("password",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wrong_false,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("password",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wrong_short_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("password",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT_8),
            (data_for_id.right_id, name_test.wright_name, password_test.wrong_long_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wright_true,
                ("password",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG_30),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wrong_str, bool_test.wright_true, bool_test.wright_true,
                ("is_master",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wrong_none, bool_test.wright_true, bool_test.wright_true,
                ("is_master",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wrong_int, bool_test.wright_true, bool_test.wright_true,
                ("is_master",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wrong_float, bool_test.wright_true, bool_test.wright_true,
                ("is_master",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wrong_str, bool_test.wright_true,
                ("is_admin",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wrong_none, bool_test.wright_true,
                ("is_admin",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wrong_int, bool_test.wright_true,
                ("is_admin",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wrong_float, bool_test.wright_true,
                ("is_admin",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wrong_str,
                ("is_active",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wrong_none,
                ("is_active",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wrong_int,
                ("is_active",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
            (data_for_id.right_id, name_test.wright_name, password_test.wright_password,
                bool_test.wright_true, bool_test.wright_true, bool_test.wrong_float,
                ("is_active",), ErrorTypes.BOOL_TYPE, ErrorMessages.BOOL_TYPE),
        ]
    )
    def test_create_worker_wrong(
            self,
            master_id,
            username,
            password,
            is_master,
            is_admin,
            is_active,
            error_loc,
            error_type,
            error_msg
    ):
        with pytest.raises(ValidationError) as error:
            worker = WorkerCreate(
                master_id=master_id,
                username=username,
                password=password,
                is_master=is_master,
                is_admin=is_admin,
                is_active=is_active
            )
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error["msg"] == error_msg
