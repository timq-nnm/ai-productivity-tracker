"""
Parse Node — первый шаг в LangGraph pipeline.
Парсит свободный текст рефлексии в структурированные данные.
"""
import logging
from llm.graph.state import InsightWorkflowState
from llm.client import LLMClient

logger = logging.getLogger(__name__)
_llm = LLMClient()


async def parse_node(state: InsightWorkflowState) -> InsightWorkflowState:
    """
    Нода парсинга: извлекает структурированные данные из текста рефлексии.
    
    Input: raw_entry с reflection текстом
    Output: parsed_tasks с задачами, настроением и т.д.
    """
    logger.info(f"[parse_node] Processing entry for user {state['user_id']}")

    reflection = state["raw_entry"].get("reflection", "")

    if not reflection:
        logger.warning("[parse_node] Empty reflection, skipping parse")
        return {**state, "parsed_tasks": None}

    try:
        parsed = await _llm.parse_tasks_from_text(reflection)
        logger.info(f"[parse_node] Parsed {len(parsed.tasks_completed)} tasks")
        return {**state, "parsed_tasks": parsed}
    except Exception as e:
        logger.error(f"[parse_node] Error: {e}")
        return {**state, "parsed_tasks": None, "error": str(e)}
