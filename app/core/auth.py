from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt import decode_access_token

security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    decoded_token = decode_access_token(token)
    if decoded_token is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return decoded_token
