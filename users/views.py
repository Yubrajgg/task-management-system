from django.contrib.auth.decorators import user_passes_test
from tasks.models import Task
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import CustomUser as User
from .forms import CustomUserCreationForm

@user_passes_test(lambda u: u.is_admin_user())
def admin_dashboard(request):
    users = User.objects.all().prefetch_related('task_set')
    return render(request, 'users/admin_dashboard.html', {'users': users})

@user_passes_test(lambda u: u.is_admin_user())
def user_tasks(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(created_by=user)
    return render(request, 'users/user_tasks.html', {'user': user, 'tasks': tasks})

@login_required
def user_dashboard(request):
    if request.user.is_admin():
        return redirect('admin_dashboard')
    user = request.user
    tasks = Task.objects.filter(created_by=user)
    return render(request, 'users/user_dashboard.html', {'user': user, 'tasks': tasks})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
