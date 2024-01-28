from django.db import models
import os
from django.contrib.auth.models import AbstractUser

def get_image_upload_path(instance, filename):
    return os.path.join('vehicle_images', str(instance.vin), filename)

class User(AbstractUser):
    pass

class Vehicle(models.Model):
    # General information about all vehicles
    brand = models.CharField(max_length=16)
    model = models.CharField(max_length=32)
    year = models.IntegerField()
    color = models.CharField(max_length=16)
    mileage = models.DecimalField(max_digits=10, decimal_places=2)
    vin = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to=get_image_upload_path, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    sold = models.BooleanField(default=False)
    type = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return f'ID:{self.id}, VIN:{self.vin}, BRAND:{self.brand}, model:{self.model}, YEAR:({self.year})' 

    @classmethod
    def get_sum_inventory_value(cls):
        # Returns sum of selling prices of non sold vehicles
        return cls.objects.filter(sold=False).aggregate(selling_prices=models.Sum('selling_price'))['selling_prices']

    @classmethod
    def get_sum_cost_prices(cls):
        # Returns sum of cost prices of sold vehicles
        sum_cost_prices = cls.objects.filter(sold=True).aggregate(sum_cost_prices=models.Sum('cost_price'))['sum_cost_prices']
        return sum_cost_prices if sum_cost_prices is not None else 0

    @classmethod
    def get_sum_selling_prices(cls):
        # Returns sum of selling prices of sold vehicles
        sum_selling_prices = cls.objects.filter(sold=True).aggregate(selling_prices=models.Sum('selling_price'))['selling_prices']
        return sum_selling_prices if sum_selling_prices is not None else 0

    @classmethod
    def get_profit(cls):
        # Returns the difference value between summations of selling prices and cost prices of sold vehicles
        return cls.get_sum_selling_prices() - cls.get_sum_cost_prices()

class Car(Vehicle):
    # Additional information about cars
    fuel_type = models.CharField(max_length=16)
    fuel_capacity_liters = models.DecimalField(max_digits=6, decimal_places=2)

class ElectricVehicle(Vehicle):
    # Additional information about electric vehicles
    battery_capacity_kwh = models.DecimalField(max_digits=8, decimal_places=2)

class Van(Vehicle):
    # Additional information about vans
    fuel_type = models.CharField(max_length=16)
    fuel_capacity_liters = models.DecimalField(max_digits=6, decimal_places=2)

class Sale(models.Model):
    # Additional information about vehicle sales
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=32)
    sale_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.vehicle.brand} {self.vehicle.model} - Sold to {self.buyer_name} on {self.sale_date}'
