from fastapi import status

class ServerException(Exception):
    def __init__(self, message: str, http_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.http_code = http_code
        super().__init__(self.message)