from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.auth.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    try:
        hashed_pw = hash_password(password)

        new_user = User(
            username=username,
            hashed_password=hashed_pw
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "User created successfully"}


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }