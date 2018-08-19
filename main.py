from speccheck.scenario_runner import ScenarioRunner

if __name__ == '__main__':

    collection_path = 'scenarios'
    spec_path = \
        'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore-expanded.yaml'

    print(ScenarioRunner.run(collection_path, spec_path))
