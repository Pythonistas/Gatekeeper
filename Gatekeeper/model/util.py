import yaml


def fields_from_request(request):
    fields = request.args.get('fields')
    return fields.split(',') if fields else None


def load_from_yaml(input_file, data_class):
    yaml_dict = {}
    try:
        with open(input_file, 'r') as stream:
            for data in yaml.safe_load(stream):
                cur_item = data_class()
                for key, value in data.items():
                    setattr(cur_item, key, value)
                yaml_dict[cur_item.object_id] = cur_item
    except OSError:
        return None
    return yaml_dict
