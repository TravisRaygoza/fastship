from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from app.api.router import master_router
from app.core.exceptions import add_exception_handlers
from app.database.session import create_db_tables
from app.worker.tasks import add_log



@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield

# Create FastAPI app with lifespan handler
app = FastAPI(lifespan=lifespan_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add all endpoints
app.include_router(router=master_router)

# Add custom exception handlers
add_exception_handlers(app)

# Add custom middleware to log request processing time
@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start = perf_counter()

    response: Response = await call_next(request)

    end = perf_counter()
    time_taken = round(end - start, 2)

    add_log.delay(f"Request: {request.method} {request.url} ({response.status_code}) completed in {time_taken} seconds.")  # noqa: F821
    
    return response


# Server Running status 
@app.get("/")
def read_root():
    return {"detail": "Server is running..."}

# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )