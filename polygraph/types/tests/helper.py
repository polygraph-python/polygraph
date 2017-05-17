from polygraph.types.field import field
from polygraph.types.object_type import ObjectType
from polygraph.types.scalar import Int, String


class Person(ObjectType):
    @field
    def name(self) -> String:
        pass

    @field
    def age(self) -> Int:
        pass


class Animal(ObjectType):
    @field
    def name(self) -> String:
        pass

    @field
    def sound(self) -> String:
        pass
