from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from .models import Task







# login in todos list
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')











class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


# register form  view
# class RegisterPage(FormView):
#     template_name = 'base/register.html'
#     form_class = UserCreationForm
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('tasks')
#
#     def form_valid(self, form):
#         user=form.save()
#         if user is not None:
#             login(self.request,user)
#         return super(RegisterPage, self).form_valid(form)












class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the form data
        form.save()
        # Authenticate the user
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        # Log in the user
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        return super(RegisterPage, self).get(*args, **kwargs)












# To show a list of tasks
class Tasklist(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    # def get_context_data(self, **kwargs):
    #     context = super(Tasklist, self).get_context_data(**kwargs)
    #     context['tasks'] = context['tasks'].filter(user=self.request.user)
    #     context['count'] = context['tasks'].filter(complete=False).count()
    #     return context

    def get_context_data(self, **kwargs):
        context = super(Tasklist, self).get_context_data(**kwargs)
        tasks = context['tasks'].filter(user=self.request.user)
        context['tasks'] = tasks
        context['count'] = tasks.filter(complete=False).count()

        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith=search_input)
        context['search_input'] = search_input
        return context











# to show a detail view of a particular task
class Taskdetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'









# to create the new task and to the list
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)








# update the particular task content
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')











# delete the particular task  from the list and database

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
