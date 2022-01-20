from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.views.generic import View
from django.contrib import messages

from .forms import LoginForm, SignUpForm


class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect("pages:index")

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Successfully logged in as {request.user.username}')
                return redirect(request.GET.get('next', 'pages:index'))
            else:
                messages.error(request, "Invalid username or password")
                return redirect("accounts:login")
        else:
            form = self.form_class()
            messages.success(request, f'An error has occurred')
            return render(request, self.template_name, {'form': form})


class SignUpView(View):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect("pages:index")

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('pages:index')
        else:
            print(form.errors)
            messages.error(request, 'Invalid form fields')
            return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('accounts:login')
