import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import chainlit as cl
from whatsapp import send_whatsapp_message
# Load environment variables
load_dotenv(find_dotenv())
set_tracing_disabled(True)  # Function call, not variable assignment

# Gemini API setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash"

# External Gemini LLM client
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model=MODEL_NAME
)

# Tool function
@function_tool
def get_user_data(min_age: int) -> list[dict]:
    """Retrieve user data based on a minimum age."""
    users = [
        {"name": "Muneeb", "age": 22},
        {"name": "Muhammad Ubaid Hussain", "age": 25},
        {"name": "Azan", "age": 19},
    ]
    return [user for user in users if user["age"] >= min_age]

# Rishtey wali Auntie Agent
rishtey_wali_agent = Agent(
    name="Auntie",
    model=model,
    instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches.",
    tools=[get_user_data,send_whatsapp_message]  # WebSearchTool() ka use sirf OpenAI API key ke sath hoga
)

# On Chat Start
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="Salamz beta! Main hoon tumhari Rishtey wali Auntie. Apni age aur WhatsApp number do, main tumhein rishtay doongi!"
    ).send()

# On Message
@cl.on_message
async def main(message: cl.Message):
    await cl.Message(content="Thinking...").send()

    history = cl.user_session.get("history") or []
    history.append({"role": "user", "content": message.content})

    result = Runner.run_sync(
        starting_agent=rishtey_wali_agent,
        input=history
    )

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)

    await cl.Message(content=result.final_output).send()





# import asyncio
# import os
# from dotenv import find_dotenv, load_dotenv
# from openai import AsyncOpenAI
# from openai.types.responses import ResponseTextDeltaEvent
# from agents import Agent, Runner, OpenAIChatCompletionsModel,set_tracing_disabled,functiontool
# import chainlit  as cl


# load_dotenv(find_dotenv())
#  set_tracing_disabled = True

#  GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL_NAME = "gemini-2.0-flash"

# # 🔹 Step 2: Gemini LLM setup
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/"
# )

# model = OpenAIChatCompletionsModel(
#     openai_client=external_client,
#     model=MODEL_NAME
# )
# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # external_client =AsyncOpenAI(
# #     api_key = API_KEY,
# #     BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
# # )
# # model = OpenAIchatCompletionsMODEL(
# # MODEL = "gemini-2.0-flash"
# # openai_client=external_client
# # )

# @function_tool
# def get_user_data(min_age: int) -> list[dict]:
#     "Retrieve user data based on a minimum age"
#     users = [
#         {"name": "Muneeb", "age": 22},
#         {"name": "Muhammad Ubaid Hussain", "age": 25},
#         {"name": "Azan", "age": 19},
#     ]

#     for user in users:
#         if user["age"] < min_age:
#             users.remove(user)
    
#     return users
#     rishtey_wali_agent = Agent(
#     name="Auntie",
#     model=model,
#     instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches",
#     tools=[get_user_data, WebSearchTool()]   # WebSearchTool will only work with OpenAI API key, 
#     # if you want to use any other free llm use "browser-use"
#     @cl.on_chat_start
#     async def on_chat_start():
#         await cl.message("Salamz! beta!, I am your Rishtey wali Auntie. Give meyour full details age our whatsapp number and i give  you rishty!")
# )
# @cl.on_message
# async def main(message :cl.Message):
#     awiat cl.Message("t=Thinking..."). send()
#     history = cl.user_session.get("history")or[]
#     history.append({"role":"user","content":message.content}) 

#     result = Runner.run_sync(
#         starting_agent= rishtey_wali_agent,
#         input = history
#     )
# history.append({"role":"assistant","content":result.final_output})
# cl.user_session.set(("history",history))
# await cl.Message(content=result.final_output).send()


# def main():
#     print("Hello from rishty-wali-anutie-streamlit!")


# if __name__ == "__main__":
#     main()
