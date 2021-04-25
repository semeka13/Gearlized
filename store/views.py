from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages  # import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView


from store.forms import SignUpForm, LoginForm, AddProductForm
from .models import Products, Image, User


def sign_up(request):
    print(request)
    errors = ""
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
        errors = form.errors
    return render(request, 'store/register.html', {'form': SignUpForm(), 'error': errors})


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


def add_product(request):
    if request.POST and request.FILES["file"]:

        condition = request.POST.get("condition")
        brand = request.POST.get("brand")
        year = request.POST.get("year")
        model = request.POST.get("model")
        size = request.POST.get("size")
        extra_info = request.POST.get("extra_info")
        price = request.POST.get("price")
        # file = request.POST.get("file")
        user = request.user
        product = Products(condition=condition, brand=brand,
                           season=year, model=model, size=size,
                           price=price, extra_info=extra_info,
                           seller=user)
        product.save()
        file = request.FILES["file"]
        fs = FileSystemStorage(location='./static/product_pictures')
        filename = fs.save(file.name, file)
        image = Image(product=product, picture=file)
        image.save()

        return redirect('buy')
    messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, 'store/sell.html', {'form': AddProductForm(), 'error': "error_message"})


def product_view(request, product_id):
    product = Products.objects.get(id=product_id)
    user = product.seller
    images = [Image.objects.get(product=product)]
    images_url = [image.picture for image in images]
    data = {"product": product, "user": user, "images": images_url}
    return render(request, 'store/product_info.html', data)


class MainView(TemplateView):
    template_name = "store/buy.html"

    def get(self, request):
        # if request.user.is_authencitated:
        products = Products.objects.all()
        users = User.objects.all()
        data = list()
        for product in products:
            images = Image.objects.filter(product=product).all()
            data.append({"data": product, "images": images, "link": f"http://127.0.0.1:8000/buy/{product.id}"})
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

