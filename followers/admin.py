from django.contrib import admin
from .models import Follower
# Register your models here.
class FollowAdmin(admin.ModelAdmin):
    pass

admin.site.register(Follower, FollowAdmin)