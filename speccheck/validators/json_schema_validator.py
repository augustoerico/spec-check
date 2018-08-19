from jsonschema import validators, exceptions
import json


class JsonSchemaValidator:

    @classmethod
    def validate(cls, schema: str, json_) -> dict:

        if isinstance(json_, str):
            json_ = json.loads(json_)
        elif not isinstance(json_, dict):
            raise ValueError()

        try:
            validators.validate(json_, schema)
        except exceptions.ValidationError as e:
            errors = [{
                "message": error.message
                for error in e.validator.iter_errors(json_)
            }]
            result = {"valid": False, "errors": errors}
        except exceptions.SchemaError as e:
            # TODO investigate what this error looks like and improve errors
            errors = [{"message": f'Invalid schema: {str(e.cause)}'}]
            result = {"valid": False, "errors": errors}
        else:
            result = {"valid": True}

        return result
