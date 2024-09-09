#!/usr/bin/python3
"""
This script initializes the models package by setting up the
storage engine and loading any saved data.
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
