'''
an example to demonstrate OOP in python
'''

import sys

class person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def print_info(self):
        print(f'the name of the person is: {self.name} and age is: {self.age}')

    def __del__(self):
      class_name = self.__class__.__name__
      print (class_name, "destroyed")

#creating an object
obj1 = person('peter', 20)
obj1.print_info()
del obj1