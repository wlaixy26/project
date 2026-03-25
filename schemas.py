from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """
    /query 的请求体。
    你如果要支持“动态本地文件”，就加 file_path 字段即可（见后续你可能的扩展）。
    """
    question: str = Field(..., min_length=1, description="用户问题")
    top_k: Optional[int] = Field(None, description="可选：覆盖默认 top_k")


class SourceDoc(BaseModel):
    """证据片段的结构化返回（方便前端展示/调试）"""
    page: Optional[int] = None
    source: Optional[str] = None
    content_preview: str = ""


class QueryResponse(BaseModel):
    """/query 的响应体"""
    answer: str
    retrieval_query: str = ""
    sources: List[SourceDoc] = []
    debug: Dict[str, Any] = {}