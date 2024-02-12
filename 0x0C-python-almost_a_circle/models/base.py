#!/usr/bin/python3
"""
Base class
"""
import json
import csv
import turtle


class Base:
    """
    The Base class is the foundation for all other classes in this project.
    It manages the 'id' attribute, ensuring its proper assignment based on the
    provided argument.

    Attributes:
        __nb_objects (int): A private class attribute to keep track of the
                            number of objects created.

    Methods:
        __init__(self, id=None): The class constructor.

    Static Methods:
        to_json_string(list_dictionaries): Returns the JSON string
                                           representation of list_dictionaries.

        from_json_string(json_string): Converts a JSON string to a
                                        list of dictionaries.

        draw(list_rectangles, list_squares): Opens a window and draws
                                            all the Rectangles and Squares
                                            using Turtle graphics.

    Class Methods:
        save_to_file(cls, list_objs): Save a list of instances to a JSON file.

        create(cls, **dictionary): Create an instance with attributes set
                                    from a dictionary.

        load_from_file(cls): Load instances from a JSON file and return a list
                             of instances.

        save_to_file_csv(cls, list_objs): Save a list of instances
                                          to a CSV file.

        load_from_file_csv(cls): Load a list of instances from a CSV file.
    """
    __nb_objects = 0

    def __init__(self, id=None):
        """
        The class constructor. Initializes a new instance of the Base class.

        Args:
            id (int): Identifier for the instance.

        Note:
            If 'id' is not None, assign to the public instance attribute 'id'.
            Otherwise, increment __nb_objects and assign the new value to 'id'.
        """

        if id is not None:
            if type(id) is not int:
                raise TypeError("id must be an integer")
            if id <= 0:
                raise ValueError("id must be greater than 0")
            self.id = id
        else:
            Base.__nb_objects += 1
            self.id = Base.__nb_objects

    @staticmethod
    def to_json_string(list_dictionaries):
        """
        Returns the JSON string representation of list_dictionaries.

        Args:
            list_dictionaries (list): A list of dictionaries.

        Returns:
            str: JSON string representation of list_dictionaries.
        """
        if list_dictionaries is None or not list_dictionaries:
            return "[]"
        else:
            return json.dumps(list_dictionaries)

    @staticmethod
    def from_json_string(json_string):
        """
        Convert a JSON string to a list of dictionaries.

        Args:
            json_string (str): JSON string to be converted.

        Returns:
            list: List of dictionaries represented by the JSON string.
        """
        if json_string is None or json_string == "":
            return []
        return json.loads(json_string)

    @classmethod
    def save_to_file(cls, list_objs):
        """
        Save a list of instances to a JSON file.

        Args:
            list_objs (list): List of instances to be saved.

        """
        filename = "{}.json".format(cls.__name__)
        with open(filename, "w") as file:
            if list_objs is None:
                file.write("[]")
            else:
                list_dicts = [obj.to_dictionary() for obj in list_objs]
                file.write(cls.to_json_string(list_dicts))

    @classmethod
    def create(cls, **dictionary):
        """
        Create an instance with attributes set from a dictionary.

        Args:
            **dictionary (dict): Dictionary containing attributes for
                                the instance.

        Returns:
            Base: Instance of the class with attributes set from
                  the dictionary.
        """
        from models.rectangle import Rectangle
        from models.square import Square

        dummy_instance = None
        if cls.__name__ == "Rectangle":
            # Dummy instance for Rectangle with mandatory attributes
            dummy_instance = Rectangle(1, 1)
        elif cls.__name__ == "Square":
            # Dummy instance for Square with mandatory attributes
            dummy_instance = Square(1)

        if dictionary:
            dummy_instance.update(**dictionary)

        return dummy_instance

    @classmethod
    def load_from_file(cls):
        """
        Load instances from a JSON file and return a list of instances.

        Returns:
            list: List of instances loaded from the JSON file.
        """
        filename = "{}.json".format(cls.__name__)
        try:
            with open(filename, "r") as file:
                content = file.read()
                list_dicts = cls.from_json_string(content)
                list_instances = [cls.create(**item) for item in list_dicts]
                return list_instances
        except FileNotFoundError:
            return []

    @classmethod
    def save_to_file_csv(cls, list_objs):
        """
        Save a list of instances to a CSV file.

        Args:
            list_objs (list): List of instances to be saved.
        """
        filename = "{}.csv".format(cls.__name__)
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            if list_objs is not None:
                for obj in list_objs:
                    if cls.__name__ == "Rectangle":
                        row = [obj.id, obj.width, obj.height, obj.x, obj.y]
                    elif cls.__name__ == "Square":
                        row = [obj.id, obj.size, obj.x, obj.y]
                    writer.writerow(row)

    @classmethod
    def load_from_file_csv(cls):
        """
        Load a list of instances from a CSV file.

        Returns:
            list: List of instances loaded from the CSV file.
        """
        filename = "{}.csv".format(cls.__name__)
        instances = []
        try:
            with open(filename, "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if cls.__name__ == "Rectangle":
                        instance = cls.create(
                            id=int(row[0]), width=int(row[1]),
                            height=int(row[2]), x=int(row[3]), y=int(row[4])
                            )
                    elif cls.__name__ == "Square":
                        instance = cls.create(
                            id=int(row[0]), size=int(row[1]),
                            x=int(row[2]), y=int(row[3])
                            )
                    instances.append(instance)
        except FileNotFoundError:
            pass  # If the file doesn't exist, return an empty list
        return instances

    @staticmethod
    def draw(list_rectangles, list_squares):
        """
        Opens a window and draws all the Rectangles and Squares using
        Turtle graphics.

        Args:
            list_rectangles (list): List of Rectangle instances.
            list_squares (list): List of Square instances.
        """
        screen = turtle.Screen()
        screen.bgcolor("white")
        screen.title("Draw Rectangles and Squares")

        pen = turtle.Turtle()
        pen.speed(2)

        for rect in list_rectangles:
            pen.penup()
            pen.goto(rect.x, rect.y)
            pen.pendown()
            pen.color("blue")
            pen.forward(rect.width)
            pen.left(90)
            pen.forward(rect.height)
            pen.left(90)
            pen.forward(rect.width)
            pen.left(90)
            pen.forward(rect.height)
            pen.left(90)

        for square in list_squares:
            pen.penup()
            pen.goto(square.x, square.y)
            pen.pendown()
            pen.color("red")
            pen.forward(square.size)
            pen.left(90)
            pen.forward(square.size)
            pen.left(90)
            pen.forward(square.size)
            pen.left(90)
            pen.forward(square.size)
            pen.left(90)

        turtle.done()
