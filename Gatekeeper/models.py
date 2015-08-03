class Animal(object):
    """description of Animal goes here"""

    import itertools

    _counter = itertools.count().__next__
    _sizeRange = ['Small','Medium','Large']
    _sex = ['Male','Female']
    _ageRange = ['Baby','Young','Adult','Senior']

    def __init__(self):
        self.id = str(Animal._counter()).rjust(6, '0')
        self.name = ''
        self.age = 0
        self.ageRange = '' #_ageRange[0]
        self.size = '' #_sizeRange[0]
        self.weight = 0
        self.sex = '' #_sex[0]

    def __repr__(self):
        _result = [("{key}='{value}'".format(key=key, value=self.__dict__[key])) for key in self.__dict__]
        return '{0}({1})'.format(self.__class__.__name__, ', '.join(_result))

    def to_json_dict(self, *fields):
        """
        Returns a dictionary of properties, limited to those specified in fields, 
        or all public fields if fields is not specified.
        """

        if fields:
            return {str(self.__class__.__name__).lower(): {str(field): getattr(self, field) for field in fields}}
        else:
            return {str(self.__class__.__name__).lower(): self.__dict__}
            
class Dog(Animal):
    """description of Dog goes here"""

    _group = ['Hearding','Hound','NonSporting','Sporting','Terrier','Toy','Working','FoundationStockService','Miscellaneous']

    def __init__(self):
        super().__init__()
        self.breed = ''
        self.group = '' #_group[0]
        self.color = ''
