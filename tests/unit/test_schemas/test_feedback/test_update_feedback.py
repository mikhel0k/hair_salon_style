import pytest
from pydantic import ValidationError

from app.schemas.Feedback import FeedbackUpdate
from tests.unit.test_schemas.conftest_exceptions import DataForId, ErrorTypes, ErrorMessages
from conftest import Estimation, Comment


class TestUpdateFeedback:
    estimation = Estimation()
    comment = Comment()
    data_for_id = DataForId()

    @pytest.mark.parametrize(
        "estimation_data,comment_data",
        [
            (estimation.right_estimation_one, comment.right_short_comment),
            (estimation.right_estimation_two, comment.right_short_comment),
            (estimation.right_estimation_three, comment.right_short_comment),
            (estimation.right_estimation_four, comment.right_short_comment),
            (estimation.right_estimation_five, comment.right_short_comment),
            (estimation.right_estimation_one, comment.right_short_comment),
            (estimation.right_estimation_one, comment.right_long_comment),
            (estimation.right_estimation_one, comment.right_none_comment),
            (None, comment.right_short_comment),
            (estimation.right_estimation_one, None),
        ]
    )
    def test_right_update_feedback(self, estimation_data, comment_data):
        feedback = FeedbackUpdate(
            master_estimation=estimation_data,
            master_comment=comment_data,
            salon_estimation=estimation_data,
            salon_comment=comment_data,
        )
        assert feedback.master_estimation == estimation_data
        assert feedback.master_comment == comment_data
        assert feedback.salon_estimation == estimation_data
        assert feedback.salon_comment == comment_data


    @pytest.mark.parametrize(
        "master_estimation,master_comment,salon_estimation,salon_comment,error_loc,error_type,error_msg",
        [
            (estimation.wrong_estimation_six, comment.right_short_comment,
             estimation.right_estimation_one, comment.right_short_comment,
             ("master_estimation",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.LESS_THAN_EQUAL_5),
            (estimation.wrong_estimation_zero, comment.right_short_comment,
             estimation.right_estimation_one, comment.right_short_comment,
             ("master_estimation",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (estimation.wrong_estimation_negative_one, comment.right_short_comment,
             estimation.right_estimation_one, comment.right_short_comment,
             ("master_estimation",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (estimation.wrong_estimation_float, comment.right_short_comment,
             estimation.right_estimation_one, comment.right_short_comment,
             ("master_estimation",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (estimation.wrong_estimation_true, comment.right_short_comment,
             estimation.right_estimation_one, comment.right_short_comment,
             ("master_estimation",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (estimation.wrong_estimation_false, comment.right_short_comment,
             estimation.right_estimation_one, comment.right_short_comment,
             ("master_estimation",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (estimation.wrong_estimation_string, comment.right_short_comment,
             estimation.right_estimation_one, comment.right_short_comment,
             ("master_estimation",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (estimation.right_estimation_one, comment.right_short_comment,
             estimation.wrong_estimation_six, comment.right_short_comment,
             ("salon_estimation",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.LESS_THAN_EQUAL_5),
            (estimation.right_estimation_one, comment.right_short_comment,
             estimation.wrong_estimation_zero, comment.right_short_comment,
             ("salon_estimation",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (estimation.right_estimation_one, comment.right_short_comment,
             estimation.wrong_estimation_negative_one, comment.right_short_comment,
             ("salon_estimation",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (estimation.right_estimation_one, comment.right_short_comment,
             estimation.wrong_estimation_float, comment.right_short_comment,
             ("salon_estimation",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (estimation.right_estimation_one, comment.right_short_comment,
             estimation.wrong_estimation_true, comment.right_short_comment,
             ("salon_estimation",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (estimation.right_estimation_one, comment.right_short_comment,
             estimation.wrong_estimation_false, comment.right_short_comment,
             ("salon_estimation",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (estimation.right_estimation_one, comment.right_short_comment,
             estimation.wrong_estimation_string, comment.right_short_comment,
             ("salon_estimation",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (estimation.right_estimation_one, comment.wrong_float_comment,
             estimation.right_estimation_one, comment.right_short_comment,
             ("master_comment",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (estimation.right_estimation_one, comment.wrong_bool_comment,
             estimation.right_estimation_one, comment.right_short_comment,
             ("master_comment",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (estimation.right_estimation_one, comment.wrong_int_comment,
             estimation.right_estimation_one, comment.right_short_comment,
             ("master_comment",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (estimation.right_estimation_one, comment.right_short_comment,
             estimation.right_estimation_one, comment.wrong_float_comment,
             ("salon_comment",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (estimation.right_estimation_one, comment.right_short_comment,
             estimation.right_estimation_one, comment.wrong_bool_comment,
             ("salon_comment",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (estimation.right_estimation_one, comment.right_short_comment,
             estimation.right_estimation_one, comment.wrong_int_comment,
             ("salon_comment",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        ]
    )
    def test_wrong_update_feedback(
            self,
            master_estimation,
            master_comment,
            salon_estimation,
            salon_comment,
            error_loc,
            error_type,
            error_msg
    ):
        with pytest.raises(ValidationError) as error:
            feedback = FeedbackUpdate(
                master_estimation=master_estimation,
                master_comment=master_comment,
                salon_estimation=salon_estimation,
                salon_comment=salon_comment,
            )
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]
