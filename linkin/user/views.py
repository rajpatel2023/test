from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import Usersignup, userprofileform
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Profile, matchmodel
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models import Count, F, Value, Q
from django.core.paginator import Paginator

# Create your views here.


class home(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        data = Profile.objects.filter(user=user).values()
        return render(request, "user/home.html", {"data": data})


class profile(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        data = Profile.objects.get(user=user)
        form = userprofileform(instance=data)
        return render(request, "user/profile.html", {"form": form})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        instance = Profile.objects.get(user=user)
        form = userprofileform(request.POST, request.FILES, instance=instance)
        user_image = request.FILES.get("photo")

        # image check
        if user_image:
            user_image_size = user_image.size
            user_image_name, extention = user_image.name.split(".")
            if user_image_size > 2097152 or extention != "jpg":
                error = {
                    "photo": "check if its jpg image and size less then 2MB",
                }
                # add error
                form.errors.update(error)
                return render(
                    request,
                    "user/profile.html",
                    {"form": form, "error": ""},
                )

        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request, "user/profile.html", {"form": form, "error": form})


class match(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)

        userdata = Profile.objects.filter(user=user).values()[0]

        data = Profile.objects.annotate(
            numberss=Count("city", filter=Q(city=userdata["city"]))
            + Count("state", filter=Q(state=userdata["state"]))
            + Count("country", filter=Q(country=userdata["country"]))
            + Count("cast", filter=Q(cast=userdata["cast"]))
            + Count("subcast", filter=Q(subcast=userdata["subcast"]))
            + Count("profation", filter=Q(profation=userdata["profation"]))
            + Count("address", filter=Q(address=userdata["address"]))
        ).order_by("-numberss")
        paginator = Paginator(data, 2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "user/match.html", {"data": page_obj})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        join_user_id = request.POST.get("user_id")
        join_user = Profile.objects.get(id=join_user_id)
        join_user_object = User.objects.get(id=join_user.user_id)
        raj = matchmodel.objects.create(base_user=user, match_user=join_user_object)
        return redirect("home")


class friends(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        data = matchmodel.objects.filter(base_user=user)
        paginator = Paginator(data, 2)
        page_number = request.GET.get("page")
        data = paginator.get_page(page_number)
        return render(request, "user/friends.html", {"data": data})


class signup(View):
    def get(self, request, *args, **kwargs):
        form = Usersignup()
        return render(request, "user/signup.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = Usersignup(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(
                request, "user/signup.html", {"form": form, "error": form.error}
            )


def signup(request):
    if request.method == "POST":
        form = Usersignup(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            return redirect("home")

    else:
        form = Usersignup()
    return render(request, "user/signup.html", {"form": form})
