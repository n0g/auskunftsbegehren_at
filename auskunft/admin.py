from django.contrib import admin
from auskunft.models import Auftraggeber, Membership, Category

# Register your models here.
admin.site.register(Auftraggeber)
admin.site.register(Category)
admin.site.register(Membership)
