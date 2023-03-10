import sys

print ("this is the name of your program", sys.argv[0])

print ("length of your aruguments", len(sys.argv))

#exit if we don't have more than one argument
if len(sys.argv)<2:
    print ("usage: you must enter a number")
    sys.exit()
print ("the second number is", sys.argv[1])

#if we have 3 arguments with 2 numbers - 
if len(sys.argv) > 3 and sys.argv[3] == '+':
    print ('the sum is', int(sys.argv[1]) + int(sys.argv[2]))
    