#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    'BaseModel': BaseModel, 'User': User, 'Place': Place,
    'State': State, 'City': City, 'Amenity': Amenity,
    'Review': Review
}


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""

        temp = {}
        if cls is None:
            return FileStorage.__objects

        for key, val in FileStorage.__objects.items():
            if val.to_dict()['__class__'] == cls:
                temp.update({key: val})
        return temp

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""

        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an instance from the __objects storage

        Args:
            obj (Object): _description_. Defaults to None.
            else delete the instance object
        """
        if obj is None:
            return
        class_name = obj.to_dict()['__class__']
        key = f"{class_name}.{obj.id}"
        if key in FileStorage.__objects:
            FileStorage.__objects.pop(key)
            FileStorage.save(self)

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
