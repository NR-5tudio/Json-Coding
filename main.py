import json
import EasyJson as nrjson
import sys
from rich import print
Error = False
path = None
if len(sys.argv) > 1:
    arg = sys.argv
    path = arg[1]


else:
    print("")
    exit()




data = nrjson.Load(path)


# Load JSON

# Variables dict
variables = {}

# Includes (kept if you need it)
includes = data.get("include", {})

# Function to run any list of actions
def run_actions(actions):
    for action in actions:
        if "var" in action:  # create/update variable
            exec(action["var"], {}, variables)
        if "print" in action:  # print (supports {var} placeholders)
            print(action["print"].format(**variables))

# Run begin (variables like Health are created here)
run_actions(data.get("begin", []))
running = True
while ("update" in data) and running:
    pass 

print("\n" * 5)
if not Error:
    print("[green]PROGRAM EXECUTION COMPLETED[/green]")
    print("- Script: ", sys.argv[0])