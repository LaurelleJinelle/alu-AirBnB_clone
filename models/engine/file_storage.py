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
        obj_dict = {key: value.to_dict() for key, 
                    value in FileStorage.__objects.items()}
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

    def reload(self):

        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.city import City
        from models.state import State
        from models.amenity import Amenity
        from models.review import Review

        # This is the dictionary we will be loading from the JSON file
        file_name = FileStorage.__file_path
        # We need to check if the file exists before we try to open it but we
        #   don't do anything if it doesn't exist
        if exists(file_name):
            # Here we open the file but since we are only reading from it,
            # We don't need to specify a mode or encode(cuz it's the default)
            with open(file_name) as f:
                obj_dict = load(f)
                # print(obj_dict)
        # At this point, we're able to print the JSON file but are still
        # in a dictionary form and need to be converted to object form

            for value in obj_dict.values():
                # This gets the class name of the object & the eval() function
                # makes sure the class type is "type" and not a string
                class_name = eval(value["__class__"])
                del value["__class__"]
                # Now we want to create a new object from the dictionary values
                # by passing them as keyword arguments to BaseModel, user...etc
                # Cuz both in the classes & here objects are changed to to_dict
                #   so when passed through ** we get new objects
                obj = class_name(**value)
                # Here we call on the new method from above because we want to
                # pass each newly iterated object to __objects
                self.new(obj)