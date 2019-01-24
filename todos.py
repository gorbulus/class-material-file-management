import json
from pathlib import Path
from datetime import date

# class to create a directory to house certain categories
# i.e. "shopping", "hw"
# each category has its own JSON file with the todo items in each
class TodoManager(object):
    STATUS_ALL = 'all'
    STATUS_DONE = 'done'
    STATUS_PENDING = 'pending'
    CATEGORY_GENERAL = 'general'

    def __init__(self, base_todos_path, create_dir=True):
        self.base_todos_path = base_todos_path
        self.path = Path(self.base_todos_path)
        # if the path already exists, and is not a directory
        # (files could have the same name - checks for directory clash)
        if self.path.exists() and not self.path.is_dir():
            raise ValueError("{} path is invalid.".format(base_todos_path))
        if not self.path.exists():
            raise ValueError("{} does not exist.".format(base_todos_path))
        self.path.mkdir(parents=True)

    def list(self, status=STATUS_ALL, category=CATEGORY_GENERAL):
        todos = {}
        for todo_path in self.path.glob("*.json"):
            print(todo_path)
            with todo_path.open("r") as fp:
                document = json.load(fp)
                # if either of these keys are not in this document...
                if "category_name" not in document or "todos" not in document:
                    raise ValueError("Invalid JSON todo format.")
                # if keys are found, store new todo in the proper json file
                category_todos = []
                # iterate through the todos in the json file
                for todo in document["todos"]:
                    # checks if status in the todo item
                    if status == self.STATUS_ALL or todo["status"] == status:
                        category_todos.appens(todo)
                    # new todos output dict
                    # new key "category_name"
                    todos[document["category_name"]] = category_todos       
        return todos

    def new(self, task, category=CATEGORY_GENERAL, description=None,
            due_on=None):

        if due_on:
            if type(due_on) == date:
                due_on = due_on.isoformat()
            elif type(due_on) == str:
                # all good
                pass
            else:
                raise ValueError('Invalid due_on type. Must be date or str')

        todo_file_name = "{}.json".format(category)
        # tags on new json file extension
        path = self.path / todo_file_name
        
        todos = {
            "category_name" : category.title(),
            "todos" : []
        }
        
        if path.exists():
            with path.open("r") as fp:
                todos = json.load(fp)
        todo = {
            "task" : task,
            "description" : description,
            "due_on" : due_on,
            "status" : self.STATUS_PENDING
        }
        
        # append the new "todo"
        todos["todos"].append(todo)
        
        # writing todos to json file
        # using dump
        with path.open("w") as fp:
            todos = json.dump(todos, fp, indent=2)
