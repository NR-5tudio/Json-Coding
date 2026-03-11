import json

# ─── JSON Loader ──────────────────────────────────────────────────────────────

class nrjson:
    @staticmethod
    def load(path):
        with open(path) as f:
            return json.load(f)
