from django.contrib import admin
from .models import User, Category, Listing, Comment, Bid

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "date_joined")
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_type")
    
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "start_bid", "seller", "category", "created_on", "status",)
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("writer", "listing", "comment_msg")
    
    
class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "bid_amount")
    
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
