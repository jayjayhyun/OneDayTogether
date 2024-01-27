from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.db.models import Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
class HomeView(View):
    template_name = 'index.html'
    
    def get(self, request):
        current_user = request.user.id
        destination=Destination.objects.all()
        userdata = User_Profile.objects.filter(Users=current_user)
        purchasehis=Purchase_History.objects.filter(User=current_user)
        return render(request, self.template_name, {'desdata':destination,'userdata': userdata,'purchase_history':purchasehis})
class DestinationView(View):
    template_name = 'Destination.html'

    def get(self, request):
        current_user = request.user.id
        userdata = User_Profile.objects.filter(Users=current_user)
        search_query = request.GET.get('search')
        searchdate_query = request.GET.get('searchdate')
        desdata = Destination.objects.all()
        shcedata = Schedule.objects.all().order_by('Schedule')
        purchasehis=Purchase_History.objects.filter(User=current_user)
        
        if search_query:
            desdata = desdata.filter(
                Q(destination__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if searchdate_query:
            schesearch = shcedata.filter(
                Q(Schedule__icontains=searchdate_query) 
            )
            desdata = desdata.filter(
                Q(schedule__in=schesearch.values('pk')) 
            )
        
        return render(request, self.template_name, {'desdata': desdata, 'shcedata': shcedata, 'userdata': userdata,'purchase_history':purchasehis})
class ShopView(View):
    template_name = 'shop.html'
    
    def get(self, request):
        allproducts = Shop.objects.all()
        current_user = request.user.id
        userdata = User_Profile.objects.filter(Users=current_user)
        page_num = 20
        paginator = Paginator(allproducts, page_num)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        purchasehis=Purchase_History.objects.filter(User=current_user)
        return render(request, self.template_name, {'userdata': userdata,'productdata':products,'purchase_history':purchasehis})
    def post(self, request, **kwargs):
        search_query = request.POST.get('search')
        product=Shop.objects.all()
        if search_query:
            product = product.filter(
                Q(Product_name__icontains=search_query) |
                Q(Product_Type__icontains=search_query) |
                Q(detail__icontains=search_query)
            )
        current_user = request.user.id
        page_num = 20
        userdata = User_Profile.objects.filter(Users=current_user)
        paginator = Paginator(product, page_num)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        purchasehis=Purchase_History.objects.filter(User=current_user)
        return render(request, self.template_name, {'userdata': userdata,'productdata':products,'purchase_history':purchasehis})
class ShopCategoryView(View):
    template_name = 'shop.html'
    
    def get(self, request,category):
        allproducts = Shop.objects.filter(Product_Type=category)
        current_user = request.user.id
        userdata = User_Profile.objects.filter(Users=current_user)
        page_num = 20
        paginator = Paginator(allproducts, page_num)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        purchasehis=Purchase_History.objects.filter(User=current_user)
        return render(request, self.template_name, {'category':category,'userdata': userdata,'productdata':products,'purchase_history':purchasehis})
from decimal import Decimal
from django.shortcuts import redirect
from django.views import View
from django.utils import timezone
from decimal import Decimal
from .models import User, Cart, Purchase_History

class PurchaseView(View):
    def get(self, request):
        return redirect('onedaytwogether:cart')
    
    def post(self, request, **kwargs):
        current_user = request.user.id
        userdata = User.objects.get(id=current_user)
        allitemsincart = Cart.objects.filter(Username=current_user)

        for item in allitemsincart:
            price = Decimal(item.Product_name.New_Price) * Decimal(item.Quantity)
            PurchaseHistory = Purchase_History(
                User=userdata,
                Product_name=item.Product_name,
                Amount=item.Quantity,
                Cost=price,
                Date=timezone.now()
            )
            PurchaseHistory.save()
                # Check if the product exists in the cart
        for item in allitemsincart:
            AllProduct = Shop.objects.filter(id=item.Product_name.id)
            if AllProduct.exists():
                AllProduct = AllProduct.first()
                AllProduct.Quantity -= item.Quantity
                AllProduct.save()
        allitemsincart.delete()
        return redirect('onedaytwogether:cart')
class CartView(View):
    template_name = 'cart.html'
    
    def get(self, request):
        current_user = request.user.id
        cartdata = Cart.objects.filter(Username=current_user)
        allproduct=Shop.objects.all()
        userdata = User_Profile.objects.filter(Users=current_user)
        total_price = Decimal(0)
        for cart in cartdata:
            total_price += cart.Price
        if not cartdata:
            return redirect('onedaytwogether:shop')  # Redirect to the shop
        purchasehis=Purchase_History.objects.filter(User=current_user)
        return render(request, self.template_name, {'allproduct':allproduct,'userdata': userdata, 'cartdata': cartdata, 'total_price': total_price,'purchase_history':purchasehis})
    
    def post(self, request, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('Quantity'))
        product_detail = Shop.objects.get(id=product_id)
        user = User.objects.get(id=request.user.id)

        price = product_detail.New_Price * Decimal(quantity)  # Convert quantity to Decimal
        
        # Check if the product exists in the cart
        existing_cart = Cart.objects.filter(Username=user, Product_name=product_detail)
        if existing_cart.exists():
            existing_item = existing_cart.first()
            existing_item.Quantity += quantity
            existing_item.Price += price
            existing_item.save()
        else:
            cart = Cart(
                Username=user,
                Product_name=product_detail,
                Quantity=quantity,
                Price=price
            )
            cart.save()
        
        return redirect('onedaytwogether:cart')
class CartDeleteView(View):
    template_name = 'cart.html'
    
    def get(self, request,id):      
        current_user = request.user.id
        Carts = get_object_or_404(Cart, id=id,Username=current_user)
        Carts.delete()
        return redirect('onedaytwogether:cart')
class BookingDeleteView(View):
    template_name = 'booking.html'
    
    def get(self, request,id):      
        current_user = request.user.id
        Carts = get_object_or_404(Contact, id=id,User=current_user)
        Carts.delete()
        return redirect('onedaytwogether:Booking')
class AdminBookingApproveView(View):
    def get(self, request,id):   
        if request.user.is_superuser: 
            booking = get_object_or_404(Contact, id=id)
            booking.status = True
            booking.save()
            return redirect('onedaytwogether:AdminBooking')
        else:
            return redirect('onedaytwogether:index')
class AdminBookingDeclineView(View):
    def get(self, request, id):   
        if request.user.is_superuser: 
            booking = get_object_or_404(Contact, id=id)
            booking.status = False
            booking.save()
            return redirect('onedaytwogether:AdminBooking')
        else:
            return redirect('onedaytwogether:index')
        
class ShopDetailView(View):
    template_name = 'product-detail.html'
    
    def get(self, request, id):
        current_user = request.user.id
        try:
            product = Shop.objects.get(id=id)
        except Shop.DoesNotExist:
            return redirect('onedaytwogether:shop')  # Redirect to the shop
        purchasehis=Purchase_History.objects.filter(User=current_user)
        
        userdata = User_Profile.objects.filter(Users=current_user)
        return render(request, self.template_name, {'userdata': userdata, 'productdata': product,'purchase_history':purchasehis})
class ContactView(View):
    template_name = 'contact.html'
    
    def get(self, request):
        selectdesdata=Destination.objects.filter(id=1)
        current_user = request.user.id
        userdata = User_Profile.objects.filter(Users=current_user)
        desdata = Destination.objects.all()
        shcedata=Schedule.objects.all().order_by('Schedule')
        purchasehis=Purchase_History.objects.filter(User=current_user)
        return render(request, self.template_name,{'desid':selectdesdata,'shcedata':shcedata,'desdata':desdata,'userdata': userdata,'purchase_history':purchasehis})
    def post(self, request, **kwargs):
        schedule = request.POST.get('schedule')
        desid = request.POST.get('desid')
        selectdesdata=Destination.objects.filter(id=desid)
        selectschedata=Schedule.objects.filter(id=schedule)
        current_user = request.user.id
        userdata = User_Profile.objects.filter(Users=current_user)
        desdata = Destination.objects.all()
        shcedata=Schedule.objects.all().order_by('Schedule')
        user = User.objects.get(id=request.user.id)
        
        Name = request.POST.get('Name')
        address = request.POST.get('address')
        Contactnum = request.POST.get('ContactNumber')
        email = request.POST.get('email')
        location_id = request.POST.get('Location')
        schedule_id = request.POST.get('Scheduleid')
        detail = request.POST.get('lettalk')
        member = request.POST.get('member')
        if location_id:
            
            location = Destination.objects.get(id=location_id)
            schedule = Schedule.objects.get(id=schedule_id)

            contact = Contact(
                User=user,
                Name=Name,
                Address=address,
                Members=member,
                Phone_Number=Contactnum,
                Email=email,
                Destination=location,
                Schedule=schedule,
                Details=detail,
            )
            contact.save()
        purchasehis=Purchase_History.objects.filter(User=current_user)
        return render(request, self.template_name,{'desid':selectdesdata,'schedule':selectschedata,'shcedata':shcedata,'desdata':desdata,'userdata': userdata,'purchase_history':purchasehis})
class AboutusView(View):
    template_name = 'aboutus.html'
    
    def get(self, request):
        current_user = request.user.id
        userdata = User_Profile.objects.filter(Users=current_user)
        purchasehis=Purchase_History.objects.filter(User=current_user)
        return render(request, self.template_name,{'userdata': userdata,'purchase_history':purchasehis})
class AdminBookingView(View):
    template_name = 'adminbook.html'
    def get(self, request):   
        if request.user.is_superuser: 
            
            
            contact_data = Contact.objects.all()
            search_query = request.GET.get('q')
            print(search_query)
            
            if search_query:
                contact_data = contact_data.filter(
                    Q(Name__icontains=search_query) 
                )  
            return render(request, self.template_name,{'data':contact_data})
        else:
            return redirect('onedaytwogether:index')
    def post(self, request):   
        if request.user.is_superuser:   
            current_user = request.user.id
            
            contact_data = Contact.objects.filter(User=current_user)
            
            return render(request, self.template_name,{'data':contact_data})
        else:
            return redirect('onedaytwogether:index')
        
        
class BookingView(View):
    template_name = 'booking.html'
    
    def get(self, request):
        current_user = request.user.id
        
        userdata = User_Profile.objects.filter(Users=current_user)
        contact_data = Contact.objects.filter(User=current_user)
        purchasehis=Purchase_History.objects.filter(User=current_user)
        return render(request, self.template_name,{'data':contact_data,'userdata': userdata,'purchase_history':purchasehis})
class LoginView(View):
    template_name = 'login.html'
    
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request, *args, **kwargs): 
        username = request.POST['email']
        password = request.POST['password']
        if '@' in username:
            mydata = User.objects.filter(email=username).first()
            user = authenticate(request, username=mydata.username, password=password)
        else:
            user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onedaytwogether:index')
        else:
            error_message = 'Wrong Username or Email or Password'
            messages.error(request, error_message)
            return redirect('onedaytwogether:Login')


class SignupView(View):
    template_name = 'signup.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request, **kwargs):
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            # Email already exists
            error_message = 'Email is already registered. Please use a different email.'
            messages.error(request, error_message)
            return redirect('onedaytwogether:Signup')  # Redirect to the signup page with an error message
        if User.objects.filter(username=username).exists():
            # Email already exists
            error_message = 'Username is already taken. Please use a different one.'
            messages.error(request, error_message)
            return redirect('onedaytwogether:Signup') 
        
        # Create user and save
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # Log in the user
        user = authenticate(request, username=username, password=password)
        login(request, user)
        
        return redirect('onedaytwogether:index')


from django.core.exceptions import ObjectDoesNotExist

class CompleteProfile(View):
    template_name = 'CompleteProfiles.html'
    
    def get(self, request):
        current_user = request.user.id
        try:
            userdata = User_Profile.objects.get(Users=current_user)
            return render(request, self.template_name, {'userdata': userdata})
        except User_Profile.DoesNotExist:
            return render(request, self.template_name)
    
    def post(self, request, **kwargs):
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        avatar = request.FILES.get('file')
        sex = request.POST.get('sex')
        dob = request.POST.get('birthdate')
        tel = request.POST.get('phone')
        detail = request.POST.get('detail')
        street = request.POST.get('street')
        city = request.POST.get('city')
        country = request.POST.get('country')
        
        user_profile, created = User_Profile.objects.get_or_create(Users=user)
        user_profile.first_name = first_name
        user_profile.last_name = last_name

        if avatar:
            user_profile.avatar = avatar  # Update avatar if a new file is provided

        user_profile.sex = sex
        user_profile.dob = dob
        user_profile.email = request.user.email
        user_profile.tel = tel
        user_profile.detail = detail
        user_profile.Address = f"Street: {street} City: {city} Country: {country}"
        user_profile.status = True  # Assuming status is a BooleanField
        user_profile.save()
        
        return redirect('onedaytwogether:index')
class LogoutView(View):
    def get(self, request): 
        logout(request)
        return redirect('onedaytwogether:Login')
