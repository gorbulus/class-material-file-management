import json
import pytest
import shutil

from pathlib import Path
from datetime import date

from todos import TodoManager


TESTING_PATH = '__todos_testing'

# fixture - predefined rules for certain functions
# you could exclude some tests 
@pytest.fixture
def path():
    return Path(TESTING_PATH)


@pytest.fixture
def todos_dir_empty(path):
    path.mkdir()

    yield path

    shutil.rmtree(str(path.absolute()))

# we add json files to the new created "__todo_testing" dir
#  "__todo_testing"
#   programming.json
#   reviews.json

@pytest.fixture
def todos_with_categories(todos_dir_empty):
    cat1 = todos_dir_empty / 'programming.json'
    cat2 = todos_dir_empty / 'reviews.json'

    with cat1.open('w') as fp:
        # adds the data to the json file "programming.json" as a string json object
        json.dump({
            'category_name': 'Programming',
            'todos': [{
                'task': 'Practice Pathlib',
                'description': 'Investigate Pathlib and file creation',
                'due_on': '2018-03-25',
                'status': 'pending'
            }, {
                'task': 'Finish rmotrgram',
                'description': 'Finish before class to start reviewing',
                'due_on': '2018-03-21',
                'status': 'done'
            }]
            # indicates the "cat1" file
        }, fp, indent=2)

    with cat2.open('w') as fp:
        # adds the data to the json file "programming.json" as a string json object
        json.dump({
            'category_name': 'Reviews',
            'todos': [{
                'task': 'Review rmotrgram',
                'description': 'Finish review before weekend',
                'due_on': '2018-03-28',
                'status': 'pending'
            }]
            # indicates the "cat2" file
        }, fp, indent=2)

    return todos_dir_empty


def test_todos_dir_is_created(path):
    assert not path.exists()

    manager = TodoManager(TESTING_PATH)
    assert path.exists()
    assert path.is_dir()

    # Clean up
    shutil.rmtree(str(path.absolute()))


def test_todo_list_status_all(todos_with_categories):
    manager = TodoManager(TESTING_PATH)
    todos = manager.list()
    assert todos == {
        'Programming': [{
            'task': 'Practice Pathlib',
            'description': 'Investigate Pathlib and file creation',
            'due_on': '2018-03-25',
            'status': 'pending'
        }, {
            'task': 'Finish rmotrgram',
            'description': 'Finish before class to start reviewing',
            'due_on': '2018-03-21',
            'status': 'done'
        }],
        'Reviews': [{
            'task': 'Review rmotrgram',
            'description': 'Finish review before weekend',
            'due_on': '2018-03-28',
            'status': 'pending'
        }]
    }


def test_todo_list_status_pending(todos_with_categories):
    manager = TodoManager(TESTING_PATH)
    todos = manager.list(status=TodoManager.STATUS_PENDING)
    assert todos == {
        'Programming': [{
            'task': 'Practice Pathlib',
            'description': 'Investigate Pathlib and file creation',
            'due_on': '2018-03-25',
            'status': 'pending'
        }],
        'Reviews': [{
            'task': 'Review rmotrgram',
            'description': 'Finish review before weekend',
            'due_on': '2018-03-28',
            'status': 'pending'
        }]
    }


def test_todo_list_status_done(todos_with_categories):
    manager = TodoManager(TESTING_PATH)
    todos = manager.list(status=TodoManager.STATUS_DONE)
    assert todos == {
        'Programming': [{
            'task': 'Finish rmotrgram',
            'description': 'Finish before class to start reviewing',
            'due_on': '2018-03-21',
            'status': 'done'
        }],
        'Reviews': []
    }


def test_create_new_todo_general_empty_dir_default_vals(todos_dir_empty):
    manager = TodoManager(TESTING_PATH)
    manager.new('New Testing Task')

    general_todos_path = todos_dir_empty / 'general.json'

    assert general_todos_path.exists()
    with general_todos_path.open('r') as fp:
        todos = json.load(fp)

    assert todos == {
        'category_name': 'General',
        'todos': [{
            'task': 'New Testing Task',
            'description': None,
            'due_on': None,
            'status': 'pending'
        }]
    }


def test_create_new_todo_general_empty_dir_due_str(todos_dir_empty):
    manager = TodoManager(TESTING_PATH)
    manager.new(
        'New Testing Task',
        description='A new task to test...',
        due_on='2018-03-28')

    general_todos_path = todos_dir_empty / 'general.json'

    assert general_todos_path.exists()
    with general_todos_path.open('r') as fp:
        todos = json.load(fp)

    assert todos == {
        'category_name': 'General',
        'todos': [{
            'task': 'New Testing Task',
            'description': 'A new task to test...',
            'due_on': '2018-03-28',
            'status': 'pending'
        }]
    }


def test_create_new_todo_general_empty_dir_due_date(todos_dir_empty):
    manager = TodoManager(TESTING_PATH)
    manager.new(
        'New Testing Task',
        description='A new task to test...',
        due_on=date(2018, 3, 1))

    general_todos_path = todos_dir_empty / 'general.json'

    assert general_todos_path.exists()
    with general_todos_path.open('r') as fp:
        todos = json.load(fp)

    assert todos == {
        'category_name': 'General',
        'todos': [{
            'task': 'New Testing Task',
            'description': 'A new task to test...',
            'due_on': '2018-03-01',
            'status': 'pending'
        }]
    }


def test_create_new_todo_other_category_empty_dir(todos_dir_empty):
    manager = TodoManager(TESTING_PATH)
    manager.new(
        'New Testing Task',
        category='programming',
        description='A new task to test...',
        due_on=date(2018, 3, 1))

    general_todos_path = todos_dir_empty / 'programming.json'

    assert general_todos_path.exists()
    with general_todos_path.open('r') as fp:
        todos = json.load(fp)

    assert todos == {
        'category_name': 'Programming',
        'todos': [{
            'task': 'New Testing Task',
            'description': 'A new task to test...',
            'due_on': '2018-03-01',
            'status': 'pending'
        }]
    }


def test_create_new_todo_with_existing_todos(todos_with_categories):
    manager = TodoManager(TESTING_PATH)
    manager.new(
        'New Testing Task',
        category='programming',
        description='A new task to test...',
        due_on=date(2018, 3, 1))

    general_todos_path = todos_with_categories / 'programming.json'

    assert general_todos_path.exists()
    with general_todos_path.open('r') as fp:
        todos = json.load(fp)

    assert todos == {
        'category_name': 'Programming',
        'todos': [{
            'task': 'Practice Pathlib',
            'description': 'Investigate Pathlib and file creation',
            'due_on': '2018-03-25',
            'status': 'pending'
        }, {
            'task': 'Finish rmotrgram',
            'description': 'Finish before class to start reviewing',
            'due_on': '2018-03-21',
            'status': 'done'
        }, {  # New todo:
            'task': 'New Testing Task',
            'description': 'A new task to test...',
            'due_on': '2018-03-01',
            'status': 'pending'
        }]
    }
