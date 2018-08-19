import requests
from validators.validator import Validator


def run_scenario(scenario: dict, spec: dict) -> dict:
    return {"steps_results": [
        run_step(scenario['steps'][step], spec, scenario['headers'])
        for step in scenario['execution']
    ]}


def run_step(step_obj: dict, spec: dict, headers: dict=None) -> dict:
    operation = step_obj['operation'].lower()
    headers = headers or {}
    server = spec['servers'][0]['url']  # FIXME run against all servers
    url = server + step_obj['path']
    if operation == 'get':
        response = requests.get(url, headers=headers)
    else:
        raise NotImplementedError(f"Operation not implemented: {operation}")

    request = {"path": step_obj['path'], "operation": operation, "headers": headers}
    response = {
        "status": response.status_code,
        "body": response.json(),
        "headers": {k.lower(): v.lower() for k, v in response.headers.items()}
    }

    return Validator.validate(request, response, step_obj['expected'], spec)
