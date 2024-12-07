from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

# View to list tasks
def task_list(request):
    tasks = Task.objects.all()  # Fetch all tasks
    return render(request, 'taskmanager/task_list.html', {'tasks': tasks})

# View to add a task
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()  # Save the task to the database
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'taskmanager/add_task.html', {'form': form})

# View to delete a task
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'taskmanager/delete_task.html', {'task': task})
