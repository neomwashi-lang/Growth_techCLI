
from services.data_store import DataStore

def test_load_returns_empty_list_when_file_missing(tmp_path):
    ds = DataStore(tmp_path / "nonexistent.json")
    assert ds.load() == []

def test_save_then_load_roundtrip(tmp_path):
    ds = DataStore(tmp_path / "records.json")
    ds.save([{"id": 1, "name": "test"}])
    result = ds.load()
    assert result == [{"id": 1, "name": "test"}]

def test_next_id_on_empty_records(tmp_path):
    ds = DataStore(tmp_path / "unused.json")
    assert ds.next_id([]) == 1

def test_next_id_increments_from_max(tmp_path):
    ds = DataStore(tmp_path / "unused.json")
    records = [{"id": 1}, {"id": 5}, {"id": 2}]
    assert ds.next_id(records) == 6