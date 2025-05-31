from collections import deque
from collections import deque
from typing import Deque, Tuple

class RopeBuffer:
    def __init__(self, capacity: int = 1024):
        self.stack: Deque[Tuple[str, str, float]] = deque(maxlen=capacity)

    def push(self, gid_from: str, gid_to: str, weight: float):
        self.stack.append((gid_from, gid_to, weight))

rope_buffer = RopeBuffer()
