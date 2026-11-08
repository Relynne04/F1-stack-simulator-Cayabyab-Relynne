"""Queue object: First In, First Out (FIFO)."""


class Queue:
    def __init__(self, items=None):
        self.items = list(items or [])  # Copy previous values into this object.
        # items[0] is the FRONT (oldest value); items[-1] is the REAR (newest).

    def enqueue(self, value):
        self.items.append(value)        # New values join at the rear.

    def dequeue(self):
        # pop(0) removes the FRONT element only, which gives FIFO behavior.
        # (pop() without an index would remove the rear and act like a stack.)
        return self.items.pop(0) if self.items else None

    def peek(self):
        return self.items[0] if self.items else None   # Look at the front only.

    def front(self):
        return self.items[0] if self.items else None

    def rear(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return not self.items

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()
