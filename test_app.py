import typer
from typer.testing import CliRunner
from todocli import app
from database import get_all_todos

runner = CliRunner()

def test_add():
    result = runner.invoke(app, ["add", "Write tests", "Development"])
    assert result.exit_code == 0
    assert "adding Write tests, Development" in result.output
    
    tasks = get_all_todos()
    assert any(task.task == "Write tests" and task.category == "Development" for task in tasks)

def test_delete():
    runner.invoke(app, ["add", "Sample task", "Testing"])
    tasks_before = get_all_todos()
    initial_count = len(tasks_before)
    
    result = runner.invoke(app, ["delete", str(initial_count)])
    assert result.exit_code == 0
    assert "deleting" in result.output
    
    tasks_after = get_all_todos()
    assert len(tasks_after) == initial_count - 1

def test_update():
    runner.invoke(app, ["add", "Initial task", "Work"])
    result = runner.invoke(app, ["update", "1", "--task", "Updated task", "--category", "Updated Category"])
    assert result.exit_code == 0
    assert "updating 1" in result.output
    
    tasks = get_all_todos()
    assert tasks[0].task == "Updated task"
    assert tasks[0].category == "Updated Category"

def test_complete():
    runner.invoke(app, ["add", "Task to complete", "Misc"])
    result = runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0
    assert "complete 1" in result.output
    
    tasks = get_all_todos()
    assert tasks[0].status == 2

def test_show():
    result = runner.invoke(app, ["show"])
    assert result.exit_code == 0
    assert "Todos!" in result.output
