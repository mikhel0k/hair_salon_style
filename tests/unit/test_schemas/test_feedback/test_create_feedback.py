import pytest

from app.schemas.Feedback import FeedbackCreate
from tests.unit.test_schemas.conftest_exceptions import DataForId
from conftest import Estimation, Comment


class TestCreateFeedback:
    estimation = Estimation()
    comment = Comment()
    data_for_id = DataForId()

    @pytest.mark.parametrize(
        "feedback_id,estimation_data,comment_data",
        [
            (data_for_id.right_id, estimation.right_estimation_one, comment.right_short_comment),
            (data_for_id.right_id, estimation.right_estimation_two, comment.right_short_comment),
            (data_for_id.right_id, estimation.right_estimation_three, comment.right_short_comment),
            (data_for_id.right_id, estimation.right_estimation_four, comment.right_short_comment),
            (data_for_id.right_id, estimation.right_estimation_five, comment.right_short_comment),
            (data_for_id.big_right_id, estimation.right_estimation_one, comment.right_short_comment),
            (data_for_id.right_id, estimation.right_estimation_one, comment.right_long_comment),
            (data_for_id.right_id, estimation.right_estimation_one, comment.right_none_comment),
        ]
    )
    def test_right_short_comment(self, feedback_id, estimation_data, comment_data):
        feedback = FeedbackCreate(
            record_id=feedback_id,
            master_estimation=estimation_data,
            master_comment=comment_data,
            salon_estimation=estimation_data,
            salon_comment=comment_data,
        )
        assert feedback.record_id == feedback_id
        assert feedback.master_estimation == estimation_data
        assert feedback.master_comment == comment_data
        assert feedback.salon_estimation == estimation_data
        assert feedback.salon_comment == comment_data
