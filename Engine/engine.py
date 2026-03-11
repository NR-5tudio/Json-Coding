import re
import rich as r
import Engine.state as state
from Engine.blocks import BUILTIN_HANDLERS

# ─── Return Signal ────────────────────────────────────────────────────────────

class ReturnValue:
    """Wraps a function's return value so it doesn't accidentally stop callers."""
    def __init__(self, value):
        self.value = value

# ─── Value Helpers ────────────────────────────────────────────────────────────

def resolve_value(val, local_vars, all_functions=None):
    """Substitute {placeholder} in strings.
    
    Placeholders are resolved in this order:
      1. local_vars
      2. state.variables
      3. all_functions — if the name matches a function, call it and use the return value
    """
    if not isinstance(val, str):
        return val

    merged = {**state.variables, **local_vars}

    # Find any {placeholder} that is NOT already in merged variables
    if all_functions:
        for name in re.findall(r'\{(\w+)\}', val):
            if name not in merged and name in all_functions:
                result = call_function(name, None, all_functions, local_vars)
                merged[name] = result if result is not None else ""

    try:
        return val.format(**merged)
    except (KeyError, ValueError):
        return val


def resolve_args(val, local_vars, all_functions=None):
    """Resolve placeholders in a value that may be a list or a scalar."""
    if isinstance(val, list):
        return [resolve_value(v, local_vars, all_functions) for v in val]
    return resolve_value(val, local_vars, all_functions)


def eval_condition(condition, local_vars, all_functions=None):
    """Evaluate a condition string that may contain {variable} placeholders."""
    merged = {**state.variables, **local_vars}

    if all_functions:
        for name in re.findall(r'\{(\w+)\}', condition):
            if name not in merged and name in all_functions:
                result = call_function(name, None, all_functions, local_vars)
                merged[name] = result if result is not None else ""

    try:
        return bool(eval(condition.format(**merged), {}, merged))
    except Exception as e:
        r.print(f"[red]ERROR evaluating condition '{condition}': {e}[/red]")
        return False

# ─── Function Registry ────────────────────────────────────────────────────────

def get_functions(data_block, include_begin=False):
    """Return all callable function definitions from a data block."""
    skip = set(state.RESERVED_TOP)
    if include_begin:
        skip.discard("begin")
    return {
        key: val
        for key, val in data_block.items()
        if isinstance(val, list) and key not in skip
    }

# ─── Execution Engine ─────────────────────────────────────────────────────────

def call_function(func_name, args, all_functions, local_vars):
    """Look up and execute a named function, binding any declared parameters."""
    if func_name not in all_functions:
        r.print(f"[red]ERROR: Function '{func_name}' not found.[/red]")
        return None

    body = all_functions[func_name]

    # Collect parameter declarations at the top of the function body
    param_names  = []
    action_start = 0
    for i, item in enumerate(body):
        if isinstance(item, dict) and "param" in item:
            raw = item["param"]
            param_names  = [p.split(":")[0] for p in raw] if isinstance(raw, list) else []
            action_start = i + 1
        elif isinstance(item, list):
            action_start = i + 1
        else:
            action_start = i
            break

    # Bind arguments to parameter names
    func_locals = dict(local_vars)
    if isinstance(args, list):
        for i, name in enumerate(param_names):
            if i < len(args):
                func_locals[name] = args[i]
    elif args is not None and param_names:
        func_locals[param_names[0]] = args

    result = run_actions(body[action_start:], all_functions, func_locals)

    # Unwrap ReturnValue here — the caller just gets a plain value (or None)
    if isinstance(result, ReturnValue):
        return result.value
    return None


def dispatch_action(action, all_functions, local_vars):
    """Run an action that may be a list of steps, a single dict, or a bare string."""
    if isinstance(action, list):
        return run_actions(action, all_functions, local_vars)
    if isinstance(action, dict):
        return run_actions([action], all_functions, local_vars)
    if isinstance(action, str):
        if action in all_functions:
            return call_function(action, None, all_functions, local_vars)
        return resolve_value(action, local_vars, all_functions)
    return None


def run_actions(actions, all_functions, local_vars=None):
    """Execute a list of action dicts, stopping early only on ReturnValue or __exit__."""
    if local_vars is None:
        local_vars = {}

    for action in actions:

        # Bare string → call as a function
        if isinstance(action, str):
            result = call_function(action, None, all_functions, local_vars)
            if result == "__exit__":
                return "__exit__"
            continue

        if not isinstance(action, dict):
            continue

        # Try each key in the action dict
        for key, val in action.items():

            # ── Built-in command ──────────────────────────────────────────────
            if key in BUILTIN_HANDLERS:
                result = BUILTIN_HANDLERS[key](val, all_functions, local_vars)
                if isinstance(result, ReturnValue) or result == "__exit__":
                    return result
                break   # one key per action dict is enough

            # ── Object method call  (e.g. "Player.heal") ─────────────────────
            if "." in key:
                obj_name, func_name = key.split(".", 1)
                if obj_name not in state.loaded_objects:
                    r.print(f"[red]ERROR: Object '{obj_name}' not loaded.[/red]")
                    continue
                obj        = state.loaded_objects[obj_name]
                merged_fns = {**all_functions, **obj["functions"]}
                args       = resolve_args(val, local_vars, all_functions) if val is not None else None
                result     = call_function(func_name, args, merged_fns, local_vars)
                if result == "__exit__":
                    return "__exit__"

            # ── Regular function call ─────────────────────────────────────────
            else:
                args   = resolve_args(val, local_vars, all_functions) if val is not None else None
                result = call_function(key, args, all_functions, local_vars)
                if result == "__exit__":
                    return "__exit__"

    return None