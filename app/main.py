from fastapi import FastAPI
from .routes import org_routes, admin_routes

app = FastAPI(title="Organization Management Service", version="1.0.0")

app.include_router(org_routes.router)
app.include_router(admin_routes.router)

@app.get("/")
async def root():
    return {"status": "ok", "service": "org-management", "version": "1.0.0"}
