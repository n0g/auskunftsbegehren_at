from django.contrib import admin
from auskunft.models import Auftraggeber, Application, Membership, Category

# Register your models here.
admin.site.register(Auftraggeber)
admin.site.register(Application)
admin.site.register(Category)
admin.site.register(Membership)
