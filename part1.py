from abc import ABC, abstractmethod
from typing import List


# Shape interface
class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def get_type(self):
        pass


# Concrete Shape: Square
class Square(Shape):
    def __init__(self, id):
        self.id = id
        self.shapes = []

    def draw(self):
        print(f"Square {self.id} drawn.")

    def get_id(self):
        return self.id

    def get_type(self):
        return "Square"

    def add_shape(self, shape):
        self.shapes.append(shape)

    def display_shapes(self):
        print("Shapes inside Square", self.id, ":")
        for shape in self.shapes:
            print(f"- {shape.get_type()} {shape.get_id()}")


# Concrete Shape: Rectangle
class Rectangle(Shape):
    def __init__(self, id):
        self.id = id
        self.shapes = []

    def draw(self):
        print(f"Rectangle {self.id} drawn.")

    def get_id(self):
        return self.id

    def get_type(self):
        return "Rectangle"

    def add_shape(self, shape):
        self.shapes.append(shape)

    def display_shapes(self):
        print("Shapes inside Rectangle", self.id, ":")
        for shape in self.shapes:
            print(f"- {shape.get_type()} {shape.get_id()}")


# Concrete Shape: Circle
class Circle(Shape):
    def __init__(self, id):
        self.id = id
        self.shapes = []

    def draw(self):
        print(f"Circle {self.id} drawn.")

    def get_id(self):
        return self.id

    def get_type(self):
        return "Circle"

    def add_shape(self, shape):
        self.shapes.append(shape)

    def display_shapes(self):
        print("Shapes inside Circle", self.id, ":")
        for shape in self.shapes:
            print(f"- {shape.get_type()} {shape.get_id()}")


# Concrete Shape: Oval
class Oval(Shape):
    def __init__(self, id):
        self.id = id

    def draw(self):
        print(f"Oval {self.id} drawn.")

    def get_id(self):
        return self.id

    def get_type(self):
        return "Oval"


# Concrete Shape: Triangle
class Triangle(Shape):
    def __init__(self, id):
        self.id = id

    def draw(self):
        print(f"Triangle {self.id} drawn.")

    def get_id(self):
        return self.id

    def get_type(self):
        return "Triangle"


# CompositeShape class for our canvas
class CompositeShape(Shape):
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def remove_shape(self, shape):
        self.shapes.remove(shape)

    def remove_shape_by_id(self, shape_id):
        for shape in self.shapes:
            if shape.get_id() == shape_id:
                self.shapes.remove(shape)
                return shape
        return None

    def draw(self):
        for shape in self.shapes:
            shape.draw()

    def get_id(self):
        return -1  # Not applicable for the composite shape

    def get_type(self):
        return "CompositeShape"

    def display_canvas(self):
        print("Shapes on Canvas:")
        for shape in self.shapes:
            print(f"- {shape.get_type()} {shape.get_id()}")

    def get_shape_by_id(self, shape_id):
        for shape in self.shapes:
            if shape.get_id() == shape_id:
                return shape
            elif isinstance(shape, CompositeShape):
                found_shape = shape.get_shape_by_id(shape_id)
                if found_shape:
                    return found_shape
        return None


# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# Add command class
class AddCommand(Command):
    def __init__(self, canvas, shape, parent_id=None):
        self.canvas = canvas
        self.shape = shape
        self.parent_id = parent_id

    def execute(self):
        if self.parent_id is None:
            self.canvas.add_shape(self.shape)
            print(f"Shape {self.shape.get_type()} {self.shape.get_id()} added to canvas.")
        else:
            parent_shape = self.canvas.get_shape_by_id(self.parent_id)
            if parent_shape:
                parent_shape.add_shape(self.shape)
                print(f"Shape {self.shape.get_type()} {self.shape.get_id()} added inside {parent_shape.get_type()} {parent_shape.get_id()}.")
            else:
                print(f"No shape found with ID {self.parent_id}.")


# Remove command class
class RemoveShapeCommand(Command):
    def __init__(self, canvas):
        self.canvas = canvas

    def execute(self):
        print("Enter the ID of the shape you want to remove:")
        shape_id_to_remove = int(input())
        shape_to_remove = self.canvas.get_shape_by_id(shape_id_to_remove)
        if shape_to_remove:
            self.canvas.remove_shape(shape_to_remove)
            print(f"Shape {shape_to_remove.get_type()} {shape_to_remove.get_id()} removed.")
        else:
            print(f"No shape found with ID {shape_id_to_remove}.")


# Main class: CanvasApp
class CanvasApp:
    def __init__(self):
        self.canvas = CompositeShape()
        self.command_history = []
        self.redo_history = []

    def execute_command(self, command):
        command.execute()
        self.command_history.append(command)
        self.redo_history.clear()

    def undo(self):
        if self.command_history:
            last_command = self.command_history.pop()
            if isinstance(last_command, AddCommand):
                removed_shape = self.canvas.remove_shape_by_id(last_command.shape.get_id())
                if removed_shape:
                    print(f"Shape {removed_shape.get_type()} {removed_shape.get_id()} removed.")
            elif isinstance(last_command, RemoveShapeCommand):
                added_shape = last_command.shape
                self.canvas.add_shape(added_shape)
                print(f"Shape {added_shape.get_type()} {added_shape.get_id()} added back.")
            self.redo_history.append(last_command)
        else:
            print("Nothing to undo.")

    def redo(self):
        if self.redo_history:
            redo_command = self.redo_history.pop()
            redo_command.execute()
            self.command_history.append(redo_command)
            if isinstance(redo_command, AddCommand):
                added_shape = redo_command.shape
                print(f"Shape {added_shape.get_type()} {added_shape.get_id()} added.")
            elif isinstance(redo_command, RemoveShapeCommand):
                removed_shape = redo_command.shape
                print(f"Shape {removed_shape.get_type()} {removed_shape.get_id()} removed.")
        else:
            print("Nothing to redo.")

    def get_shape_by_id(self, shape_id, shapes=None):
        if shapes is None:
            shapes = self.canvas.shapes
        for shape in shapes:
            if isinstance(shape, CompositeShape):
                sub_shape = self.get_shape_by_id(shape_id, shape.shapes)
                if sub_shape:
                    return sub_shape
            elif shape.get_id() == shape_id:
                return shape
        return None


if __name__ == "__main__":
    canvas_app = CanvasApp()

    while True:
        print("Choose an option:")
        print("1. Add shape to canvas")
        print("2. Add shape inside another shape")
        print("3. Remove shape from canvas")
        print("4. Display canvas")
        print("5. Undo")
        print("6. Redo")
        print("7. Exit")

        option = input("Enter option number: ")

        if option == "7":
            break

        if option == "1":
            print("Enter shape type (rectangle/circle/square/oval/triangle):")
            shape_type = input()
            print("Enter shape ID:")
            shape_id = int(input())
            shape = None
            if shape_type == "rectangle":
                shape = Rectangle(shape_id)
            elif shape_type == "circle":
                shape = Circle(shape_id)
            elif shape_type == "square":
                shape = Square(shape_id)
            elif shape_type == "oval":
                shape = Oval(shape_id)
            elif shape_type == "triangle":
                shape = Triangle(shape_id)
            else:
                print("Invalid shape type.")
                continue

            command = AddCommand(canvas_app.canvas, shape)
            canvas_app.execute_command(command)

        elif option == "2":
            print("Enter shape type (rectangle/circle/square/oval/triangle):")
            shape_type = input()
            print("Enter shape ID:")
            shape_id = int(input())
            shape = None
            if shape_type == "rectangle":
                shape = Rectangle(shape_id)
            elif shape_type == "circle":
                shape = Circle(shape_id)
            elif shape_type == "square":
                shape = Square(shape_id)
            elif shape_type == "oval":
                shape = Oval(shape_id)
            elif shape_type == "triangle":
                shape = Triangle(shape_id)
            else:
                print("Invalid shape type.")
                continue

            print("Enter the ID of the shape in which you want to add this shape (or press Enter to add to canvas):")
            parent_id_input = input()
            parent_id = int(parent_id_input) if parent_id_input.strip() else None
            command = AddCommand(canvas_app.canvas, shape, parent_id)
            canvas_app.execute_command(command)

        elif option == "3":
            command = RemoveShapeCommand(canvas_app.canvas)
            canvas_app.execute_command(command)

        elif option == "4":
            canvas_app.canvas.display_canvas()

        elif option == "5":
            canvas_app.undo()

        elif option == "6":
            canvas_app.redo()

        else:
            print("Invalid option.")
