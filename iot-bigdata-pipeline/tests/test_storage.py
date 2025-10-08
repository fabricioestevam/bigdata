import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.storage import MongoDBStore

class TestStorage:
    def test_storage_connection(self):
        try:
            storage = MongoDBStore()
            assert storage.client is not None
        except Exception as e:
            pytest.skip(f"MongoDB not available: {e}")