import pytest
from pydantic import ValidationError

from app.schemas.Worker import Login
from tests.unit.test_schemas.conftest import assert_single_validation_error
from tests.unit.test_schemas.test_worker.conftest import Name, Password
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes

name_test = Name()
password_test = Password()


class TestLogin:

    @pytest.mark.parametrize(
        "username, password",
        [
            (name_test.correct_name, password_test.correct_password),
            (name_test.correct_name_short, password_test.correct_password),
            (name_test.correct_name_long, password_test.correct_password),
            (name_test.correct_name, password_test.correct_password_short),
            (name_test.correct_name, password_test.correct_password_long),
            (name_test.correct_name, password_test.correct_password_integers),
        ]
    )
    def test_login_correct(self, username, password):
        login = Login(username=username, password=password)
        assert login.username == username
        assert login.password == password

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
    def test_login_wrong(self, username, password, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as exc_info:
            Login(username=username, password=password)
        assert_single_validation_error(exc_info.value.errors(), error_loc, error_type, error_msg)
