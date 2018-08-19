import os

import requests
import yaml

from speccheck.spec_parser import SpecParser
from speccheck.validators.validator import Validator


class ScenarioRunner:

    @classmethod
    def run(cls, collection_path: str, spec_path: str) -> dict:
        return cls.run_all(
            cls.parse_scenarios(collection_path),
            SpecParser.parse(spec_path)
        )

    @classmethod
    def parse_scenarios(cls, collection_path: str) -> list:
        return [
            yaml.load(
                open(os.path.join(collection_path, f), 'r').read()
            )
            for f in os.listdir(collection_path)
            if f.endswith('.yml') or f.endswith('.yaml')
        ]

    @classmethod
    def run_all(cls, scenarios: list, spec: dict) -> dict:
        return {"results": [
            cls.run_scenario(s, spec)
            for s in scenarios
        ]}

    @classmethod
    def run_scenario(cls, scenario: dict, spec: dict) -> dict:
        return {"steps_results": [
            cls.run_step(scenario['steps'][step], spec, scenario['headers'])
            for step in scenario['steps']
        ]}

    @classmethod
    def run_step(cls, step_obj: dict, spec: dict, headers: dict = None) -> dict:
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
            # "body": response.json(),
            "headers": {k.lower(): v.lower() for k, v in response.headers.items()}
        }

        return Validator.validate(request, response, step_obj['expected'], spec)
