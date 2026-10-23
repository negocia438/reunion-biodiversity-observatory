from google.genai import types


def execute_tool_calls(response, available_tools):
    function_responses = []

    for call in response.function_calls:

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
            result = tool(**call.args)

            function_responses.append(
                types.Part.from_function_response(
                    name=call.name,
                    response={
                        "result": result
                    }
                )
            )

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