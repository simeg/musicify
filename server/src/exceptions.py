class SpotifyConnectionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class SpotifyOAuthError(Exception):
    def __init__(self, message):
        super().__init__(message)


class EmotionClientError(Exception):
    def __init__(self, message):
        super().__init__(message)
