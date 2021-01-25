from django.contrib import admin
from .models import Store,AddStore,Sale

# Register your models here.
admin.site.register(Store)
admin.site.register(AddStore)
admin.site.register(Sale)