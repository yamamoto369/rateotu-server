class WebsocketClientError(Exception):
    """
    Custom WebSocket exception class.
    """

    def __init__(self, code):
        super().__init__(code)
        self.code = code
