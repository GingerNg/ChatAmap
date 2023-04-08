from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.agents import initialize_agent
import uvicorn
import utils.env as env
from utils.logger_utils import logging
from fastapi import FastAPI


app = FastAPI()

from typing import Dict, List, Tuple
from pydantic import BaseModel

class ChatParam(BaseModel):
    question: str
    history: List[Tuple[str, str]] = []



from handler import plan_route


# ****************************agent************************** #
tools = [
    Tool(
        name = "Gaode",
        func=lambda q: str(plan_route(q)),
        description="用于规划路线。输入是一个中文句子。",
        return_direct=True
    )
]

# set Logging to DEBUG for more detailed outputs
memory = ConversationBufferMemory(memory_key="chat_history")
llm=OpenAI(temperature=0)
agent_chain = initialize_agent(tools, llm, agent="conversational-react-description",
                                    memory=memory,
                                    verbose=True)

# ***************************api************************* #

@app.post("/chat")
def chitchat_infer(param: ChatParam):
    try:
        question = param.question
        response = agent_chain.run(input=question)
        history = param.history
        history.append([question, response])
        # print(response)
        return { "data":{"response": response, "history": history},
                'status': 1}
    except Exception as e:
        logging.error(e)
        return {"status": 0}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=env.port)