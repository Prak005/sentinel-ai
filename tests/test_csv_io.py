from io import BytesIO
import pytest

from src.csv_io import read_traffic_csv


class Upload(BytesIO):
    def __init__(self, data: bytes, name: str = "sample.csv"):
        super().__init__(data)
        self.name = name
        self.size = len(data)


def test_reads_csv_and_normalizes_headers():
    uploaded = Upload(b"\xef\xbb\xbf f1 , f2 \n1,2\n")
    frame = read_traffic_csv(uploaded)
    assert list(frame.columns) == ["f1", "f2"]
    assert frame.iloc[0].tolist() == [1, 2]


def test_rejects_empty_file():
    with pytest.raises(ValueError, match="empty or does not contain"):
        read_traffic_csv(Upload(b""))


def test_rejects_header_only_file():
    with pytest.raises(ValueError, match="no data rows"):
        read_traffic_csv(Upload(b"f1,f2\n"))


def test_rejects_duplicate_headers_after_normalization():
    with pytest.raises(ValueError, match="Duplicate column names"):
        read_traffic_csv(Upload(b"f1, f1 \n1,2\n"))


def test_does_not_apply_a_second_smaller_upload_size_limit():
    uploaded = Upload(b"f1\n1\n")
    uploaded.size = 200 * 1024 * 1024
    frame = read_traffic_csv(uploaded)
    assert frame.iloc[0, 0] == 1


def test_model_feature_columns_are_parsed_as_float32(monkeypatch):
    import src.csv_io as csv_io

    monkeypatch.setattr(csv_io, "_model_feature_columns", lambda: ("f1",))
    frame = read_traffic_csv(Upload(b"f1,f2\n1.25,2\n3.5,4\n"))

    assert str(frame["f1"].dtype) == "float32"
    assert frame.iloc[0]["f1"] == pytest.approx(1.25)
