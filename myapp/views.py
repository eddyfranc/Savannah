# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django import forms
from .models import Customer

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = Customer
        fields = ("username", "email", "phone", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # create session
            return redirect("/")  # or wherever
    else:
        form = SignupForm()
    return render(request, "myapp/signup.html", {"form": form})
