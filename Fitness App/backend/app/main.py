from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, users, workouts, assignments, progress, health_tips
from app.db.database import engine, Base


try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create tables. Make sure database is running and connection is correct.")
    print(f"Error: {e}")

app = FastAPI(title="FitSphere API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(assignments.router)
app.include_router(progress.router)
app.include_router(health_tips.router)

@app.get("/")
def root():
    return {"message": "FitSphere API is running"}

@app.get("/api")
def api_info():
    return {
        "message": "FitSphere API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth",
            "users": "/api/users",
            "workouts": "/api/workouts",
            "assignments": "/api/assignments",
            "progress": "/api/progress",
            "health-tips": "/api/health-tips"
        }
    }

