from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.auth import register, login
from app.api.routes import user_routes
from app.db.database import Base, engine
from app.api.routes.predict_routes import router as predict_router
from app.api.routes.predictions_routes import router as predictions_router
from fastapi.responses import HTMLResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI API con Registro de Usuario")

# Mount static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route to serve the main HTML page
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html") as f:
        return f.read()

# Incluir routers
app.include_router(register.router, prefix="/auth", tags=["Auth"])
app.include_router(login.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])
app.include_router(predictions_router, prefix="/predictions", tags=["Prediction History"])
