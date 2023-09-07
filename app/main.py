from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.budget_breakdown.router import router as budget_breakdown_router

app = FastAPI()

#  allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(
    budget_breakdown_router, prefix="/budget-breakdown", tags=["budget-breakdown"]
)
