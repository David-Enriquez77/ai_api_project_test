from fastapi import FastAPI
from app.auth import register, login
from app.api.routes import user_routes
from app.db.database import Base, engine
from app.api.routes.predict_routes import router as predict_router

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="AI API con Registro de Usuario")

# Include routes
app.include_router(register.router, prefix="/auth", tags=["Auth"])
app.include_router(login.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])
