from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..utils.security import verify_password, get_password_hash, create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
    except Exception as exc:  # noqa: B902
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register(email: str, password: str, full_name: str | None = None, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=email, hashed_password=get_password_hash(password), full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}
