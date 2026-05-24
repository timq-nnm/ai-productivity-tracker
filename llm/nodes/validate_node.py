"""
Validate Node — проверяет данные перед отправкой в LLM.
"""
import logging
from llm.graph.state import InsightWorkflowState

logger = logging.getLogger(__name__)


async def validate_node(state: InsightWorkflowState) -> InsightWorkflowState:
    """
    Нода валидации: проверяет корректность данных entry.
    
    Проверяет:
    - Наличие обязательных полей
    - Диапазоны значений (0-10)
    - Наличие рефлексии
    """
    logger.info(f"[validate_node] Validating entry for user {state['user_id']}")

    entry = state["raw_entry"]
    errors = []

    # Проверка обязательных полей
    required_fields = ["sleep", "energy", "clarity", "motivation"]
    for field in required_fields:
        if field not in entry:
            errors.append(f"Missing field: {field}")
        elif not (0 <= entry[field] <= 10):
            errors.append(f"Field {field}={entry[field]} out of range [0, 10]")

    # Проверка рефлексии (мягкая — рефлексия опциональна для утреннего чек-ина)
    reflection = entry.get("reflection", "")
    if reflection and len(reflection.strip()) < 3:
        errors.append("Reflection is too short")

    if errors:
        logger.warning(f"[validate_node] Validation failed: {errors}")
        return {**state, "validation_passed": False, "validation_errors": errors}

    logger.info("[validate_node] Validation passed")
    return {**state, "validation_passed": True, "validation_errors": []}
