class ConvoLensAPIError(Exception):
    """Base exception for ConvoLens API errors."""
    pass

class InvalidAPIKeyError(ConvoLensAPIError):
    """Raised when the API key is invalid."""
    pass

class InsufficientCreditsError(ConvoLensAPIError):
    """Raised when the user has insufficient credits."""
    pass

class AnalysisError(ConvoLensAPIError):
    """Raised when analysis fails."""
    pass
