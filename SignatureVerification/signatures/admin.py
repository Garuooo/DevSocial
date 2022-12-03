from django.contrib import admin

from .models import Signature,Tag,Note,Verify
# Register your models here.
admin.site.register(Signature)
admin.site.register(Tag)
admin.site.register(Note)
admin.site.register(Verify)
