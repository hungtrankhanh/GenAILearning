from typing import Dict, Any, List, Optional
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult


class AgentCallbackHandler(BaseCallbackHandler):
    async def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM starts running.

        **ATTENTION**: This method is called for non-chat models (regular LLMs). If
            you're implementing a handler for a chat model,
            you should use on_chat_model_start instead.
        """
        print(f"***Prompt to LLM ***\n{prompts[0]}")
        print("******************")
    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM ends running."""
        print(f"***response from LLM ***\n{response.generations[0][0].text}")
        print("******************")