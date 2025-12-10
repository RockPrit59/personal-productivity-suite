# timer.py
import time
import threading

class TimerStopwatch:
    def __init__(self):
        self._running = False
        self._start_time = None
        self._elapsed = 0.0
        self._lock = threading.Lock()

    def start(self):
        with self._lock:
            if not self._running:
                self._running = True
                self._start_time = time.time()

    def stop(self):
        with self._lock:
            if self._running:
                self._elapsed += time.time() - self._start_time
                self._running = False

    def reset(self):
        with self._lock:
            self._running = False
            self._start_time = None
            self._elapsed = 0.0

    def elapsed(self):
        with self._lock:
            if self._running:
                return self._elapsed + (time.time() - self._start_time)
            return self._elapsed

    def countdown(self, seconds: int, tick=None):
        """Run a countdown in a background thread. `tick` is an optional callback(seconds_left)."""
        try:
            seconds = int(seconds)
        except Exception:
            raise ValueError("Invalid seconds")

        def run(cd):
            while cd > 0:
                if tick:
                    tick(cd)
                time.sleep(1)
                cd -= 1
            if tick:
                tick(0)

        threading.Thread(target=run, args=(seconds,), daemon=True).start()
