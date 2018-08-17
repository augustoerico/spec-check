import yaml


def parse_yaml(file_path: str) -> dict:
    """

    :param file_path: yaml file location
    :return: OpenAPI spec object
    """
    # TODO add try/catch
    with open(file_path, 'r') as f:
        spec = yaml.load(f.read())

    return spec
