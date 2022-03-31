from typing import Dict, Callable, Set
from pydantic import BaseModel


class Store:

    records: Dict[str, Dict] = {}
    data_model: BaseModel = None

    def __init__(self, records: Dict = None, data_model: BaseModel = None):
        if records:
            self.records = records
        if data_model:
            self.data_model = data_model

    def get(self, key: str = None, fn: Callable = None):

        if key:
            if self.data_model is not None:
                return self.data_model( **self.records.get(key))
            return self.records.get(key, None)

        if fn:
            return fn(self.records)

        return None

    def put(self, key: str, data: Dict):

        if key in self.records.keys():
            if self.data_model is not None:
                record = self.data_model(**data)
                self.records[key].update(record.dict())

            else:
                self.records[key].update(data)
        else:
            raise RuntimeError('Unknown record provided for update. Please use post to create new records.')
        return self.records[key]

    def post(self, key: str, data: Dict, upsert: bool = False):

        if key in self.records.keys() and not upsert:
            raise RuntimeError('Record already exists, please use put or toggle upsert=True')
        elif key in self.records.keys():
            self.records[key].update(data)
        else:
            self.records[key] = data

        return self.records[key]
