from django.shortcuts import render, redirect
from .models import ParkingLot, ParkingSpot, Vehicle, ParkingTicket, Payment
from django.utils import timezone
from django.db.models import Sum

# Create your views here.
def home(request):
    lots = ParkingLot.objects.all()
    return render(request, 'home.html', {'lots': lots})

def add_lot(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        total = request.POST.get('total_spots')
        price = request.POST.get('payment')
        
        lot = ParkingLot()
        lot.name = name
        lot.total_spots = total
        lot.payment = price
        lot.save()
        
        for i in range(1, int(total) + 1):
            spot = ParkingSpot()
            spot.parking_lot = lot
            spot.spot_no = i
            spot.save()
        return redirect('home')
    return render(request, 'add_lot.html')

def edit_lot(request, lot_id):
    lot = ParkingLot.objects.get(id=lot_id)
    if request.method == 'POST':
        lot.name = request.POST.get('name')
        lot.payment = request.POST.get('payment')
        lot.save()
        return redirect('home')
    return render(request, 'edit_lot.html', {'lot': lot})

def delete_lot(request, lot_id):
    lot = ParkingLot.objects.get(id=lot_id)
    lot.delete()
    return redirect('home')

def lot_detail(request, lot_id):
    lot = ParkingLot.objects.get(id=lot_id)
    spots = ParkingSpot.objects.filter(parking_lot=lot)

    if request.method == "POST":
        owner = request.POST.get('owner_name')
        plate = request.POST.get('plate_no')
        spot_id = request.POST.get('spot_id')

        if Vehicle.objects.filter(plate_no=plate).exists():
            vehicle = Vehicle.objects.get(plate_no=plate)
        else:
            vehicle = Vehicle()
            vehicle.owner_name = owner
            vehicle.plate_no = plate
            vehicle.save()

        spot = ParkingSpot.objects.get(id=spot_id)
        if spot.is_available:
            ticket_obj = ParkingTicket()
            ticket_obj.vehicle = vehicle
            ticket_obj.parking_spot = spot
            ticket_obj.save()

            spot.is_available = False
            spot.save()
            return redirect('lot_detail', lot_id=lot.id)
            
    return render(request, 'lots_detail.html', {'lot': lot, 'spots': spots})

def maintenance_toggle(request, spot_id):
    spot = ParkingSpot.objects.get(id=spot_id)
    spot.is_available = not spot.is_available
    spot.save()
    return redirect('lot_detail', lot_id=spot.parking_lot.id)

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicles.html', {'vehicles': vehicles})

def vehicle_edit(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    if request.method == 'POST':
        vehicle.owner_name = request.POST.get('owner_name')
        vehicle.plate_no = request.POST.get('plate_no')
        vehicle.save()
        return redirect('vehicle_list')
    return render(request, 'edit_vehicle.html', {'vehicle': vehicle})

def vehicle_search(request):
    query = request.GET.get('q')
    results = Vehicle.objects.filter(plate_no__icontains=query)
    return render(request, 'search.html', {'results': results})

def active_tickets(request):
    tickets = ParkingTicket.objects.filter(exit_time=None)
    return render(request, 'active_tickets.html', {'tickets': tickets})

def vehicle_exit(request, ticket_id):
    ticket = ParkingTicket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.exit_time = timezone.now()
        ticket.save()

        duration = ticket.exit_time - ticket.entry_time
        duration_in_hours = duration.total_seconds() / 3600
        
        if ticket.parking_spot:
            rate = ticket.parking_spot.parking_lot.payment
            total_amount = float(rate) * max(1, duration_in_hours)

            pay_obj = Payment()
            pay_obj.ticket = ticket
            pay_obj.amount = total_amount
            pay_obj.save()
            
            spot = ticket.parking_spot
            spot.is_available = True
            spot.save()
        return redirect('active_tickets')
    return render(request, 'confirm.html', {'ticket': ticket})

def ticket_delete(request, ticket_id):
    ticket = ParkingTicket.objects.get(id=ticket_id)
    if ticket.parking_spot:
        ticket.parking_spot.is_available = True
        ticket.parking_spot.save()
    ticket.delete()
    return redirect('active_tickets')

def payment_history(request):
    payments = Payment.objects.all().order_by('-payment_time')
    return render(request, 'payments.html', {'payments': payments})

def delete_payment_record(request, pay_id):
    pay = Payment.objects.get(id=pay_id)
    pay.delete()
    return redirect('payment_history')

def revenue_stats(request):
    total = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    count = Payment.objects.count()
    avg_transaction = total / count if count and count > 0 else 0
    return render(request, 'revenue.html', {'avg_transaction':avg_transaction,'total': total, 'count': count})

def clear_all_history(request):
    Payment.objects.all().delete()
    ParkingTicket.objects.all().delete()
    return redirect('home')

def spot_list_all(request):
    all_spots = ParkingSpot.objects.all().order_by('parking_lot')
    return render(request, 'all_spots.html', {'spots': all_spots})

def lot_capacity_check(request, lot_id):
    lot = ParkingLot.objects.get(id=lot_id)
    occupied = ParkingSpot.objects.filter(parking_lot=lot, is_available=False).count()
    is_full = occupied >= lot.total_spots
    return render(request, 'status.html', {'lot': lot, 'is_full': is_full})