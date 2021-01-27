from django.contrib import admin
from asft_core.models import Profile, Message
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)