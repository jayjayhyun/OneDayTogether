from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from onedaytwogether import views as onedaytwogether_view
from onedaytwogether.views import *

app_name = 'onedaytwogether'

urlpatterns = [
    re_path('^index/$', onedaytwogether_view.HomeView.as_view(), name='index'),
    re_path('^Destination/$', onedaytwogether_view.DestinationView.as_view(), name='Destination'),
    re_path('^Shop/$', onedaytwogether_view.ShopView.as_view(), name='shop'),
    re_path('^Shop/(?P<category>[a-zA-Z0-9_]+)$', ShopCategoryView.as_view(), name='shopcategory'),
    re_path('^ShopDetail/(?P<id>[a-zA-Z0-9_]+)$', onedaytwogether_view.ShopDetailView.as_view(), name='detail'),
    re_path('^Contact/$', onedaytwogether_view.ContactView.as_view(), name='contact'),
    re_path('^Cart/$', onedaytwogether_view.CartView.as_view(), name='cart'),
    re_path('^Cart/Purchase/$', onedaytwogether_view.PurchaseView.as_view(), name='purchase'),
    re_path('^Cart/Delete/(?P<id>[a-zA-Z0-9_]+)$', onedaytwogether_view.CartDeleteView.as_view(), name='cartdelete'),
    re_path('^Aboutus/$', onedaytwogether_view.AboutusView.as_view(), name='Aboutus'),
    re_path('^Login/$', onedaytwogether_view.LoginView.as_view(), name='Login'),
    re_path('^Signup/$', onedaytwogether_view.SignupView.as_view(), name='Signup'),
    re_path('^Logout/$', onedaytwogether_view.LogoutView.as_view(), name='Logout'),
    re_path('^CompleteProfile/$', onedaytwogether_view.CompleteProfile.as_view(), name='CompleteProfile'),
    re_path('^Onedaytowgther/Admin/Booking/$', onedaytwogether_view.AdminBookingView.as_view(), name='AdminBooking'),
    re_path('^Onedaytowgther/Admin/Booking/Approve/(?P<id>[a-zA-Z0-9_]+)$', onedaytwogether_view.AdminBookingApproveView.as_view(), name='AdminBooking'),
    re_path('^Onedaytowgther/Admin/Booking/Decline/(?P<id>[a-zA-Z0-9_]+)$', onedaytwogether_view.AdminBookingDeclineView.as_view(), name='AdminBooking'),
    re_path('^Booking/$', onedaytwogether_view.BookingView.as_view(), name='Booking'),
    re_path('^Booking/Delete/(?P<id>[a-zA-Z0-9_]+)$', onedaytwogether_view.BookingDeleteView.as_view(), name='Bookingdelete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)