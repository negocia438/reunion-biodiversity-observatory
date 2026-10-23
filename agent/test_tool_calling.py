from google import genai
from google.genai import types
from dotenv import load_dotenv

from tools import get_observation_count
from orchestrator import execute_tool_calls


load_dotenv()

client = genai.Client()


available_tools = {
    "get_observation_count": get_observation_count
}


config = types.GenerateContentConfig(
    tools=[
        get_observation_count
    ],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="AUTO"
        )
    ),
)


chat = client.chats.create(
    model="gemini-3.8-flash",
    config=config
)


response = chat.send_message(
    "Combien d'observations de Phelsuma avons-nous en 2024 ?"
)


if not response.function_calls:
    print("Réponse directe :", response.text)

else:
    function_responses = execute_tool_calls(
        response,
        available_tools
    )

    final_response = chat.send_message(
        function_responses
    )

    print("Réponse finale :", final_response.text)