class AethraAPIError(Exception):
    """Base exception for ConvoLens API errors."""

    def __init__(self, message: str, status_code: int = None, details: dict = None):
        """
        Initialize the base exception.

        Args:
            message (str): The error message.
            status_code (int, optional): HTTP status code associated with the error.
            details (dict, optional): Additional details about the error.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def __str__(self):
        base = f"{self.message}"
        if self.status_code:
            base += f" (Status Code: {self.status_code})"
        if self.details:
            base += f" | Details: {self.details}"
        return base


class InvalidAPIKeyError(AethraAPIError):
    """Raised when the API key is invalid."""

    def __init__(self, message="Invalid API Key.", status_code=403, details=None):
        super().__init__(message, status_code, details)


class InsufficientCreditsError(AethraAPIError):
    """Raised when the user has insufficient credits."""

    def __init__(self, message="Insufficient credits.", status_code=403, details=None):
        super().__init__(message, status_code, details)


class AnalysisError(AethraAPIError):
    """Raised when analysis fails."""

    def __init__(self, message="Analysis failed.", status_code=500, details=None):
        super().__init__(message, status_code, details)
