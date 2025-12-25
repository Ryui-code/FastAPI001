from fastapi import FastAPI
from fstsite.admin.routes import router as admin_routes
app = FastAPI()

app.include_router(admin_routes)