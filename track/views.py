from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, DeleteView

from .models import Application, Company
from .forms import NewApplicationForm, NewCompanyForm, UpdateApplicationForm, LoginForm, DeleteApplicationForm

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
        tester = Application.objects.filter(Q(position__icontains='tester') | Q(position__icontains='QA'))
        developer = Application.objects.filter(Q(position__icontains='developer') | Q(position__icontains='python') | Q(position__icontains='django'))
        intern = Application.objects.filter(Q(position__icontains='intern') | Q(position__icontains='internship'))
        resumes = Application.objects.filter(user=self.request.user).order_by('-date')
        considered = Application.objects.filter(user=self.request.user).filter(result='under consideration').order_by('-date')
        rejected = Application.objects.filter(user=self.request.user).filter(result='rejected').order_by('-date')
        return render(request, self.template_name, {'resumes': resumes, 'considered': considered, 'rejected': rejected, 'tester': tester, 'developer': developer, 'intern': intern})


class NewApplication(LoginRequiredMixin, FormView):
    template_name = 'track/new_application.html'
    model = Application
    form_class = NewApplicationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        last_id = Application.objects.count()
        cd = form.cleaned_data
        user = User.objects.get(username=self.request.user.username)
        Application.objects.create(id=last_id+4, user=user, date=cd['date'], company=cd['company'], position=cd['position'],
                                   application_amount=cd['application_amount'], localization=cd['localization'], result=cd['result'] )
        return super().form_valid(form)



class NewCompany(LoginRequiredMixin, FormView):
    template_name = 'track/new_company.html'
    model = Application
    form_class = NewCompanyForm
    success_url = reverse_lazy('new_app')

    def form_valid(self, form):
        last_id = Company.objects.count()
        name = form.cleaned_data['name']
        if Company.objects.filter(name=name).exists():
            messages.error(self.request, f'The {name} company name already exists!')
        else:
            Company.objects.create(id=last_id+4, name=name)
        return super().form_valid(form)


class UpdateApplication(LoginRequiredMixin, UpdateView):
    template_name = 'track/update.html'
    model = Application
    success_url = reverse_lazy('dashboard')
    form_class = UpdateApplicationForm


class DeleteApplicationView(LoginRequiredMixin, DeleteView):
    template_name = 'track/track_confirm_delete.html'
    model = Application
    form_class = DeleteApplicationForm
    success_url = reverse_lazy('dashboard')

