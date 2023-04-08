from enum import Enum
import gradio as gr
import time
import requests
import utils.env as env
from utils.logger_utils import logging
def predict(input, history=[]):
    logging.debug(history)
    resp = requests.post(url=f"http://localhost:{env.port}/chat",
                         json={"question":input,
                               "history":history,})
    response  = resp.json()["data"]["response"]
    return response



with gr.Blocks() as demo:
    ## layout
    with gr.Row():
        with gr.Column():
            with gr.Row():
                clear = gr.Button("Clear")

            chatbot = gr.Chatbot()
            msg = gr.Textbox()


    def user(user_message, history):
        """
        user_message: msg
        history: chatbot
        """
        return "", history + [[user_message, None]]

    def bot(history):
        """
        history: chatbot
        """
        input_payload = history[-1][0]
        history_payload = history[0:-1]
        try:
            bot_message = predict(input_payload, history=history_payload)
        except Exception as e:
            logging.error(e)
            bot_message = f"出错啦：{e.__repr__()}"
        # bot_message = random.choice(["Yes", "No"])
        history[-1][1] = bot_message
        time.sleep(0.5)
        return history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot], chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(share=False, server_name='0.0.0.0', server_port=env.gr_port)
