from django.contrib import admin
from .models import Vehicle, Car, ElectricVehicle, Van, Sale

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Car)
admin.site.register(ElectricVehicle)
admin.site.register(Van)
admin.site.register(Sale)