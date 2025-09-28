import threading
import time

_lock = threading.Lock()
_last_ts = 0
_counter = 0


def generate_id() -> str:
    """
    Генерирует уникальный строковый ID без использования UUID/random/sequence.
    """
    global _last_ts, _counter
    with _lock:
        ts = int(time.time() * 1000)  # миллисекунды
        if ts == _last_ts:
            _counter += 1
        else:
            _last_ts = ts
            _counter = 0
        return f"{ts}{_counter:03d}"  # строка вида 1695821234567001
