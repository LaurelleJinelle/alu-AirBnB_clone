#!/usr/bin/python3
"""Command interpreter for Holberton AirBnB project."""

import cmd
import re
from shlex import split
import ast  # Safer than eval()
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """Parses the arguments for different command formats."""
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    try:
        if curly_braces:
            lexer = split(arg[:curly_braces.span()[0]])
            return [i.strip(",") for i in lexer] + [curly_braces.group()]
        if brackets:
            lexer = split(arg[:brackets.span()[0]])
            return [i.strip(",") for i in lexer] + [brackets.group()]
        return [i.strip(",") for i in split(arg)]
    except Exception as e:
        print(f"Error parsing argument: {e}")
        return []


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Override default behavior to do nothing on empty input."""
        pass

    def default(self, arg):
        """Override default behavior for unknown commands."""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match:
            class_name, command = arg[:match.span()[0]], arg[match.span()[1]:]
            match = re.search(r"\((.*?)\)", command)
            if match:
                func_name, params = command[:match.span()[0]], match.group(1)
                if func_name in argdict:
                    return argdict[func_name]("{} {}".format(class_name, params))
        print(f"*** Unknown syntax: {arg}")
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        print("Goodbye!")
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("\nGoodbye!")
        return True

    def do_create(self, arg):
        """Create a new instance of a class."""
        try:
            if not arg:
                raise SyntaxError()
            args = arg.split(" ")
            class_name = args[0]
            kwargs = {
                k: ast.literal_eval(v.strip('"').replace("_", " ")) if '"' in v
                else ast.literal_eval(v)
                for k, v in (item.split("=") for item in args[1:])
            }
            obj = eval(class_name)(**kwargs) if kwargs else eval(class_name)()
            storage.new(obj)
            print(obj.id)
            obj.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except Exception as e:
            print(f"Error: {e}")

    def do_show(self, arg):
        """Show the details of a class instance."""
        args = parse(arg)
        objdict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            print(objdict.get(key, "** no instance found **"))

    def do_destroy(self, arg):
        """Destroy a class instance by id."""
        args = parse(arg)
        objdict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key in objdict:
                del objdict[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Display all instances of a given class or all classes."""
        args = parse(arg)
        if args and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objs = [str(obj) for obj in storage.all().values()
                    if not args or obj.__class__.__name__ == args[0]]
            print(objs)

    def do_count(self, arg):
        """Count the number of instances of a given class."""
        args = parse(arg)
        count = sum(1 for obj in storage.all().values()
                    if obj.__class__.__name__ == args[0])
        print(count)

    def do_update(self, arg):
        """Update a class instance with new attributes."""
        args = parse(arg)
        objdict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in objdict:
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            obj = objdict["{}.{}".format(args[0], args[1])]
            try:
                if type(ast.literal_eval(args[2])) == dict:
                    for k, v in ast.literal_eval(args[2]).items():
                        setattr(obj, k, v)
                else:
                    setattr(obj, args[2], ast.literal_eval(args[3]))
                storage.save()
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    try:
        HBNBCommand().cmdloop()
    except Exception as e:
        print(f"Error: {e}")
