from fastapi import FastAPI
from app.routes import basic_route, image_routes
from app.db.database import init_db

app = FastAPI(title="Image Processing Backend")

# Inicializa o banco na inicialização do app
@app.on_event("startup")
def on_startup():
    init_db()

# Rotas
app.include_router(basic_route.router)
app.include_router(image_routes.router)

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}
