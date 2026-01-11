import pytest
from pydantic import ValidationError

from app.schemas.SpecializationService import SpecializationServicesSchema

from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestSpecializationServicesSchema:
    data_for_id = DataForId()

    @pytest.mark.parametrize("specialization_id, services_id",[
        (data_for_id.right_id, [data_for_id.right_id, ]),
        (data_for_id.big_right_id, [data_for_id.right_id, ])
    ])
    def test_specialization_services_schema_create(self, specialization_id, services_id):
        specialization_services = SpecializationServicesSchema(
            specialization_id=specialization_id,
            services_id=services_id
        )
        assert isinstance(specialization_services, SpecializationServicesSchema)
        assert specialization_services.specialization_id == specialization_id
        assert specialization_services.services_id == set(services_id)

    @pytest.mark.parametrize("specialization_id, services_id, error_loc, error_type, error_msg",[
        (data_for_id.wrong_id_zero, [data_for_id.right_id,],
         ("specialization_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.wrong_negative_id, [data_for_id.right_id,],
         ("specialization_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.big_wrong_negative_id, [data_for_id.right_id,],
         ("specialization_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.wrong_id_str, [data_for_id.right_id,],
         ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_float, [data_for_id.right_id,],
         ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_str, [data_for_id.right_id,],
         ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_true, [data_for_id.right_id,],
         ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_false, [data_for_id.right_id,],
         ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.right_id, [data_for_id.wrong_id_zero, data_for_id.right_id,],
         ("services_id", 0), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.right_id, [data_for_id.wrong_negative_id, data_for_id.right_id,],
         ("services_id", 0), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.right_id, [data_for_id.big_wrong_negative_id, data_for_id.right_id,],
         ("services_id", 0), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.right_id, [data_for_id.right_id, data_for_id.wrong_id_zero,],
         ("services_id", 1), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.right_id, [data_for_id.right_id, data_for_id.wrong_negative_id,],
         ("services_id", 1), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.right_id, [data_for_id.right_id, data_for_id.big_wrong_negative_id,],
         ("services_id", 1), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.right_id, [data_for_id.wrong_id_str, data_for_id.right_id,],
         ("services_id", 0), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.right_id, [data_for_id.wrong_id_none, data_for_id.right_id,],
         ("services_id", 0), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.right_id, [data_for_id.wrong_id_float, data_for_id.right_id,],
         ("services_id", 0), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.right_id, [data_for_id.wrong_id_true, data_for_id.right_id,],
         ("services_id", 0), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.right_id, [data_for_id.wrong_id_false, data_for_id.right_id,],
         ("services_id", 0), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.right_id, [data_for_id.right_id, data_for_id.wrong_id_str,],
         ("services_id", 1), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.right_id, [data_for_id.right_id, data_for_id.wrong_id_none,],
         ("services_id", 1), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.right_id, [data_for_id.right_id, data_for_id.wrong_id_float,],
         ("services_id", 1), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.right_id, [data_for_id.right_id, data_for_id.wrong_id_false,],
         ("services_id", 1), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
    ])
    def test_specialization_services_schema_wrong(self, specialization_id, services_id, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            record = SpecializationServicesSchema(
            specialization_id=specialization_id,
            services_id=services_id
        )
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]
