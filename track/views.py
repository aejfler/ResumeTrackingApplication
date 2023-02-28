from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, UpdateView

from .models import Application, Company
from .forms import NewApplicationForm, NewCompanyForm, UpdateApplicationForm, LoginForm

User = get_user_model()


class LoginView(FormView):
    template_name = 'track/loginTemplate.html'
    success_url = reverse_lazy('dashboard')
    form_class = LoginForm

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'track/dashboard.html'
    model = Application
    context_object_name = 'resumes'

    def get(self, request, *args, **kwargs):
        resumes = Application.objects.filter(user=self.request.user).order_by('-date')
        considered = Application.objects.filter(user=self.request.user).filter(result='under consideration').order_by('-date')
        rejected = Application.objects.filter(user=self.request.user).filter(result='rejected').order_by('-date')
        return render(request, self.template_name, {'resumes': resumes, 'considered': considered, 'rejected': rejected})


class NewApplication(LoginRequiredMixin, FormView):
    template_name = 'track/new_application.html'
    model = Application
    form_class = NewApplicationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        last_id = Application.objects.count()
        cd = form.cleaned_data
        user = User.objects.get(username=self.request.user.username)
        Application.objects.create(id=last_id+2, user=user, date=cd['date'], company=cd['company'], position=cd['position'],
                                   application_amount=cd['application_amount'], localization=cd['localization'], result=cd['result'] )
        return super().form_valid(form)



class NewCompany(LoginRequiredMixin, FormView):
    template_name = 'track/new_company.html'
    model = Application
    form_class = NewCompanyForm
    success_url = reverse_lazy('new_app')

    def form_valid(self, form):
        last_id = Company.objects.count()
        cd = form.cleaned_data
        Company.objects.create(id=last_id+1, name=cd['name'])
        return super().form_valid(form)


class UpdateApplication(LoginRequiredMixin, UpdateView):
    template_name = 'track/update.html'
    model = Application
    success_url = reverse_lazy('dashboard')
    form_class = UpdateApplicationForm




