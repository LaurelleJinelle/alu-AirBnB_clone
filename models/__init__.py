#!/usr/bin/python3
"""
This script initializes the models package by setting up the
storage engine and loading any saved data.
"""
from models.engine.file_storage import FileStorage

# Initialize the storage system
storage = FileStorage()

# Load any previously saved objects from file storage
storage.reload()
