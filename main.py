from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.config import AppSettings
from app.schemas import QueryRequest, QueryResponse
from app.rag_service import RAGService


settings = AppSettings()
rag_service = RAGService(settings=settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    服务生命周期：
    启动时初始化（加载索引/模型）。
    """
    rag_service.startup()
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)


@app.get("/health")
def health():
    """探活接口：返回 readiness 状态"""
    return rag_service.health()


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    """
    问答接口：
    - 接收 question
    - 调用 rag_service.ask
    - 返回答案及证据
    """
    if not rag_service.is_ready:
        raise HTTPException(status_code=503, detail="Service not ready")

    result = rag_service.ask(req.question, top_k=req.top_k)
    return result