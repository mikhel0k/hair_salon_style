from app.schemas import EditRecordNote


class TestEditRecordNote:
    def test_edit_record_note_short(self):
        data = {
            "id": 1,
            "notes": "Note",
        }
        record = EditRecordNote(**data)
        assert record.id == data["id"]
        assert record.notes == data["notes"]

    def test_edit_record_note_long(self):
        data = {
            "id": 1,
            "notes": "asdsadasdasdasvdgavsgdvahgsdvasdasdasdsfdshuv dscs bduwhb nvjdkw vijwfen vijkw vefknfkhsvdya"
                    "sfdvyasdvadqimvodfwnmv iofdmnv oim iowf mmfwvo emdv oikfwd niodk fvmosytdvasytdvasytdvasydtvasy"
                    "tdvgasodkfn vwfn okfdl moin wodfn kmo,v miodn jkn doi kmo ifnm iew omf ovkdvbaygsdvgysvdygas",
        }
        record = EditRecordNote(**data)
        assert record.id == data["id"]
        assert record.notes == data["notes"]

    def test_edit_record_note_empty(self):
        data = {
            "id": 1,
            "notes": "",
        }
        record = EditRecordNote(**data)
        assert record.id == data["id"]
        assert record.notes == data["notes"]

    def test_edit_record_note_is_none(self):
        data = {
            "id": 1,
        }
        record = EditRecordNote(**data)
        assert record.id == data["id"]
        assert record.notes is None
