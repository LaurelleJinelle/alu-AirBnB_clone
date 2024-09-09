#!/usr/bin/python3

from json import dump, load
from os.path import exists

class FileStorage:
    # Private class attributes for storing file path and objects
    __file_path = "file.json"  # Path to the JSON file used for storage
    __objects = {}  # Dictionary to store all objects by <class name>.id

    def all(self):
        # Returns the dictionary containing all stored objects
        return FileStorage.__objects

    def new(self, obj):
        # Adds a new object to the __objects dictionary
        # The key is created as <class name>.<object id>
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        # Serializes the __objects dictionary to the JSON file at __file_path
        # Converts each object to a dictionary using the to_dict() method
        obj_dict = {key: value.to_dict() for key, value in FileStorage.__objects.items()}
        # Writes the serialized data (as JSON) to the file
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            dump(obj_dict, f)

    def reload(self):
        # Deserializes the JSON file to load stored objects back into __objects
        if exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                loaded_dict = load(f)
                # Reconstruct each object using the class name and data
                for key, value in loaded_dict.items():
                    class_name = key.split('.')[0]  # Extract class name from key
                    # Assuming dynamic class instantiation using eval
                    self.__objects[key] = eval(f"{class_name}(**value)")
