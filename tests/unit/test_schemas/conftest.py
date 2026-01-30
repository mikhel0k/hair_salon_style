def assert_single_validation_error(errors, loc, error_type, msg_contains):
    assert len(errors) == 1, f"Expected 1 error, got {len(errors)}: {errors}"
    err = errors[0]
    assert err["loc"] == loc, f"Expected loc {loc}, got {err['loc']}"
    assert err["type"] == error_type, f"Expected type {error_type}, got {err['type']}"
    if isinstance(msg_contains, (list, tuple)):
        assert any(m in err["msg"] for m in msg_contains), f"None of {msg_contains} found in {err['msg']}"
    else:
        assert msg_contains in err["msg"], f"Expected '{msg_contains}' in '{err['msg']}'"


def make_name_fixture(min_length: int = 3, max_length: int = 60, default_name: str = "Name", cyrillic: str = "Стрижка"):
    half = min_length // 2
    attrs = dict(
        correct_name=default_name,
        correct_name_short="a" * min_length,
        correct_name_long="a" * max_length,
        correct_name_cyrillic=cyrillic,
        wrong_name_long="a" * (max_length + 1),
        wrong_name_short="a" * (min_length - 1),
        wrong_name_int=1,
        wrong_name_empty="",
        wrong_name_spaces="   ",
        wrong_name_none=None,
        wrong_invalid_character=f"{'a' * min_length}?",
        wrong_consecutive_spaces=f"{'a' * half}  {'a' * (half + 1)}",
        wrong_consecutive_hyphens=f"{'a' * half}--{'a' * (half + 1)}",
        wrong_consecutive_apostrophes=f"{'a' * half}``{'a' * (half + 1)}",
        wrong_consecutive_underscores=f"{'a' * half}__{'a' * (half + 1)}",
        wrong_start_with_hyphen=f"-{'a' * min_length}",
        wrong_start_with_apostrophe=f"`{'a' * min_length}",
        wrong_start_with_underscore=f"_{'a' * min_length}",
        wrong_end_with_hyphen=f"{'a' * min_length}-",
        wrong_end_with_apostrophe=f"{'a' * min_length}`",
        wrong_end_with_underscore=f"{'a' * min_length}_",
        wrong_space_and_hyphen_adjacent=f"{'a' * half} -{'a' * (half + 1)}",
        wrong_space_and_apostrophe_adjacent=f"{'a' * half} `{'a' * (half + 1)}",
        wrong_space_and_underscore_adjacent=f"{'a' * half} _{'a' * (half + 1)}",
        wrong_hyphen_and_space_adjacent=f"{'a' * half}- {'a' * (half + 1)}",
        wrong_apostrophe_and_space_adjacent=f"{'a' * half}` {'a' * (half + 1)}",
        wrong_underscore_and_space_adjacent=f"{'a' * half}_ {'a' * (half + 1)}",
    )
    return type("Name", (), attrs)
