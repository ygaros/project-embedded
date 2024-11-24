class PWMLEDMOCK:
    def __init__(self, pin: int):
        self.value = 0
        self.pin = pin
