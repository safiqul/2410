'''
an example to demonstrate OOP: inheritance in python
'''

from select import select
import sys

#base class 1
class person:
    def __init__(self, name, age):
        print('base: person constructor')
        self.name = name
        self.age = age
    def print_info(self):
        print(f'the name of the person is: {self.name} and age is: {self.age}')

    def __del__(self):
      print ("destroyed")

#base class 2:
class animal:
    def __init__(self, type):
        print('base: animal constructor')
        self.type = 'human'
    def print_type(self):
        print('the type is {}'.format(self.type))

#derived class

class woman(person, animal):
    def __init__(self, name, age, type, gender):
        print('derived: man constructor')
        self.gender = gender
        #invoking the init functions of the base classes
        person.__init__(self, name, age)
        animal.__init__(self, type)
    def print_gender(self):
        print('the gender is {}'.format(self.gender))

obj1 = woman('diba', 20, 'human', 'female')


#calling a method from base classes
obj1.print_info()
obj1.print_gender()

#calling the method from a derived class
obj1.print_type()
#deleting the object
del obj1