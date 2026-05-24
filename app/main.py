from fastapi import FastAPI, Depends
from app.db.database import Base, engine
from app.api.upload import router as upload_router
from app.auth.routes import router as auth_router
from app.auth.security import get_current_user

app = FastAPI(title="DocuMind AI Backend")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, tags=["Authentication"])
app.include_router(upload_router, tags=["Upload"])

try:
    from app.api.chat import router as chat_router
    app.include_router(chat_router, tags=["Chat"])
except Exception as e:
    print(f"Warning: failed to include chat router: {e}")


@app.get("/")
def home():
    return {"message": "Backend running with PostgreSQL"}

@app.get("/me")
def read_user(username: str = Depends(get_current_user)):
    return {"logged_in_user": username}