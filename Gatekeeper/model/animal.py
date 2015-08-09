import yaml
import flask

ages    = ["puppy", "young", "adult", "senior"]
sizes   = ["small", "medium", "large"]
genders = ["female", "male"]
statuses= ["unavailable", "available", "foster", "adopted", "tbpd"]

def load_from_yaml():
    dogs = []
    try:
        with open("dogs.yaml", 'r') as stream:
            for data in yaml.safe_load(stream):
                cur_dog = Dog()
                cur_dog.name = data['name']
                cur_dog.status = data['status']
                cur_dog.breed = data['breed']
                cur_dog.color = data['color']
                cur_dog.ageRange = data['ageRange']
                cur_dog.age = data['age']
                cur_dog.weightRange = data['weightRange']
                cur_dog.weight = data['weight']
                cur_dog.gender = data['gender']
                cur_dog.trained = data['trained']
                dogs.append(cur_dog)
        return dogs
    except OSError:
        print("File not found")

class Dog(object):
    """data for individual dogs"""

    def __init__(self):
        self._id = 0
        self.name = ""
        self.status = ""
        self.breed = ""
        self.color = ""
        self.ageRange = ""
        self.age = 0
        self.weightRange = ""
        self.weight = 0
        self.gender = ""
        self.goodWith = {}
        self.trained = False
        self.notes = ""
        self.owners = ""
        self.primaryImage = {}
        self.links = {}
        self.metadata = {}

    def to_json_dict(self, *fields):
        if (len(fields) > 0):
            filtered_dog = {}
            for field in fields:
                try:
                    filtered_dog[field] = getattr(self, field)
                except AttributeError:
                    print("Attribute not found")
            return filtered_dog 
        else:
            return {'name' : getattr(self, 'name'), 
                    'status': getattr(self,'status'),
                    'breed': getattr(self,'breed'),
                    'color': getattr(self,'color'),
                    'ageRange': getattr(self,'ageRange'),
                    'age': getattr(self,'age'),
                    'weightRange': getattr(self,'weightRange'),
                    'weight': getattr(self,'weight'),
                    'gender': getattr(self,'gender')
                   }
