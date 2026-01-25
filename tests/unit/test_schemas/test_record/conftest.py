from dataclasses import dataclass


@dataclass
class AllowedRecordStatuses:
    Created = "CREATED"
    Confirmed = "CONFIRMED"
    Completed = "COMPLETED"
    Cancelled = "CANCELLED"
    wrong_status_string = "string"
    wrong_status_none = None
    wrong_status_empty = ""
    wrong_status_boolean = True
    wrong_status_integer = 1
    wrong_status_float = 1.0


@dataclass
class Phone:
    right_number_str_with_seven = "+79009009090"
    right_number_str_with_eight = "89009009090"
    right_number_int = 89009009090
    right_number_str_with_seven_without_plus = "79009009090"
    wrong_number_str_with_two_without_plus = "29009009090"
    wrong_number_str_with_five_without_plus = "59009009090"
    wrong_number_str_with_two_with_plus = "+29009009090"
    wrong_number_str_with_five_with_plus = "+59009009090"
    wrong_number_str_with_eight_with_plus = "+89009009090"
    wrong_number_str_with_seven_short = "+790090090"
    wrong_number_int_short = 890090090
    wrong_number_str_with_seven_long = "+7900900909090"
    wrong_number_int_long = 8900900909090
    wrong_number_none = None
    wrong_number_empty = ""
    wrong_number_true = True
    wrong_number_false = False
