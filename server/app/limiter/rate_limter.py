from time import time

_RATE_LIMIT_STORE = {}

SHORT_WINDOW = 600
SHORT_LIMIT = 2

LONG_WINDOW = 43200
LONG_LIMIT = 4


def rate_limit(key: str):
    now = time()
    requests = _RATE_LIMIT_STORE.get(key, [])

    requests = [t for t in requests if now - t < LONG_WINDOW]
    short = [t for t in requests if now - t < SHORT_WINDOW]

    if len(short) >= SHORT_LIMIT:
        return False, "Too many submissions. Please wait 10 minutes."

    if len(requests) >= LONG_LIMIT:
        return False, "Submission limit reached for today."

    requests.append(now)
    _RATE_LIMIT_STORE[key] = requests
    return True, None
