from exceptions import PathNotFound, OperationNotFound


class SpecValidator:

    @classmethod
    def validate(cls, request: dict, response: dict, spec: dict) -> dict:
        operation_spec = cls.get_operation_spec(request, spec)

        return {
            "status": "",
            "request": "",
            "response": cls.validate_response(response, operation_spec)
        }

    @classmethod
    def get_operation_spec(cls, request: dict, spec: dict) -> dict:
        path = cls.get_matching_path(request['path'], spec['paths'].keys())

        path_item = spec['paths'].get(path)
        if not path_item:
            raise PathNotFound()

        operation = path_item.get(request['operation'])
        if not operation:
            raise OperationNotFound()

        return operation

    @classmethod
    def get_matching_path(cls, path: str, spec_paths: list) -> str:
        return ''

    @classmethod
    def validate_response(cls, response: dict, operation_spec: dict) -> dict:
        status = response['status']
        generic_status = str(int(status) // 100) + 'XX'

        return dict()
