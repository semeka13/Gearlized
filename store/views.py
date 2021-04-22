from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib import messages  # import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView


from store.forms import SignUpForm
from .models import Products, Image, User


def sign_up(request):
    print(request)
    if request.POST:
        form = SignUpForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password,)
            login(request, user)
            return redirect('buy')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, 'store/register.html', {'form': SignUpForm()})


class MainView(TemplateView):
    template_name = "store/buy.html"

    def get(self, request):
        # if request.user.is_authencitated:
        products = Products.objects.all()
        users = User.objects.all()
        data = list()
        for product in products:
            images = Image.objects.filter(product=product).all()
            data.append({"data": product, "images": images})
        ctx = {"products": data, "users": users}
        return render(request, self.template_name, ctx)


class LoginView(FormView):
    form_class = SignUpForm
    success_url = "/buy/"
    template_name = "store/login.html"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/buy/")


class AddProduct(CreateView):

    fields = ["type", "model", "brand", "size", "condition", "season", "price", "extra_info"]
    model = Products
    success_url = "/buy/"
    template_name = "store/sell.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.seller = self.request.user
        self.object.save()
        return redirect(self.success_url)

