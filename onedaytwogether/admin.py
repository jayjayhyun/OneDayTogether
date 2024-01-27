from django.contrib import admin
from . models import *
from django.utils.html import format_html

class UserAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="../../../onedaytwogether/media/{}" width="50px" />'.format(obj.avatar))
    list_display = ['id','Users', 'first_name', 'last_name', 'image_tag', 'dob']
    list_display_links = ['id', 'first_name', 'last_name']
    list_per_page = 5
    search_fields = ['id', 'first_name', 'last_name']
    autocomplete_fields = ['Users']
admin.site.register(User_Profile, UserAdmin)

class Tour_TeamAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="../../../onedaytwogether/media/{}" width="50px" />'.format(obj.Image))
    list_display = ['id','Team_name', 'image_tag', 'tel', 'detail']
    list_display_links = ['id', 'Team_name']
    list_per_page = 5
    search_fields = ['id', 'Team_name']
admin.site.register(Tour_Team, Tour_TeamAdmin)

class DestinationAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="../../../onedaytwogether/media/{}" width="50px" />'.format(obj.Image))
    list_display = ['id','destination','image_tag']
    list_display_links = ['id', 'destination']
    list_per_page = 5
    search_fields = ['id', 'destination']
admin.site.register(Destination, DestinationAdmin)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id','Destination','Schedule']
    list_display_links = ['id', 'Destination']
    list_per_page = 5
    search_fields = ['id', 'Destination', 'Schedule']
admin.site.register(Schedule, ScheduleAdmin)

class TourAdmin(admin.ModelAdmin):
    list_display = ['id','User_Profile_ID', 'Tour_Team_ID', 'Destination_ID', 'Schedule_ID']
    list_display_links = ['id', 'User_Profile_ID', 'Tour_Team_ID']
    list_per_page = 5
    search_fields = ['id', 'User_Profile_ID', 'Tour_Team_ID', 'Destination_ID']
#    autocomplete_fields = ['User_Profile_ID, Tour_Team_ID', 'Destination_ID', 'Schedule_ID']
admin.site.register(Tour, TourAdmin)
class ShopAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="../../../onedaytwogether/media/{}" width="50px" />'.format(obj.Image))
    list_display = ['id', 'image_tag', 'Product_name', 'Quantity', 'Original_Price', 'New_Price', 'Product_Type']
    list_display_links = ['id', 'image_tag', 'Product_name']
    list_per_page = 5
    search_fields = ['id', 'Product_name']
admin.site.register(Shop, ShopAdmin)
class Purchase_HistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'User', 'Product_name', 'Amount', 'Cost', 'Date']
    list_display_links = ['id', 'User', 'Product_name']
    list_per_page = 5
    search_fields = ['id', 'User', 'Product_name']
admin.site.register(Purchase_History, Purchase_HistoryAdmin)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Email', 'Destination', 'Schedule','Details']
    list_display_links = ['id', 'Name', 'Email']
    list_per_page = 5
    search_fields = ['id', 'Name', 'Destination', 'Schedule']
admin.site.register(Contact, ContactAdmin)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'Username', 'Product_name', 'Price', 'Quantity']
    list_display_links = ['id', 'Username', 'Product_name']
    list_per_page = 5
    search_fields = ['id', 'Username', 'Product_name']
admin.site.register(Cart, CartAdmin)