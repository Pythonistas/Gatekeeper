import yaml

def fields_from_request(request):
    fields = request.args.get('fields')
    return fields.split(',') if fields else None

def load_from_yaml(input_file, animal_class):
    animals = {}
    try:
        with open(input_file, 'r') as stream:
            for data in yaml.safe_load(stream):
                cur_animal = animal_class()
                for key, value in data.items():
                    setattr(cur_animal, key, value)
                animals[cur_animal.object_id] = cur_animal
    except OSError:
        return None
    return animals
