#!/bin/python
import sys
import os
sys.path.insert(0, os.path.join("..","..","src"))

import miniflask
mf = miniflask.init(
    modules_dir="./modules",
)
mf.load("moduleunique")

class event():

    @classmethod
    def func(cls, x):
        return x

a = 0
for i in range(10000000):
    a += event.func(42)