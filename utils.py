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

def rephrase_query(prompt, query, current_time=None, df=None):

    llm = ChatOpenAI(
        model=LLM_MODEL,
        max_retries=3,
        api_key=API_KEY,
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                prompt,
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm
    
    if current_time:
        output = chain.invoke(
            {
                "current_time": current_time,
                "input": query,
            }
        ).content

    if df is not None:
        output = chain.invoke(
            {
                "sample_df": df,
                "input": query,
            }
        ).content

    return output

# query = "Number of bookings for American Airlines yesterday."
# answer = rephrase_query(rephrase_query_prompt, query)
# output = query_agent.invoke(answer)

# print(output)