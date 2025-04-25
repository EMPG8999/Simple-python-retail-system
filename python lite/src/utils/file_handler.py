import json
import os
from typing import List, Dict, Any

class FileHandler:
    @staticmethod
    def read_data(filename: str) -> List[Dict]:
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def write_data(filename: str, data: List[Dict]) -> None:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def append_data(filename: str, data: Dict) -> None:
        existing_data = FileHandler.read_data(filename)
        existing_data.append(data)
        FileHandler.write_data(filename, existing_data)

    @staticmethod
    def update_data(filename: str, condition: callable, new_data: Dict) -> bool:
        data = FileHandler.read_data(filename)
        for i, item in enumerate(data):
            if condition(item):
                data[i].update(new_data)
                FileHandler.write_data(filename, data)
                return True
        return False 