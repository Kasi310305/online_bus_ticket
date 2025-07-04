from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Bus(models.Model):
    bus_name = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=20)
    total_seats = models.IntegerField()

    def __str__(self):
        return f"{self.bus_name} ({self.bus_number})"


class Route(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    from_city = models.ForeignKey(City, related_name='route_from', on_delete=models.CASCADE)
    to_city = models.ForeignKey(City, related_name='route_to', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bus} - {self.from_city} to {self.to_city} on {self.date}"


class Seat(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} on {self.route}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    # seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    seat = models.ManyToManyField(Seat)
    booked_on = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username} - Seat {self.seat.seat_number} on {self.route}"




def user_profile_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_profile_path, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
