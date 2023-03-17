import ipaddress
import argparse


def check_ip(address):
    '''check if an address is a valid IPv4 address'''
    try:
       val = ipaddress.ip_address(address)
       print(f"The IP address {val} is valid.")
    except ValueError:
       print(f"The IP address is {address} not valid")


parser = argparse.ArgumentParser(description="Optional arguments: checking IPv4 address", epilog="end of help")
parser.add_argument('-I' , '--ip', type=str, required=True)

args = parser.parse_args()

check_ip(args.ip)
