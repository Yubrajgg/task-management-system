
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from users.models import CustomUser as User

@login_required
def task_list(request):
    tasks = Task.objects.filter(created_by=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status', 'todo')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        attachment = request.FILES.get('attachment')
        
        task = Task.objects.create(
            title=title,
            description=description,
            status=status,
            created_by=request.user,
            assigned_to=User.objects.get(id=assigned_to_id) if assigned_to_id else None,
            due_date=due_date if due_date else None,
            attachment=attachment
        )
        return redirect('task_detail', pk=task.pk)
    users = User.objects.all()
    return render(request, 'tasks/task_form.html', {'users': users})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        assigned_to_id = request.POST.get('assigned_to')
        task.assigned_to = User.objects.get(id=assigned_to_id) if assigned_to_id else None
        task.due_date = request.POST.get('due_date')
        
        # Handle status change to completed
        if task.status == 'done':
            task.save()
            return redirect('task_list')
        
        if request.FILES.get('attachment'):
            task.attachment = request.FILES['attachment']
        task.save()
        return redirect('task_detail', pk=task.pk)
    users = User.objects.all()
    return render(request, 'tasks/task_form.html', {'task': task, 'users': users})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    task.delete()
    return redirect('task_list')
