from fastapi import FastAPI
from database import engine, Base
from router import router
from auth import auth_router
from middleware import *


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.add_middleware(TenantMiddleware)


app.include_router(auth_router, prefix="/auth")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "LMS tizimiga xush kelibsiz"}
