from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages  # import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView


from store.forms import SignUpForm, LoginForm
from .models import Products, Image, User


def sign_up(request):
    print(request)
    if request.POST:
        form = SignUpForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=password,)
            login(request, user)
            return redirect('buy')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, 'store/register.html', {'form': SignUpForm(), 'error': "error_message"})


def sign_in(request):
    error = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/buy/")
                return HttpResponse('Disabled account')
            error = 'Invalid login or password'
    return render(request, 'store/login.html', {'form': LoginForm(), "error": error})


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

