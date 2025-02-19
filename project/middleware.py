
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Depends, HTTPException
from starlette.responses import RedirectResponse
from database import SessionLocal, get_db
from models import User
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from models import User as UserModel
from sqlalchemy.orm import Session
from database import SessionLocal

SECRET_KEY = "mysecretkey"

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = request.headers.get("tenant-id")
        # request.state.tenant_id = int(tenant_id) if tenant_id else None
        if not tenant_id:
            pass
        else:
            return int(tenant_id)

        db = SessionLocal()
        request.state.db = db
        response = await call_next(request)
        db.close()
        return response



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("username")
        role: str = payload.get("role")
        branch: int = payload.get("branch")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        return {"username": username, "role": role, "branch": branch}
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
