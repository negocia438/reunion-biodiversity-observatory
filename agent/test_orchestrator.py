from types import SimpleNamespace

from orchestrator import execute_tool_calls
from tools import get_observation_count, get_data_freshness


available_tools = {
    "get_observation_count": get_observation_count,
    "get_data_freshness": get_data_freshness,
}


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