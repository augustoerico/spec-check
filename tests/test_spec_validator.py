import yaml

from speccheck.validators.spec_validator import SpecValidator


def test_spec_response_not_valid_for_mismatching_schema():
    # given
    with open('tests/resources/openapi/characters.yaml', 'r') as f:
        spec = yaml.load(f.read())
    request = {
        "path": "/characters",
        "operation": "get"
    }
    response = {
        "status": 200,
        "headers": {"content-type": "application/json"},
        "body": [{"id": "1234", "name": "Shinny Broccoli"}]
    }

    # when
    result = SpecValidator.validate(request, response, spec)

    # then
    assert result['valid'] is False
