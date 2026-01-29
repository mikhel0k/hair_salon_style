import pytest
from pydantic import ValidationError

from conftest import Name, Password
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes

from app.schemas.Worker import Login


class TestCreateWorker:
    name_test = Name()
    password_test = Password()


    @pytest.mark.parametrize(
        "username, password",
        [
            (name_test.correct_name, password_test.correct_password),
            (name_test.correct_name, password_test.correct_password),
            (name_test.correct_name, password_test.correct_password),
            (name_test.correct_name_short, password_test.correct_password),
            (name_test.correct_name_long, password_test.correct_password),
            (name_test.correct_name, password_test.correct_password_short),
            (name_test.correct_name, password_test.correct_password_long),
            (name_test.correct_name, password_test.correct_password_integers),
            (name_test.correct_name, password_test.correct_password),
            (name_test.correct_name, password_test.correct_password),
            (name_test.correct_name, password_test.correct_password),
        ]
    )
    def test_create_worker_correct(self, username, password):
        worker = Login(
            username=username,
            password=password
        )
        assert worker.username == username
        assert worker.password == password


    @pytest.mark.parametrize(
        "username, password, error_loc, error_type, error_msg",
        [
            (name_test.wrong_empty_name, password_test.correct_password,
                ("username",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name_test.wrong_short_name, password_test.correct_password,
                ("username",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name_test.wrong_long_name, password_test.correct_password,
                ("username",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG_30),
            (name_test.wrong_float, password_test.correct_password,
                ("username",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name_test.wrong_none, password_test.correct_password,
                ("username",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name_test.wrong_false, password_test.correct_password,
                ("username",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name_test.wrong_true, password_test.correct_password,
                ("username",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name_test.wrong_int, password_test.correct_password,
                ("username",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name_test.correct_name, password_test.wrong_none,
                ("password",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name_test.correct_name, password_test.wrong_int,
                ("password",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name_test.correct_name, password_test.wrong_float,
                ("password",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name_test.correct_name, password_test.wrong_true,
                ("password",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name_test.correct_name, password_test.wrong_false,
                ("password",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name_test.correct_name, password_test.wrong_short_password,
                ("password",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT_8),
            (name_test.correct_name, password_test.wrong_long_password,
                ("password",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG_30),
        ]
    )
    def test_create_worker_wrong(
            self,
            username,
            password,
            error_loc,
            error_type,
            error_msg
    ):
        with pytest.raises(ValidationError) as error:
            worker = Login(
                username=username,
                password=password,
            )
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error["msg"] == error_msg
