#!/usr/bin/python3

from models.base_model import BaseModel

# User has public class attributes email, password, first_name, last_name


class User(BaseModel):
    """User class that inherits from BaseModel"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
