from typing import Any, Optional

import reflex as rx
from langchain_core.messages import HumanMessage

from aitalab.states.prompt_template import PromptTemplateState
from aitalab.states.datasource import DataSourceState
from aitalab.states.tool import Tool
from aita.agent.base import AitaAgent
from aita.agent.factory import AgentFactory
from aita.datasource.base import DataSource


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Intros": [],
}


class ChatState(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    current_model: str

    current_datasource: str

    current_prompt_template: str = ""

    _current_agent: AitaAgent = None

    current_tools: list[Tool] = []

    current_tool: Tool = None

    def set_current_tool_arg(self, tool_id: str, key: str, value: str):
        tool = next(filter(lambda x: x.id == tool_id, self.current_tools), None)
        tool.args[key] = value

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    def create_agent(self, datasource: DataSource, prompt: str):
        agent_type = ""
        if self.current_datasource:
            agent_type = "sql"
        self._current_agent = AgentFactory.create_agent(
            agent_type,
            model_id=self.current_model,
            datasource=datasource,
            prompt_context=prompt,
        )

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        # Get the datasource
        if self.current_datasource:
            datasource = DataSourceState.connect(self.current_datasource)
            catalog = datasource.get_metadata()
            target = {
                "catalog": catalog,
                "question": question,
                "db_id": "",
                "path_db": "/Users/haoxu/dev/aita/DAIL-SQL/dataset/spider/database/concert_singer/concert_singer.sqlite",
                "query": ""
            }

            # build prompt
            prompt_template_state = await self.get_state(PromptTemplateState)
            prompt_template = next(filter(lambda x: x.prompt_template_name == self.current_prompt_template,
                                          prompt_template_state.prompt_templates), None)
            prompt = PromptTemplateState.build_prompt(prompt_template, self.current_model, target)
        else:
            datasource = None
            prompt = ""

        # create agent
        # if self._current_agent is None:
        #     self._current_agent = SqlAgent(datasource, model_id=self.current_model, prompt_context=prompt)
        self.create_agent(datasource, prompt)

        async for value in self.aita_process_question(question):
            yield value

    async def aita_process_question(self, question: str):
        """Get the response from the API.

        Args:
            question: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        events = self._current_agent.chat(question, display=False)
        chat_state = self._current_agent.get_current_state()
        if chat_state and chat_state.next:
            # having an action to execute
            for tool_call in self._current_agent.get_current_tool_calls():
                tool = Tool(id=tool_call["id"], name=tool_call["name"], args=tool_call["args"])
                self.current_tools.append(tool)

            # Add the tool call to the answer
            self.chats[self.current_chat][-1].answer += f"Confirm to run the tool in the panel"

            for event in events:
                message = event["messages"]
                if not message:
                    continue
                if isinstance(message, list):
                    message = message[-1]
                if not isinstance(message, HumanMessage):
                    self.chats[self.current_chat][-1].answer += message.content
                yield
        else:
            # No action to execute
            for event in events:
                self.chats[self.current_chat][-1].answer += event.content
                yield

        # Toggle the processing flag.
        self.processing = False