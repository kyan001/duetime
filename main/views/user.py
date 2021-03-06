from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


def userSignup(request):
    username = request.POST.get('username') or None
    password = request.POST.get('password') or None
    email = request.POST.get('email') or None
    if request.POST:
        if not username or not password:
            messages.error(request, _("Username / Password cannot be empty"))
        elif User.objects.filter(username=username).exists():
            messages.error(request, _("The username ({}) is taken").format(username))
        elif User.objects.filter(email=email).exists():
            messages.error(request, _("The email ({}) is taken").format(email))
        else:
            with transaction.atomic():
                user = User.objects.create_user(username=username)
                user.set_password(password)
                user.email = email
                user.save()
                messages.success(request, _("Sign up success. Please log in"))
                return redirect("/user/signin")
    return render(request, "user/signup.html")
