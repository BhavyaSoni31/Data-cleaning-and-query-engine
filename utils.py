from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

LLM_MODEL = "gpt-4o"
API_KEY = os.getenv("OPENAI_API_KEY", "")


def get_agent(dataframes: list, prefix: str = "", suffix: str = ""):

    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model=LLM_MODEL, openai_api_key=API_KEY),
        dataframes,
        prefix=prefix,
        suffix=suffix,
        verbose=True,
        allow_dangerous_code=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    return agent

def rephrase_query(prompt, query, current_time):

    llm = ChatOpenAI(
        model=LLM_MODEL,
        max_retries=3,
        api_key=API_KEY,
    )
    
    _prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                prompt,
            ),
            ("human", "{input}"),
        ]
    )

    chain = _prompt | llm
    
    output = chain.invoke(
        {
            "current_time": current_time,
            "input": query,
        }
    ).content

    return output
