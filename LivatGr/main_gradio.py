import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from utils.env_utils import init_logger, init_custom_env
init_custom_env(flag="prod", botname="main_gradio")
init_logger(file_name="main_gradio")
from utils.logger_utils import get_logger
logger = get_logger()

from enum import Enum
import gradio as gr
import time

from common.handlers import GPT35ApiInference
from common.models.dto import UniMsg
from common.models.msgs import Dialog, app, db
from common.models.dao import FsaDao
from utils.id_utils import get_session_id
inference = GPT35ApiInference()

fsa_dao = FsaDao(db=db, app=app)

system_role_content = "You are a helpful assisant"
session_id = get_session_id()

def predict_v2(input, history=[], model_id="0000"):
    """
    history: [['***', '***']]
    """
    uni_history = []
    for h in history:
        uni_history.append(UniMsg(role_type="user", content=h[0], round=len(uni_history)))
        uni_history.append(UniMsg(role_type="assistant", content=h[1], round=len(uni_history)))
    input_msg = UniMsg(role_type="user", content=input, round=len(uni_history))
    fsa_dao.save_obj(Dialog(content=input,
                            role="default_user",
                            role_type="user",
                            round=len(uni_history),
                            session_id=session_id))
    uni_history.append(input_msg)
    resp = inference.infer(history=uni_history, stream=False, syetem_role_content=system_role_content)
    fsa_dao.save_obj(Dialog(content=resp,
                            role="openai",
                            role_type="model",
                            round=len(uni_history),
                            session_id=session_id))
    return resp

def save_dialogues(history):
    logger.debug("------------------")
    return history

def update_system_role_content(text1):
    global system_role_content
    system_role_content = text1

def clear_dialog():
    global session_id
    session_id = get_session_id()
    return None, [[session_id, None]]

class ModelIdType(Enum):
    ChatYuanInference = "0000"
    GLM6BInference = "0001"
    GPT35ApiInference = "1000"


with gr.Blocks() as demo:
    ## layout
    with gr.Row():
        with gr.Column(scale=1, variant=system_role_content):
            text1 = gr.Textbox(label="System role", placeholder=system_role_content)
            text2 = gr.Chatbot(label="session-id", value=[[session_id, None]])
        with gr.Column(scale=5):
            with gr.Row():
                dropdown = gr.Dropdown(
                    [
                    ModelIdType.GPT35ApiInference.name,
                    ModelIdType.GLM6BInference.name,
                    # ModelIdType.ChatYuanInference.name,
                     ],
                    value=ModelIdType.GPT35ApiInference.name,
                    label="Choose model_id",
                    # info="Will add more model later!"
                )
                save = gr.Button("save dialogues")
                clear = gr.Button("Clear")

            chatbot = gr.Chatbot()
            msg = gr.Textbox()


    def user(user_message, history):
        """
        user_message: msg
        history: chatbot
        """
        return "", history + [[user_message, None]]

    def bot(history, pp):
        """
        history: chatbot
        pp: dropdown
        """
        logger.debug(history)
        logger.debug(ModelIdType.__getitem__(pp).value)
        input_payload = history[-1][0]
        history_payload = history[0:-1]
        try:
            bot_message = predict_v2(input_payload, history=history_payload, model_id=ModelIdType.__getitem__(pp).value)
        except Exception as e:
            logger.error(e)
            bot_message = f"出错啦：{e.__repr__()}"
        # bot_message = random.choice(["Yes", "No"])
        history[-1][1] = bot_message
        time.sleep(0.5)
        return history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot, dropdown], chatbot
    )
    text1.submit(update_system_role_content, text1, None)
    clear.click(clear_dialog, None, [chatbot, text2], queue=False)
    save.click(save_dialogues, chatbot, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(share=False, server_name='0.0.0.0')
