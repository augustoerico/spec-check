class ResultValidator:

    @classmethod
    def validate(cls, response: dict, expected: dict):
        from speccheck.validators.validator import Validator

        valid_status = Validator.is_valid_status(response['status'], expected['status'])
        # valid_body = is_valid_body(...)
        valid = valid_status  # and valid_body
        return {
            "valid": valid,
            "status": {
                "valid": valid_status,
                "expected": str(expected['status']),
                "actual": str(response['status'])
            }
            # "body": { "status": valid_body, ... }
        }
