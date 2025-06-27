from fastapi import HTTPException, status


class PlanogramNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="no planogram found for the user")

class RunAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="another run exists with same name")

class RunDeleteNotAuthorized(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="user is not authorized to delete the run")
        
class ScorecardNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="no scorecard found for the planogram")