"""
LangGraph Workflow для обработки daily entry.

Pipeline:
  validate → parse → analysis → memory → END
       ↓ (fail)
      END (with error)
"""
import logging
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from llm.graph.state import InsightWorkflowState
from llm.nodes.validate_node import validate_node
from llm.nodes.parse_node import parse_node
from llm.nodes.analysis_node import analysis_node
from llm.nodes.memory_node import memory_node

logger = logging.getLogger(__name__)


def should_continue_after_validation(state: InsightWorkflowState) -> str:
    if state.get("validation_passed"):
        return "parse"
    logger.warning(f"[workflow] Validation failed: {state.get('validation_errors')}")
    return END


def should_continue_after_parse(state: InsightWorkflowState) -> str:
    if state.get("error"):
        return END
    return "analysis"


class InsightWorkflow:
    """
    LangGraph граф для генерации инсайтов.
    
    Демонстрирует:
    - Stateful workflow
    - Conditional edges
    - Async nodes
    - Error handling
    - Memory integration
    """

    def __init__(self):
        self.graph: CompiledStateGraph = self._build_graph()

    def _build_graph(self) -> CompiledStateGraph:
        workflow = StateGraph(InsightWorkflowState)

        # Ноды
        workflow.add_node("validate", validate_node)
        workflow.add_node("parse", parse_node)
        workflow.add_node("analysis", analysis_node)
        workflow.add_node("memory", memory_node)

        # Точка входа
        workflow.set_entry_point("validate")

        # Conditional edge после валидации
        workflow.add_conditional_edges(
            "validate",
            should_continue_after_validation,
            {"parse": "parse", END: END},
        )

        # Conditional edge после парсинга
        workflow.add_conditional_edges(
            "parse",
            should_continue_after_parse,
            {"analysis": "analysis", END: END},
        )

        # После анализа — сохраняем в memory
        workflow.add_edge("analysis", "memory")
        workflow.add_edge("memory", END)

        return workflow.compile()

    async def run(self, entry_data: dict, user_id: int, entry_id: int) -> dict:
        """Запустить workflow для обработки entry."""
        initial_state: InsightWorkflowState = {
            "user_id": user_id,
            "entry_id": entry_id,
            "raw_entry": entry_data,
            "parsed_tasks": None,
            "validation_passed": False,
            "validation_errors": [],
            "insight": None,
            "insight_saved": False,
            "error": None,
        }

        logger.info(f"[workflow] Starting for user={user_id}, entry={entry_id}")
        result = await self.graph.ainvoke(initial_state)
        logger.info(
            f"[workflow] Completed: insight={'yes' if result.get('insight') else 'no'}, "
            f"error={result.get('error')}"
        )
        return result
