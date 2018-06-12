class SpotifyConnectionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class EmotionAPIConnectionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class EmotionAPIResponseError(Exception):
    def __init__(self, message):
        super().__init__(message)
