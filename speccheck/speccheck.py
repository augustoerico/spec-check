from speccheck.scenario_runner import ScenarioRunner

if __name__ == '__main__':

    collection_path = 'scenarios'
    spec_path = 'https://github.com/OAI/OpenAPI-Specification/blob/master/examples/v3.0/petstore.yaml'

    print(ScenarioRunner.run(collection_path, spec_path))
