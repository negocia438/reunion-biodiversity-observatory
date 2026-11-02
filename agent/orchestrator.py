"""Exécute les outils demandés par Gemini et prépare les réponses pour le modèle."""

from google.genai import types


def execute_tool_calls(response, available_tools):
    """Convertit chaque appel en réponse SDK, contenant un résultat ou une erreur.

    response.function_calls doit être itérable. available_tools associe les noms
    autorisés aux fonctions Python ; aucun nom fourni par le modèle n’est évalué.
    """
    function_responses = []

    # Conserver l’ordre des appels pour renvoyer une réponse à chacun.
    for call in response.function_calls:

        # La liste explicite des outils limite les fonctions exécutables.
        if call.name not in available_tools:
            function_responses.append(
                types.Part.from_function_response(
                    name=call.name,
                    response={
                        "error": f"Tool inconnu : {call.name}"
                    }
                )
            )
            continue

        tool = available_tools[call.name]

        try:
            # Les arguments nommés du modèle deviennent les paramètres Python.
            result = tool(**call.args)

            function_responses.append(
                types.Part.from_function_response(
                    name=call.name,
                    response={
                        "result": result
                    }
                )
            )

        # Une erreur d’outil devient une réponse ; les appels suivants continuent.
        except Exception as error:
            function_responses.append(
                types.Part.from_function_response(
                    name=call.name,
                    response={
                        "error": str(error)
                    }
                )
            )

    return function_responses