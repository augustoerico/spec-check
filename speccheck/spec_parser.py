import json

import yaml
from requests import get


class SpecParser:

    @classmethod
    def parse(cls, spec_path: str) -> dict:
        if spec_path.startswith('http'):
            spec = get(spec_path).content
        else:
            with open(spec_path, 'r') as f:
                spec = f.read()

        if spec_path.endswith('.json'):
            return json.loads(spec)
        elif spec_path.endswith('.yaml') or spec_path.endswith('.yml'):
            return yaml.load(spec)
        else:
            raise NotImplementedError()
