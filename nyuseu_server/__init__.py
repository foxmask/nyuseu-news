# coding: utf-8
import os
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
with open(f'{PROJECT_DIR}/VERSION.txt', 'r') as f:
    __version__ = f.read()
