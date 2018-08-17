def validate(response: dict, expected: dict, spec: dict):
    return {
        "expected": validate_expected(response, expected),
        "spec": validate_spec(response, spec)
    }


def validate_expected(response: dict, expected: dict):
    return {
        "status": {
            "valid": is_valid_status(response['status'], expected['status']),
            "expected": str(expected['status']),
            "actual": str(response['status'])
        }
    }


def validate_spec(response: dict, spec: dict):
    return {
        "status": "",
        "response_schema": ""
    }


def is_valid_status(response_status, expected_status):
    response_generic_status = str(int(response_status) // 100) + 'XX'
    expected_status = str(expected_status)
    return expected_status == str(response_status) or expected_status == response_generic_status
