import re

from exceptions import PathNotFound, OperationObjNotFound, ResponseObjNotFound, MediaTypeObjNotFound, \
    SchemaObjNotFound
from validators.json_schema_validator import JsonSchemaValidator


class SpecValidator:

    @classmethod
    def validate(cls, request: dict, response: dict, spec: dict) -> dict:
        """

        :param request:
        :param response:
        :param spec: OpenAPI object as specified in
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#oasObject
        :return:
        """
        operation_spec = cls.get_operation_spec(request, spec)

        return {
            "status": "",
            "request": "",
            "response": cls.validate_response(response, operation_spec)
        }

    @classmethod
    def get_operation_spec(cls, request: dict, spec: dict) -> dict:
        """

        :param request:
        :param spec: OpenAPI object as specified in
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#oasObject
        :return: OperationObject as specified in
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#operationObject
        """
        path = cls.get_matching_path(request['path'], list(spec['paths'].keys()))

        path_item = spec['paths'].get(path)
        if not path_item:
            raise PathNotFound()

        operation = path_item.get(request['operation'])
        if not operation:
            raise OperationObjNotFound()

        return operation

    @classmethod
    def get_matching_path(cls, path: str, template_paths: list) -> str:
        for p in template_paths:
            pattern = p.replaceAll('{\\w+}', r'\w+').replaceAll('/', r'\/')
            if re.match(pattern, path):
                return path
        return ''

    @classmethod
    def validate_response(cls, test_response: dict, operation_obj: dict) -> dict:
        """

        :param test_response:
        :param operation_obj: OperationObject as specified in
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#operationObject
        :return:
        """
        status = test_response['status']
        generic_status = str(int(status) // 100) + 'XX'
        responses_obj = operation_obj['responses']

        response_obj = \
            responses_obj.get(str(status)) \
            or responses_obj.get(generic_status) \
            or responses_obj.get('default')

        if not response_obj:
            raise ResponseObjNotFound()

        content = responses_obj.get('content')
        if not content:
            return {"valid": True}

        # TODO it needs further investigation to handle headers
        media_type = test_response['headers'].get('content-type')
        # TODO for now, only evaluating the application/json content-type
        if media_type != 'content-type':
            raise NotImplementedError(f'Media type not supported: {media_type}')

        media_type_obj = content.get(media_type or '')
        if not media_type_obj:
            raise MediaTypeObjNotFound

        schema = media_type_obj.get('schema')
        if not schema:
            raise SchemaObjNotFound()

        # TODO research if there is a way to resolve $ref
        return JsonSchemaValidator.validate(schema, test_response["body"])

    # TODO implement it
    @classmethod
    def validate_headers(cls, response_headers: dict, response_obj: dict):
        """

        :param response_headers:
        :param response_obj: response_obj as specified in
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#responseObject
        :return:
        """
        headers = {k: v for k, v in response_headers.items() if k.lower() != 'content-type'}
        content = (response_headers.get('content-type') or '').lower()
        raise NotImplementedError('Method not implemented')
