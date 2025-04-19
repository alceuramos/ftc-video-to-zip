class ItemAccessException(Exception):
    """Custom exception for Item access errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class ItemNotFoundException(Exception):
    """Custom exception for Item not found errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message