
from fastapi import FastAPI
from app.auth import register
from app.auth import login
from app.api import user_routes
from app.db.database import Base, engine


# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI API con Registro de Usuario")

# Include routes
app.include_router(register.router)
app.include_router(login.router)
app.include_router(user_routes.router)
