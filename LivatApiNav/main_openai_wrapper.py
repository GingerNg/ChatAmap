import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from fastapi import FastAPI
import uvicorn
from fastapi import FastAPI, HTTPException, Request, status, BackgroundTasks
# from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from utils.env_utils import env_conf
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

import json
from typing import List, Optional

from dataclasses import dataclass
from typing import List

# from domain import UserTokens
from utils.openai_utils import Openai, num_tokens_from_messages

openai_obj = Openai()

from utils.message_utils import Sender
sender = Sender()

# *******************************************

@dataclass
class Context:
    llm_model_type: str
    model: any
    tokenizer: any
    embeddings_model: any
    tokens: List[str]


@dataclass
class User:
    user: str
    token: str
    token_limit: int
UserTokens = {}
UserTokens["sk-123456"] = User(user="test", token="sk-123456", token_limit=10000)
context = Context(None, None, None, None, UserTokens.keys())

def generate_response(content: str):
    return {
        "id": "chatcmpl-77PZm95TtxE0oYLRx3cxa6HtIDI7s",
        "object": "chat.completion",
        "created": 1682000966,
        "model": "gpt-3.5-turbo-0301",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 10,
            "total_tokens": 20,
        },
        "choices": [{
            "message": {"role": "assistant", "content": content},
            "finish_reason": "stop", "index": 0}
        ]
    }


def generate_stream_response_start():
    return {
        "id": "chatcmpl-77QWpn5cxFi9sVMw56DZReDiGKmcB",
        "object": "chat.completion.chunk", "created": 1682004627,
        "model": "gpt-3.5-turbo-0301",
        "choices": [{"delta": {"role": "assistant"}, "index": 0, "finish_reason": None}]
    }


def generate_stream_response(content: str):
    return {
        "id": "chatcmpl-77QWpn5cxFi9sVMw56DZReDiGKmcB",
        "object": "chat.completion.chunk",
        "created": 1682004627,
        "model": "gpt-3.5-turbo-0301",
        "choices": [{"delta": {"content": content}, "index": 0, "finish_reason": None}
                    ]}


def generate_stream_response_stop():
    return {"id": "chatcmpl-77QWpn5cxFi9sVMw56DZReDiGKmcB",
            "object": "chat.completion.chunk", "created": 1682004627,
            "model": "gpt-3.5-turbo-0301",
            "choices": [{"delta": {}, "index": 0, "finish_reason": "stop"}]
            }

class Message(BaseModel):
    role: str
    content: str

class ChatBody(BaseModel):
    messages: List[Message]
    model: str
    stream: Optional[bool] = False
    max_tokens: Optional[int]
    temperature: Optional[float]
    top_p: Optional[float]

@app.post("/v1/chat/completions")
async def completions(body: ChatBody, request: Request, background_tasks: BackgroundTasks):
    # background_tasks.add_task(torch_gc)
    auth_token = request.headers.get("Authorization").split(" ")[1]
    if auth_token not in context.tokens:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")

    # find user and limit by token
    user = UserTokens.get(auth_token, None)
    if user.token_limit < 0:
        raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED, "cash used up!")

    # model = body.model
    # if not context.model:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, "LLM model not found!")

    # if not sender.ping():
    #     raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal error")

    question = body.messages[-1]
    if question.role == 'user':
        question = question.content
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No Question Found")
    messages = []
    for message in body.messages:
        messages.append(message.__dict__)

    history = []
    user_question = ''
    for message in body.messages:
        if message.role == 'system':
            history.append((message.content, "OK"))
        if message.role == 'user':
            user_question = message.content
        elif message.role == 'assistant':
            assistant_answer = message.content
            history.append((user_question, assistant_answer))

    print(f"question = {question}, history = {history}")

    if body.stream:
        async def eval_llm_v2():
            first = True
            for response in ["hello", "hello", "hello", "hello", "hello"]:
            # for response in context.model.do_chat_stream(
            #     context.model, context.tokenizer, question, history, {
            #         "temperature": body.temperature,
            #         "top_p": body.top_p,
            #         "max_tokens": body.max_tokens,
            #     }):
                if first:
                    first = False
                    yield f"data: {json.dumps(generate_stream_response_start(),ensure_ascii=False)}\n\n"
                yield f"data: {json.dumps(generate_stream_response(response), ensure_ascii=False)}\n\n"
                # print(response)
            yield f"data: {json.dumps(generate_stream_response_stop(), ensure_ascii=False)}\n\n"
            yield f"data: [DONE]\n\n"

        async def eval_llm():
            tokens = []
            first = True
            ensure_ascii = False
            for response in openai_obj.chat_complete(messages=messages):
                one = response.choices[0].delta.content if 'content' in response.choices[0].delta else ''
                if first:
                    first = False
                    yield json.dumps(generate_stream_response_start(),
                                    ensure_ascii=ensure_ascii)
                tokens.append(one)
                yield json.dumps(response, ensure_ascii=ensure_ascii)
            # yield json.dumps(generate_stream_response_stop(), ensure_ascii=ensure_ascii)

            # token counter
            # messages.append({"role": "system", "content": "".join(tokens)})
            # num_tokens = num_tokens_from_messages(messages=messages, model=model)
            # await sender.send(str(num_tokens))
            yield '[DONE]'
        # return StreamingResponse(eval_llm_v2(),
        #                          headers={"Connection": "keep-alive",
        #                                   "Content-Type": "text/event-stream",
        #                                   "X-Accel-Buffering": "no",
        #                                   "Cache-Control": "no-cache",},
        #                         #  media_type='text/plain '
        #                          )
        return EventSourceResponse(eval_llm(),
                                    ping=10000
                                    )
    else:
        # response = "hello"
        response = openai_obj.chat_complete(messages=messages, stream=False)
        # response = context.model.do_chat(context.model, context.tokenizer, question, history, {
        #     "temperature": body.temperature,
        #     "top_p": body.top_p,
        #     "max_tokens": body.max_tokens,
        # })
        return JSONResponse(content=generate_response(response))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8084)