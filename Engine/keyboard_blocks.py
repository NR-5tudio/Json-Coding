import keyboard

def is_key_down(value, all_functions, local_vars):
    from Engine.engine import ReturnValue
    
    return ReturnValue(keyboard.is_pressed(value))

Keyboard = {
    "is_key_down": is_key_down
}