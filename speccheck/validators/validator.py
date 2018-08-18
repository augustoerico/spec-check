from validators.result_validator import ResultValidator
from validators.spec_validator import SpecValidator


class Validator:

    @classmethod
    def validate(cls, request: dict, response: dict, expected: dict, spec: dict):
        return {
            "result": ResultValidator.validate(response, expected),
            "spec": SpecValidator.validate(request, response, spec)
        }

    @classmethod
    def is_valid_status(cls, response_status, expected_status):
        response_generic_status = str(int(response_status) // 100) + 'XX'
        expected_status = str(expected_status)
        return expected_status == str(response_status) or expected_status == response_generic_status
