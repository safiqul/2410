'''using argparse module for user friendly command-line interfaces
you will define arguments you need and argparse will 
parse these arguments from sys.argv. This program will show the usage of optional  
arguments starting with -. 
'''

import argparse
import sys


def check_port(val):
    try:
        value = int(val)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')
    if (value<=0):
        print('it is not a valid port')
        sys.exit()
    return value


parser = argparse.ArgumentParser(description="positional arguments", epilog="end of help")


#arguments with short name and long name
#NOTE: you must access the value with args.longname, e.g., args.num1
parser.add_argument('-n1' , '--num1', type=int, required=True)
parser.add_argument('-n2' , '--num2', type=int, default=10)
parser.add_argument('-p', '--port', type=check_port)

#how to use boolean values here
parser.add_argument('-s', '--server', action='store_true')

#use append
parser.add_argument('-l', '--values', help="can hold multiple values", action='append', default=[])

#offer list of options: you must select from the choices
parser.add_argument('-m', '--mode', choices=('add', 'sub'))


args = parser.parse_args()

print ("your number is: ", args.num1)
print ("your 2nd number is: ", args.num2)


#print all the appended values with -l
print ("your list values are: ", args.values)


#ports

print ("your port number is: ", args.port)


#checking if the server flag is set
if args.server:
    print ('the server is on ', args.server)