import sys
import rich as r
from Engine.engine import get_functions, run_actions
from Engine.nrjson import nrjson


if len(sys.argv) < 2:
    r.print("[red]Missing arg: <file.json>[/red]")
    sys.exit(1)

data = nrjson.load(sys.argv[1])
all_functions = get_functions(data)          # "begin" is NOT callable here (prevents recursion)

run_actions(data.get("begin", []), all_functions)

update_actions = data.get("update", [])
running = True
while update_actions and running:
    if run_actions(update_actions, all_functions) == "__exit__":
        running = False

r.print("\n[green]PROGRAM EXECUTION COMPLETED[/green]")
r.print("- Script:", sys.argv[1])