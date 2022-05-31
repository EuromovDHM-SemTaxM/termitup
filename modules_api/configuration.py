import ruamel.yaml as yaml

PARAMS = {}
with open("global_config.yaml", "r") as stream:
    try:
        parameters = yaml.safe_load(stream)
        PARAMS.update(parameters)
    except yaml.YAMLError as exc:
        print(exc)
