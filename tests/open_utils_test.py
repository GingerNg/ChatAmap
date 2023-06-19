from utils.env_utils import env_conf
from utils.openai_utils import Openai, openai

# def test_count():
#     assert count([1, 2, 3]) == 3
messages = [
    {"role": "user", "content": "你是一个聊天助手，*****"}
]

def test_request_flask_app():
    import requests
    resp = requests.post("http://127.0.0.1:5001/chat",
                         stream=True,
                         json={"model": "gpt-3.5-turbo",
                        "messages": messages,
                        "timeout": 5,
                        "stream": True,
                        "presence_penalty": 1,
                        # "max_tokens": 800,
                        "temperature": 0.8
        })
    # print(resp.content)
    # Python requests库的stream属性: https://kushao1267.github.io/2019/06/25/python-requests-stream/
    for chunk in resp.iter_content(chunk_size=8192):
        if chunk:
            resp_content = chunk.decode("utf-8")
            print(resp_content)
    # print(resp)
    # for r in resp:
    #     print(r)

def test_request_stream():
    import requests
    resp = requests.post("http://localhost:8083/v1/chat/completions",
                         json={"model": "gpt-3.5-turbo",
                        "messages": messages,
                        "timeout": 5,
                        "stream": True,
                        "presence_penalty": 1,
                        # "max_tokens": 800,
                        "temperature": 0.8
        })
    print(resp)
    for r in resp:
        print(r)

def test_sse():
    openai.api_base = "http://localhost:8084/v1"
    openai.api_key = 'sk-*****'
    openai_obj = Openai()
    result = []
    resp = openai_obj.chat_complete(messages, stream=True)
    print(resp)
    for r in resp:
        one = r.choices[0].delta.content if 'content' in r.choices[0].delta else ''
        print(one)
        result.append(one)


from utils.openai_utils import num_tokens_from_messages
def test_count_tokens():
    example_messages = [
        {
            "role": "system",
            "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English.",
        },
        {
            "role": "system",
            "name": "example_user",
            "content": "New synergies will help drive top-line growth.",
        },
        {
            "role": "system",
            "name": "example_assistant",
            "content": "Things working well together will increase revenue.",
        },
        {
            "role": "system",
            "name": "example_user",
            "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage.",
        },
        {
            "role": "system",
            "name": "example_assistant",
            "content": "Let's talk later when we're less busy about how to do better.",
        },
        {
            "role": "user",
            "content": "This late pivot means we don't have time to boil the ocean for the client deliverable.",
        },
    ]

    for model in ["gpt-3.5-turbo-0301", "gpt-4-0314"]:
        print(model)
        # example token count from the function defined above
        print(f"{num_tokens_from_messages(example_messages, model)} prompt tokens counted by num_tokens_from_messages().")
        # example token count from the OpenAI API
        response = openai.ChatCompletion.create(
            model=model,
            messages=example_messages,
            temperature=0,
            max_tokens=1  # we're only counting input tokens here, so let's not waste tokens on the output
        )
        print(f'{response["usage"]["prompt_tokens"]} prompt tokens counted by the OpenAI API.')
        print()