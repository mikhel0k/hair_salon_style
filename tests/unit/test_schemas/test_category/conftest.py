from tests.unit.test_schemas.conftest import make_name_fixture

Name = make_name_fixture(min_length=3, max_length=60, default_name="Haircut")
