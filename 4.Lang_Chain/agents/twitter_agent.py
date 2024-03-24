from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools import get_profile_url2


def lookup(name: str) -> str:
    template = """given the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username.
       In Your Final answer only the person's username"""

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    react_prompt = hub.pull("hwchase17/react")
    tools_for_agent=[
        Tool(
            name="Crawl Google 4 Twitter profile page",
            func=get_profile_url2,
            description="useful for when you need get the Twitter Page URL")]
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    twitter_username = agent_executor.invoke(
        input = {"input": prompt_template.format_prompt(name_of_person=name)}
    )

    return twitter_username