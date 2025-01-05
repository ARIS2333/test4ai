import streamlit as st
import openai
from openai import OpenAI
import json

from mangers.thread_manger import ThreadHandler
from mangers.message_manger import MessageManger
from mangers.runs_manager import RunsManager


########################################参数设置########################################
if "apibase" in st.secrets:
    OPENAI_API_KEY = st.secrets["apibase"]
else:
    OPENAI_API_KEY = "https://api.openai.com/v1"

client = openai.OpenAI(api_key=OPENAI_API_KEY)

ThreadManager = ThreadHandler(client)
MessageManger = MessageManger(client)
RunsManager = RunsManager(client)

thread_id = "thread_9CLLPmaMtZF8ZpEhsL5F0DIZ"
assistant_id = "asst_NRv8h202G699izYUeCjtEQiv"

all_thread_ids = ['thread_9CLLPmaMtZF8ZpEhsL5F0DIZ', 'thread_S0S7W66Sjr0BZAy9JAUnlVXV', 'thread_0Y0rPIE7DRsXVc12a8Kux2jy']


########################################helpers########################################
def get_response(user_input, assistant_id, thread_id):

        # 创建用户消息
        message = MessageManger.create_message(
            thread_id=thread_id,
            role="user",
            content=user_input,
        )

        # 创建并轮询运行
        run = RunsManager.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # 获取回复
        response_message = None
        messages = MessageManger.list_messages(thread_id)
        for message in messages:
            if message.role == "assistant" and message.created_at > run.created_at:
                response_message = message

        # return response_message.content
        return response_message.content[0].text.value

# new_thread_id = ThreadManager.create_thread().id

# def save_info4thread(thread_id, **kwargs):
#     # 以json格式保存创建的thread信息，存储到chat_info文件夹下
#     with open(f"chat_info/{thread_id}.json", "w") as f:
#         json.dump(kwargs, f)






########################################页面设置########################################
st.set_page_config(
    page_title="ChatGPT Assistant",
    layout="wide",
    page_icon="🤖"
)
st.title("ChatGPT Assistant")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("#### 操作")
    st.markdown("#### 设置")
    st.markdown("#### 帮助")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    # option选项去选择thread_id
    thread_id = st.selectbox("选择对话", all_thread_ids)
    st.markdown(f"**当前对话**: {thread_id}")

 
########################################历史对话展示########################################
history_messages = MessageManger.extract_listed_messages(MessageManger.list_messages(thread_id))

container_show_messages = st.container()
with container_show_messages:
    for history_message in history_messages:
        role = history_message['role']
        content = history_message['content']
        st.chat_message(role).write(content)


########################################对话输入########################################
if mesg := st.chat_input(placeholder='请输入你的问题', key="user_input"):
    response = get_response(mesg, assistant_id, thread_id)
    st.chat_message("user").write(mesg)
    st.chat_message("assistant").write(response)
