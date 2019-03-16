class LimitedMemory(list):
    def __init__(self, size):
        self.size = size

    def append(self, item):
        if len(self) >= self.size:
            del self[0]
        super().append(item)
