from operator import call

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

available_tools = {
    "get_observation_count": get_observation_count
}

if not response.function_calls:
    print("Aucun tool demandé.")
else:
    call = response.function_calls[0]

    if call.name not in available_tools:
        print(f"Tool interdit ou inconnu : {call.name}")
    else:
        tool = available_tools[call.name]

        try:
            result = tool(**call.args)
            print("Résultat :", result)

        except Exception as error:
            print("Erreur pendant l'exécution du tool :", error)


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