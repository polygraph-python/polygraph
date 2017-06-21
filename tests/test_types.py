from polygraph.types import Int, String, TypeKind, field, object_type


def test_object_type():
    Person = object_type(
        name="Person",
        fields=[
            field(name="name", return_type=String, description="Name of person"),
            field(name="age", return_type=Int, description="Age"),
        ],
        description="Test person",
    )
    assert Person.kind == TypeKind.OBJECT
    assert Person.name == "Person"
    assert Person.description == "Test person"
