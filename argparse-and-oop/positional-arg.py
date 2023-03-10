'''using argparse module for user friendly command-line interfaces
you will define arguments you need and argparse will 
parse these arguments from sys.argv. This program will show the usage of positional 
arguments. 
'''
import argparse
import sys

#we create an argparse parser object with a description - what the program does
parser = argparse.ArgumentParser(description='A simple calculator')

#attaches individual argument specifications to the parser. 
#metvar: Alternate display name for the argument as shown in help
#type: automatically convert the type
#help: Help message for an argument
parser.add_argument('num1', metavar='N1', help='Enter your first number', type=int)
parser.add_argument('num2', metavar='N2', help='Enter your second number', type=int)
parser.add_argument('op', metavar='op', help='enter the op')

#runs the parser and places the extracted data
args = parser.parse_args()

if args.op == 'add':
    print ('the sum is', args.num1 + args.num2)

if args.op == 'sub':
    print ('the difference is', args.num1 - args.num2)
