'''using argparse module for user friendly command-line interfaces
you will define arguments you need and argparse will 
parse these arguments from sys.argv.
'''
import argparse
import sys

#we create an argparse object with a description - what the program does
parser = argparse.ArgumentParser(description='positional arguments')

#attaches individual argument specifications to the parser. 
#help: Help message for an argument
parser.add_argument('name', help='Enter your name')

#runs the parser and places the extracted data
args = parser.parse_args()

#can access the arg with . operator"
print ('your name is: ', args.name)
