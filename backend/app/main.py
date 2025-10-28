import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.api.v1.routers import analytics, auth, departments, employees, projects, reports, timesheets, uploads
from app.core.config import settings
from app.db.base_class import Base
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    yield


app = FastAPI(
    title=settings.SERVER_NAME,
    lifespan=lifespan
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(departments.router, prefix=f"{settings.API_V1_STR}/departments", tags=["departments"])
app.include_router(employees.router, prefix=f"{settings.API_V1_STR}/employees", tags=["employees"])
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(timesheets.router, prefix=f"{settings.API_V1_STR}/timesheets", tags=["timesheets"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(uploads.router, prefix=f"{settings.API_V1_STR}/upload", tags=["uploads"])
app.include_router(reports.router, prefix=f"{settings.API_V1_STR}/reports", tags=["reports"])

# Mount reports directory as static files
app.mount("/reports", StaticFiles(directory="reports"), name="reports")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Employee Productivity API"}