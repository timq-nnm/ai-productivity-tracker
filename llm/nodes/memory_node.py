"""
Memory Node — сохраняет данные в Vector Store после анализа.
Обеспечивает long-term memory для персонализации.
"""
import logging
from llm.graph.state import InsightWorkflowState
from memory.vector_store import vector_store

logger = logging.getLogger(__name__)


async def memory_node(state: InsightWorkflowState) -> InsightWorkflowState:
    """
    Нода памяти: сохраняет рефлексию и инсайт в ChromaDB.
    
    Это позволяет:
    - Искать похожие периоды в будущем
    - Строить контекст для LLM (RAG)
    - Анализировать долгосрочные паттерны
    """
    logger.info(f"[memory_node] Saving to vector store for user {state['user_id']}")

    entry = state["raw_entry"]
    reflection = entry.get("reflection", "")
    date = entry.get("date", "unknown")

    # Сохраняем рефлексию
    if reflection:
        try:
            vector_store.add_reflection(
                user_id=state["user_id"],
                entry_id=state["entry_id"],
                date=date,
                reflection=reflection,
                metadata={
                    "sleep": entry.get("sleep", 0),
                    "energy": entry.get("energy", 0),
                    "motivation": entry.get("motivation", 0),
                },
            )
            logger.debug(f"[memory_node] Reflection saved for date {date}")
        except Exception as e:
            logger.error(f"[memory_node] Failed to save reflection: {e}")

    # Сохраняем инсайт если есть
    insight = state.get("insight")
    if insight:
        try:
            vector_store.add_insight(
                user_id=state["user_id"],
                insight_id=state["entry_id"],
                date=date,
                summary=insight.summary,
                metadata={
                    "mood": insight.mood,
                    "productivity_score": insight.productivity_score,
                    "energy_trend": insight.energy_trend,
                },
            )
            logger.debug(f"[memory_node] Insight saved for date {date}")
        except Exception as e:
            logger.error(f"[memory_node] Failed to save insight: {e}")

    return state
