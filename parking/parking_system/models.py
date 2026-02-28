from django.db import models

# Create your models here.
class ParkingLot(models.Model):
    name = models.CharField(max_length=50)
    total_spots = models.PositiveIntegerField()
    payment = models.DecimalField(max_digits=6,decimal_places=2)
    def __str__(self):
        return self.name
    
class ParkingSpot(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, )
    spot_no = models.IntegerField()
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.parking_lot.name} - {self.spot_no}"

class Vehicle(models.Model):
    owner_name = models.CharField(max_length=20)
    plate_no = models.CharField(max_length=8,unique=True)
    def __str__(self):
        return self.plate_no

class ParkingTicket(models.Model):
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(ParkingSpot,on_delete=models.SET_NULL, null=True)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null= True,blank=True)
    def __str__(self):
        return f"Ticket {self.id} - {self.vehicle.plate_no}"

class Payment(models.Model):
    ticket = models.ForeignKey(ParkingTicket,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_time = models.DateTimeField(auto_now_add=True)
