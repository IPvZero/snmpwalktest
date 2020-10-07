import subprocess
from getpass import getpass
from rich.console import Console
from rich.table import Table
import itertools

good_list = []
bad_list = []
username = input("Username: ")
password = getpass()

with open('reader.txt', 'r') as f:
    filelines = f.readlines()
for ip in filelines:
    getResult =  subprocess.Popen(f"snmpwalk -v3  -l authPriv -u {username} -a SHA -A {password} {ip}", shell=True, stdout=subprocess.PIPE).stdout
    output =  getResult.read()
    result = output.decode()
    print(result)
    if "IF-MIB" in result:
        good_list.append(ip)
    else:
        bad_list.append(ip)

table = Table(title="SUMMARY REPORT \n")
table.add_column("Successful Hosts", justify="center", style="green")
table.add_column("Failed Hosts", justify="center",style="red")
for (success, fail) in itertools.zip_longest(good_list, bad_list):
    table.add_row(success, fail)
console = Console()
console.print(table)
