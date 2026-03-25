import re
from typing import List, Dict, Any, Optional

from langchain_core.documents import Document


class RAGService:
    """
    RAG 核心业务层：
    - 负责：清洗问题 -> 检索 -> 拼上下文 -> 调用LLM -> 组装返回
    API层(main.py)只负责接HTTP，不碰RAG细节。
    """

    def __init__(self, settings):
        self.settings = settings

        # 资源：向量库/检索器/LLM 这些都在 startup() 初始化
        self.vectorstore = None
        self.llm = None
        self.is_ready = False

    def startup(self) -> None:
        """
        服务启动时初始化资源（加载/建索引/加载模型）。
        这里是你把 download.py 的“加载与准备部分”搬过来的位置。
        """
        # TODO: 1) 加载/构建向量库
        # TODO: 2) 加载 LLM（pipeline + HuggingFacePipeline）
        # TODO: 3) 初始化 retriever
        #
        # 由于这里是骨架示例：先留空，确保代码结构完整可运行。
        self.is_ready = True

    def health(self) -> dict:
        """健康检查：用于运维探活"""
        return {
            "ready": self.is_ready,
            "index_loaded": self.vectorstore is not None,
            "llm_loaded": self.llm is not None,
        }

    def normalize_query(self, q: str) -> str:
        """
        避免“问题污染”（你之前遇到的问题就是：日志残留/多轮拼接污染了 query）
        这一步的目标是：只保留用户真实问题主体。
        """
        q = q.strip()
        if "问题:" in q:
            q = q.split("问题:")[-1].strip()

        # 截断掉你调试输出中可能混进来的片段
        cut_markers = ["正在检索并生成答案", "检索查询：", "=== 调试", "答案：", "发生错误:"]
        for m in cut_markers:
            if m in q:
                q = q.split(m)[0].strip()

        q = re.sub(r"\s+", " ", q).strip(" ：:\t\r\n")
        return q

    def rewrite_query_for_retrieval(self, query: str) -> str:
        """
        通用检索改写（按意图追加锚词）。
        目的：让向量/BM25更容易召回“定义/年份/别名/原因”类的句子。
        """
        q = query.strip()

        if re.search(r"(哪一年|哪年|何时|什么时候|年份|提出时间|发表时间)", q):
            return f"{q} 提出 发表 首次 年份 时间 论文 文献"

        if re.search(r"(又被称作|又称|也称|别称|简称|全称|叫做|称作)", q):
            return f"{q} 又称 也称 别称 被称为 通常称为 叫做"

        if re.search(r"(是什么|什么是|定义|概念|含义)", q):
            return f"{q} 定义 概念 内涵 外延 核心特征 分类 方法 适用场景"

        if re.search(r"(为什么|原因|为何|机制)", q):
            return f"{q} 原因 机制 影响因素 作用路径 证据"

        return f"{q} 关键点 相关解释"

    def retrieve(self, retrieval_query: str, top_k: int) -> List[Document]:
        """
        检索阶段（骨架）。
        你需要在这里接入：
        - vectorstore.similarity_search...
        - 或 bm25
        - 或 hybrid + rerank
        """
        # TODO: 用你的实际检索逻辑替换下面占位
        return []

    def generate(self, question: str, docs: List[Document]) -> str:
        """
        生成阶段（骨架）。
        你需要在这里接入：
        - 你的 PromptTemplate
        - 你的 llm.invoke(...)
        """
        # TODO: 用你的实际生成逻辑替换下面占位
        return "我不知道"

    def ask(self, question: str, top_k: Optional[int] = None) -> Dict[str, Any]:
        """
        完整问答链路：
        1) 清洗问题
        2) 检索query改写
        3) 检索拿到 docs
        4) LLM 生成答案
        5) 返回结构化结果（答案 + sources + debug）
        """
        top_k = top_k or self.settings.top_k

        clean_q = self.normalize_query(question)
        retrieval_q = self.rewrite_query_for_retrieval(clean_q)

        docs = self.retrieve(retrieval_q, top_k=top_k)
        answer = self.generate(clean_q, docs)

        sources = []
        for d in docs:
            meta = d.metadata or {}
            sources.append({
                "page": meta.get("page"),
                "source": meta.get("source"),
                "content_preview": (d.page_content or "")[:220].replace("\n", " "),
            })

        return {
            "answer": answer,
            "retrieval_query": retrieval_q,
            "sources": sources,
            "debug": {
                "clean_query": clean_q,
                "retrieved_count": len(docs),
            },
        }