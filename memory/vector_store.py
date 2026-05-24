"""
Vector Store для хранения и поиска embeddings.
Использует ChromaDB как локальное векторное хранилище.

Позволяет:
- Хранить рефлексии и инсайты как embeddings
- Искать похожие периоды (similarity search)
- Строить long-term memory пользователя
"""
import logging
from typing import Optional
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

# Путь к локальному ChromaDB
CHROMA_PATH = "./chroma_db"


class VectorStore:
    """
    Обёртка над ChromaDB для хранения embeddings.
    
    Коллекции:
    - reflections: ежедневные рефлексии пользователей
    - insights: сгенерированные AI инсайты
    - patterns: выявленные паттерны поведения
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH,
            settings=Settings(anonymized_telemetry=False),
        )
        self._init_collections()

    def _init_collections(self):
        """Инициализировать коллекции ChromaDB."""
        self.reflections = self.client.get_or_create_collection(
            name="reflections",
            metadata={"description": "Daily reflections from users"},
        )
        self.insights = self.client.get_or_create_collection(
            name="insights",
            metadata={"description": "AI-generated insights"},
        )
        self.patterns = self.client.get_or_create_collection(
            name="patterns",
            metadata={"description": "Behavioral patterns"},
        )
        logger.info("ChromaDB collections initialized")

    def add_reflection(
        self,
        user_id: int,
        entry_id: int,
        date: str,
        reflection: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """Добавить рефлексию в векторное хранилище."""
        doc_id = f"user_{user_id}_entry_{entry_id}"
        meta = {
            "user_id": user_id,
            "entry_id": entry_id,
            "date": date,
            **(metadata or {}),
        }

        self.reflections.upsert(
            ids=[doc_id],
            documents=[reflection],
            metadatas=[meta],
        )
        logger.debug(f"Reflection added: {doc_id}")

    def add_insight(
        self,
        user_id: int,
        insight_id: int,
        date: str,
        summary: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """Добавить инсайт в векторное хранилище."""
        doc_id = f"user_{user_id}_insight_{insight_id}"
        meta = {
            "user_id": user_id,
            "insight_id": insight_id,
            "date": date,
            **(metadata or {}),
        }

        self.insights.upsert(
            ids=[doc_id],
            documents=[summary],
            metadatas=[meta],
        )
        logger.debug(f"Insight added: {doc_id}")

    def search_similar_reflections(
        self,
        query: str,
        user_id: int,
        n_results: int = 5,
    ) -> list[dict]:
        """
        Найти похожие рефлексии пользователя.
        
        Используется для:
        - Поиска похожих периодов выгорания
        - Контекста для LLM (RAG)
        - Анализа паттернов
        """
        results = self.reflections.query(
            query_texts=[query],
            n_results=n_results,
            where={"user_id": user_id},
        )

        if not results["documents"] or not results["documents"][0]:
            return []

        raw_metadatas: list = results["metadatas"] or []  # type: ignore[assignment]
        raw_distances: list = results.get("distances") or []  # type: ignore[assignment]
        similar = []
        for i, doc in enumerate(results["documents"][0]):
            similar.append({
                "text": doc,
                "metadata": raw_metadatas[0][i] if raw_metadatas else {},
                "distance": raw_distances[0][i] if raw_distances else None,
            })

        return similar

    def search_similar_insights(
        self,
        query: str,
        user_id: int,
        n_results: int = 3,
    ) -> list[dict]:
        """Найти похожие инсайты пользователя."""
        results = self.insights.query(
            query_texts=[query],
            n_results=n_results,
            where={"user_id": user_id},
        )

        if not results["documents"] or not results["documents"][0]:
            return []

        raw_metadatas: list = results["metadatas"] or []  # type: ignore[assignment]
        return [
            {
                "text": doc,
                "metadata": raw_metadatas[0][i] if raw_metadatas else {},
            }
            for i, doc in enumerate(results["documents"][0])
        ]

    def get_user_context(self, user_id: int, query: str) -> str:
        """
        Получить контекст из памяти для LLM (RAG pattern).
        
        Возвращает строку с релевантными прошлыми рефлексиями и инсайтами.
        """
        similar_reflections = self.search_similar_reflections(query, user_id, n_results=3)
        similar_insights = self.search_similar_insights(query, user_id, n_results=2)

        context_parts = []

        if similar_reflections:
            context_parts.append("Похожие прошлые периоды:")
            for r in similar_reflections:
                date = r["metadata"].get("date", "unknown")
                context_parts.append(f"  [{date}]: {r['text'][:200]}")

        if similar_insights:
            context_parts.append("\nПрошлые инсайты:")
            for ins in similar_insights:
                date = ins["metadata"].get("date", "unknown")
                context_parts.append(f"  [{date}]: {ins['text'][:200]}")

        return "\n".join(context_parts) if context_parts else ""


# Singleton instance
vector_store = VectorStore()
