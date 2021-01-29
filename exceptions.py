class Plugboard_Error(Exception):
    def __init__(self, message):
        super().__init__(message)


class Rotor_Error(Exception):
    def __init__(self, message):
        super().__init__(message)


class Enigma_Error(Exception):
    def __init__(self, message):
        super().__init__(message)
