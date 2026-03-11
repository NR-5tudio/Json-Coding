# ─── Global State ─────────────────────────────────────────────────────────────

variables      = {}   # global variable scope
loaded_objects = {}   # { "Player": { "functions": {...} } }

# ─── Constants ────────────────────────────────────────────────────────────────

# Top-level keys that are not callable functions
RESERVED_TOP = {"begin", "update", "include", "window"}
