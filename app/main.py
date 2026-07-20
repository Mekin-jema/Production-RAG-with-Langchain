from langsmith.schemas import ListedPromptCommit
import time
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from langsmith import traceable
from dotenv import load_dotenv

from app.config import get_settings
from app.models import (
    ChatRequest,ChatResponse,HealthResponse,MetricsResponse,ErrorResponse
)
from app.security import SecurePipeline
from app.cache import ResponseCache
from app.monitering import get_logger,MetricsCollector,RequestTimer
from app.agent import ProductionAgent

load_dotenv()

cache:ResponseCache=None
metrics:MetricsCollector=None
agent:ProductionAgent=None
security:SecurePipeline=None
logger=get_logger()


#  ===============Lifespan (startup or shutdwon)===================
@asynccontextmanager
async def lifespan(apop:FastAPI):
    """ Initialize all components on startup, clean up on shutdown.
        This is the modern FastAPI patter (replaces @app.on_event)

    """
    global security,cache,metrics,agent
    settings=get_settings()
    logger.info("Starting production API...",extra={"extra_data":{
        "environment":settings.app_env,
        "primary_model":settings.primary_model,
        "tracing_eanables":settings.langsmith_tracing_v2,
    }})

    # Initialize components

    security=SecurePipeline()
    cache=ResponseCache(ttl_seconds=settings.cache_ttl_seconds)
    metrics=MetricsCollector()
    agent=ProductionAgent()
    logger.info("All Componets initialized. Ready to serve requests.")

    yield # Appp is running
    logger.info("Shutting down....",extra={
        "extra_data":{
            metrics.summary
        }
    })


    
# ========= Rate Limmter setup =========
limiter= Limiter(key_func=get_remote_address)

# ======FastAPI App===
app=FastAPI(
    title="Production Langraph API",
    description="A Production-ready chat API with security ,caching , and observablility.",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter=limiter



# =============Exception Handlers============
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded(request:Request,exc:RateLimitExceeded):
    """ Handle rate limit exceeded exceptions."""
    logger.warning("Rate limit exceeded",extra={
        "extra_data":{
            "request_id":request.headers.get("x-request-id"),
            "ip":request.client.host,
            "limit":exc.limiter.limit,
            "retry_after":exc.retry_after,
        }
    })
    return JSONResponse(
        status_code=429,
        content=ErrorResponse(
            error="Rate limit exceeded",
            detail=f"You have exceeded the rate limit. Please try again in {exc.retry_after} seconds.",
            request_id=request.headers.get("x-request-id"),
        ).dict()
    )


# ============================================
# ENDPOINTS
#=============================================
@app.post("/chat",response_model=ChatResponse)
@limiter.limit(get_settings().rate_limit)
@traceable(name="chat_endpoint ")
async def chat(requst:Request,body:ChatRequest):
    """ 
    Main chat endpoint.
    Flow:
    1. Security check(injection +PII  masking)
    2. Cache Lookup
    3. Langrgraph agent invoke (if cache miss)
    4. Output valiation
    5. Cache store
    6. Return repsonse
    """


    
    



