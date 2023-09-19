import uvicorn
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


# append CORS headers to all responses
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(
    budget_breakdown_router, prefix="/budget-breakdown", tags=["budget-breakdown"]
)

# if __name__ == "__main__":
#     uvicorn.run(app, port=8000, host="0.0.0.0")
