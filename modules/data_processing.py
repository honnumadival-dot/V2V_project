class DataFilter:
    def __init__(self):
        self.prev = None

    def smooth(self, value):
        if self.prev is None:
            self.prev = value
            return value
        filtered = (self.prev * 0.6) + (value * 0.4)
        self.prev = filtered
        return filtered