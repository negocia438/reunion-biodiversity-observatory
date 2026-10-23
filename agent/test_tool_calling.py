from google import genai
from google.genai import types
from tools import get_observation_count

client = genai.Client()

config = types.GenerateContentConfig(
    tools=[get_observation_count],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="ANY"
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

print(response.function_calls)

call = response.function_calls[0]

available_tools = {
    "get_observation_count": get_observation_count
}

tool = available_tools[call.name]

result = tool(**call.args)

print("Résultat :", result)

function_response = types.Part.from_function_response(
    name=call.name,
    response={
        "result": result
    }
)


final_response = chat.send_message(
    function_response
)

print("Réponse finale :", final_response.text)