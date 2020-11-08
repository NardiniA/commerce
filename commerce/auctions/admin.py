from django.contrib import admin

from .models import User, Category, Auction, Bid, Comment, WatchList

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)