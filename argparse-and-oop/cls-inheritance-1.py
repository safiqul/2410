'''
an example to demonstrate OOP in python
'''
import sys

#base class
class person:
    def __init__(self, name, age):
        print('parent constructor')
        self.name = name
        self.age = age
    def print_info(self):
        print(f'the name of the person is: {self.name} and age is: {self.age}')

    def __del__(self):
      class_name = self.__class__.__name__
      print (class_name, "destroyed")


#derived class
class woman(person):
    def __init__(self, name, age, gender):
        print('child constructor')
        self.gender = gender
        person.__init__(self, name, age)
    def print_gender(self):
        print('the gender is {}'.format(self.gender))
#creating an object

obj1 = woman('majda', 20, 'female')
obj1.print_info()
obj1.print_gender()
del obj1