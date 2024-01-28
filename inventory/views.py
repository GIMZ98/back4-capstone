from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Create your views here.
def index(request):
    return render(request, "inventory/index.html", {
        "profit": Vehicle.get_profit(),
        "revenues": Vehicle.get_sum_selling_prices(),
        "inventory": Vehicle.get_sum_inventory_value(),
    })

@csrf_protect
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "inventory/login.html", {
                "message": "Invalid username and/or password. Try Again!"
            })
    else:
        return render(request, "inventory/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def revenues(request):
    return render(request, "inventory/revenues.html", {
        "sales": Sale.objects.all(),
       
    })

def vehicles(request):
    return render(request, "inventory/vehicles.html", {
        "vehicles": Vehicle.objects.filter(sold=False)
       
    })



@csrf_exempt
@require_http_methods(["GET"])
def data_charts(request, chart):
    
    if chart == 'revenues':
        car = Car.get_sum_selling_prices()
        ev = ElectricVehicle.get_sum_selling_prices()
        van = Van.get_sum_selling_prices()

        data = [car, ev, van]

    elif chart == 'profits':
        car = Car.get_profit()
        ev = ElectricVehicle.get_profit()
        van = Van.get_profit()

        data = [car, ev, van]

    elif chart == 'unsold':
        car = Car.get_sum_inventory_value()
        ev = ElectricVehicle.get_sum_inventory_value()
        van = Van.get_sum_inventory_value()

        data = [car, ev, van]

    else:
        data = []

    # Create a dictionary to be converted to JSON
    response_data = {
        'chart': chart,
        'data': data,
    }
    print(response_data)
    # Return the data as JSON response
    return JsonResponse(response_data)

@csrf_exempt
@require_http_methods(["POST"])
def sell(request):

    buyerName = request.POST["buyerName"]
    vehicleId = request.POST["vehicleId"]
    
    vehicle = Vehicle.objects.filter(id=vehicleId)[0]
    sale=Sale.objects.create(vehicle=vehicle, buyer_name=buyerName)
    sale.save()
    vehicle.sold = True
    vehicle.save()
    #return JsonResponse({"sold": "yes"})
    return HttpResponseRedirect(reverse("revenues"))


@csrf_exempt
@require_http_methods(["POST"])
def add(request):

    brand = request.POST["brand"]
    model = request.POST["model"]
    year = request.POST["year"]
    color = request.POST["color"]
    mileage = request.POST["mileage"]
    vin = request.POST["vin"]
    costPrice = request.POST["costPrice"]
    sellingPrice = request.POST["sellingPrice"]
    type = request.POST["type"]


    if 'image' in request.POST:
        image = request.FILES.get('image')
    else:
        image = None

    if type == 'car':
        fuelType = request.POST["fuelType"]
        fuelCapacityLiters = request.POST["fuelCapacityLiters"]
        car = Car.objects.create(brand=brand, model=model, year=year, color=color, mileage=mileage, vin=vin, image=image, cost_price=costPrice, selling_price=sellingPrice, type=type, fuel_type=fuelType, fuel_capacity_liters=fuelCapacityLiters)
        car.save()

    elif type == 'ev':
        batteryCapacity = request.POST["batteryCapacity"]
        ev = ElectricVehicle.objects.create(brand=brand, model=model, year=year, color=color, mileage=mileage, vin=vin, image=image, cost_price=costPrice, selling_price=sellingPrice, type=type, battery_capacity_kwh=batteryCapacity)
        ev.save()

    elif type == 'van':
        fuelType = request.POST["fuelType"]
        fuelCapacityLiters = request.POST["fuelCapacityLiters"]
        van = Van.objects.create(brand=brand, model=model, year=year, color=color, mileage=mileage, vin=vin, image=image, cost_price=costPrice, selling_price=sellingPrice, type=type, fuel_type=fuelType, fuel_capacity_liters=fuelCapacityLiters)
        van.save()
         
    #return JsonResponse({"sold": "yes"})
    return HttpResponseRedirect(reverse("vehicles"))


def sell_view(request, vtype):

    if vtype == 'car':
        vehicles = Car.objects.filter(sold=False)
        text = 'Car'

    elif vtype == 'ev':
        vehicles = ElectricVehicle.objects.filter(sold=False)
        text = 'Electric Vehicle'

    elif vtype == 'van':
        vehicles = Van.objects.filter(sold=False)
        text = 'Van'

    else:
        vehicles = []
    
    #return JsonResponse({"sold": "yes"})
    return render(request, "inventory/sell_page.html", {
        "vehicles": vehicles,
        "type": text,
    })


def add_view(request, vtype):

    if vtype == 'car':
        text = 'Car'

    elif vtype == 'ev':
        text = 'Electric Vehicle'

    elif vtype == 'van':
        text = 'Van'

    else:
        vehicles = []
    
    #return JsonResponse({"sold": "yes"})
    return render(request, "inventory/add_page.html", {
        "type": text,
        "stype": vtype,
    })
