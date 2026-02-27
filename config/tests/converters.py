from .constants import LEVELS, TYPES

class LevelConverter:
    regex = "|".join(LEVELS)

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
    

class TypeConverter:
    regex = "|".join(TYPES)

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value