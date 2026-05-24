"""
Analysis Node — генерирует AI инсайт через structured LLM output.
"""
import logging
from llm.graph.state import InsightWorkflowState
from llm.client import LLMClient

logger = logging.getLogger(__name__)
_llm = LLMClient()


async def analysis_node(state: InsightWorkflowState) -> InsightWorkflowState:
    """
    Нода анализа: генерирует DailyInsightSchema через LLM.
    
    Input: raw_entry + parsed_tasks
    Output: insight (DailyInsightSchema)
    """
    logger.info(f"[analysis_node] Generating insight for user {state['user_id']}")

    entry = state["raw_entry"]

    # Обогащаем данные результатами парсинга
    parsed = state.get("parsed_tasks")
    if parsed is not None:
        entry = {
            **entry,
            "tasks_done": ", ".join(parsed.tasks_completed) or entry.get("tasks_done", ""),
        }

    try:
        insight = await _llm.generate_daily_insight(entry)
        logger.info(
            f"[analysis_node] Insight generated: mood={insight.mood}, "
            f"score={insight.productivity_score}"
        )
        return {**state, "insight": insight}
    except Exception as e:
        logger.error(f"[analysis_node] Error: {e}")
        return {**state, "error": str(e)}
