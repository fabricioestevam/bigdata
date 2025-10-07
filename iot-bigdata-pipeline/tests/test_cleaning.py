from src.data_cleaning.cleaners import DataCleaner

def test_outlier_correction():
    cleaner = DataCleaner()
    data = {"temperature": 150}
    cleaned = cleaner.clean(data)
    assert cleaned["temperature"] == 25.0
    assert "_outlier_corrected" in cleaned
