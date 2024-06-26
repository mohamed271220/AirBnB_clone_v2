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

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, class_name=None):
        """Returns a dictionary of models currently in storage"""
        if class_name:
            if type(class_name) == str:
                class_name = globals().get(class_name)
            if class_name and issubclass(class_name, BaseModel):
                return {k: v for k, v in self.__objects.items() if isinstance(v, class_name)}
        return FileStorage.__objects

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


        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

    def delete(self, obj = None):
        """
        Delete obj from __objects if it’s inside - if obj is equal to None,
        the method should not do anything
        """
        if obj is None:
            return
        targetObj = f"{obj.__class__.__name__}.{obj.id}"
        try:
            del FileStorage.__objects[targetObj]
        except AttributeError:
            pass
        except KeyboardInterrupt:
            pass
