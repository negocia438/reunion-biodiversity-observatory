"""Démonstration du choix des outils par Gemini avec exécution manuelle en Python.

Contacte Gemini et utilise des résultats métier simulés, sans accès PostgreSQL."""

from google import genai
from google.genai import types
from dotenv import load_dotenv

from tools import get_observation_count, get_data_freshness
from orchestrator import execute_tool_calls


# Charge les variables locales d’un .env, sans écraser celles déjà exportées.
load_dotenv()

client = genai.Client()


# Registre utilisé par notre orchestrateur pour résoudre les noms des outils.
available_tools = {
    "get_observation_count": get_observation_count,
    "get_data_freshness": get_data_freshness,
}


# Le SDK déduit les descriptions des outils de leurs signatures et docstrings.
config = types.GenerateContentConfig(
    tools=[
        get_observation_count,
        get_data_freshness,
    ],
    # Désactive l’exécution automatique : notre code garde la main.
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            # Gemini peut répondre directement ou demander des outils.
            mode="AUTO"
        )
    ),
)


chat = client.chats.create(
    model="gemini-3.8-flash",
    config=config
)


response = chat.send_message(
    "Combien d'observations de Phelsuma avons-nous en 2024 "
    "et à quand remonte la dernière mise à jour des données ?"
)

print("Function calls :", response.function_calls)


if not response.function_calls:
    print("Réponse directe :", response.text)

else:
    function_responses = execute_tool_calls(
        response,
        available_tools
    )

    # Un seul aller-retour est géré : aucun nouvel appel d’outil n’est traité ici.
    final_response = chat.send_message(
        function_responses
    )

    print("Réponse finale :", final_response.text)