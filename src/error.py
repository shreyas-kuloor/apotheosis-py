class TokenQuotaReachedError(Exception):
    def __init__(self, message="Monthly token quota reached"):
        self.message = message
        super().__init__(self.message)


class UnexpectedNetworkError(Exception):
    def __init__(self, message="An unexpected status code or network error occurred"):
        self.message = message
        super().__init__(self.message)
