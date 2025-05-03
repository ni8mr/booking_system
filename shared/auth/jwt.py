from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi import HTTPException, status

class User(BaseModel):
    sub: str
    role: str

def verify_jwt_token(token: str, public_key: str) -> User:
    try:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        user = User(sub=payload.get("sub"), role=payload.get("role"))
        if not user.sub or not user.role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")