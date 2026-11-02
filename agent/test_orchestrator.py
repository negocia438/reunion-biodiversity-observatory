"""Démonstration locale de l’orchestrateur avec des appels Gemini simulés.

Aucune API ni base n’est appelée. Les scénarios initiaux sont affichés ; les validations sont vérifiées par assertions."""

from types import SimpleNamespace

from orchestrator import execute_tool_calls
from tools import get_observation_count, get_data_freshness


# Même registre que pour Gemini, mais utilisé sans réseau.
available_tools = {
    "get_observation_count": get_observation_count,
    "get_data_freshness": get_data_freshness,
}


# SimpleNamespace reproduit seulement les attributs lus par l’orchestrateur.
response_observation = SimpleNamespace(
    function_calls=[
        SimpleNamespace(
            name="get_observation_count",
            args={
                "genus": "Phelsuma",
                "year": 2024,
            }
        )
    ]
)


response_freshness = SimpleNamespace(
    function_calls=[
        SimpleNamespace(
            name="get_data_freshness",
            args={}
        )
    ]
)


response_both = SimpleNamespace(
    function_calls=[
        SimpleNamespace(
            name="get_observation_count",
            args={
                "genus": "Phelsuma",
                "year": 2024,
            }
        ),
        SimpleNamespace(
            name="get_data_freshness",
            args={}
        ),
    ]
)


# Scénarios affichés : comptage seul, fraîcheur seule, puis les deux ensemble.
print("TEST 1")
print(
    execute_tool_calls(
        response_observation,
        available_tools
    )
)


print("TEST 2")
print(
    execute_tool_calls(
        response_freshness,
        available_tools
    )
)


print("TEST 3")
print(
    execute_tool_calls(
        response_both,
        available_tools
    )
)

# Un outil espion permet de vérifier les arguments effectivement reçus.
captured_calls = []


def tracked_observation_count(genus, year):
    captured_calls.append({"genus": genus, "year": year})
    return 127


tracked_tools = {
    **available_tools,
    "get_observation_count": tracked_observation_count,
}


def observation_response(genus, year):
    return SimpleNamespace(function_calls=[SimpleNamespace(
        name="get_observation_count",
        args={"genus": genus, "year": year},
    )])


cleaned = execute_tool_calls(
    observation_response(" Phelsuma ", 2024), tracked_tools
)
assert cleaned[0].function_response.response == {"result": 127}
assert captured_calls == [{"genus": "Phelsuma", "year": 2024}]
print("PASS : espaces retirés avant l’appel de l’outil")

for genus, year in [("", 2024), ("   ", 2024), ("Phelsuma", 1700)]:
    invalid = execute_tool_calls(observation_response(genus, year), tracked_tools)
    assert "error" in invalid[0].function_response.response
    # Aucun appel supplémentaire ne doit avoir atteint l’outil.
    assert len(captured_calls) == 1
    print(f"PASS : arguments refusés sans exécution : {genus!r}, {year}")

# Une erreur de validation ne doit pas empêcher l’appel suivant de réussir.
mixed = observation_response("   ", 2024)
mixed.function_calls.append(response_freshness.function_calls[0])
results = execute_tool_calls(mixed, tracked_tools)
assert len(results) == 2
assert "error" in results[0].function_response.response
assert results[1].function_response.response == {"result": "2026-10-20"}
assert len(captured_calls) == 1
print("PASS : les appels suivants continuent après une erreur de validation")
