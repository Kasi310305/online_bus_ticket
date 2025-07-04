from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Route, Booking, Seat, City ,Bus
from .forms import UserRegisterForm
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CityForm, BusForm, RouteForm, SeatForm
from .forms import EditUserForm, EditProfileForm
from django.core.paginator import Paginator
from django.db.models.functions import TruncMonth
from django.db.models import Count
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import datetime,date

# ----------- City Views -----------

@staff_member_required
def city_list(request):
    cities = City.objects.all()
    return render(request, 'city_list.html', {'cities': cities})

@staff_member_required
def city_create(request):
    form = CityForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('city_list')
    return render(request, 'form_template.html', {'form': form, 'title': 'Add City'})

@staff_member_required
def city_update(request, id):
    city = get_object_or_404(City, id=id)
    form = CityForm(request.POST or None, instance=city)
    if form.is_valid():
        form.save()
        return redirect('city_list')
    return render(request, 'form_template.html', {'form': form, 'title': 'Edit City'})

@staff_member_required
def city_delete(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    return redirect('city_list')


# ----------- Bus Views -----------

@staff_member_required
def bus_list(request):
    buses = Bus.objects.all()
    return render(request, 'bus_list.html', {'buses': buses})

@staff_member_required
def bus_create(request):
    form = BusForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('bus_list')
    return render(request, 'form_template.html', {'form': form, 'title': 'Add Bus'})

@staff_member_required
def bus_update(request, id):
    bus = get_object_or_404(Bus, id=id)
    form = BusForm(request.POST or None, instance=bus)
    if form.is_valid():
        form.save()
        return redirect('bus_list')
    return render(request, 'form_template.html', {'form': form, 'title': 'Edit Bus'})

@staff_member_required
def bus_delete(request, id):
    bus = get_object_or_404(Bus, id=id)
    bus.delete()
    return redirect('bus_list')


# ----------- Route Views -----------

@staff_member_required
def route_list(request):
    routes = Route.objects.all()
    return render(request, 'route_list.html', {'routes': routes})

@staff_member_required
def route_create(request):
    form = RouteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('route_list')
    return render(request, 'form_template.html', {'form': form, 'title': 'Add Route'})

@staff_member_required
def route_update(request, id):
    route = get_object_or_404(Route, id=id)
    form = RouteForm(request.POST or None, instance=route)
    if form.is_valid():
        form.save()
        return redirect('route_list')
    return render(request, 'form_template.html', {'form': form, 'title': 'Edit Route'})

@staff_member_required
def route_delete(request, id):
    route = get_object_or_404(Route, id=id)
    route.delete()
    return redirect('route_list')


# ----------- Seat Views -----------

@staff_member_required
def seat_list(request):
    seats = Seat.objects.all()
    return render(request, 'seat_list.html', {'seats': seats})

@staff_member_required
def seat_create(request):
    form = SeatForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('seat_list')
    return render(request, 'form_template.html', {'form': form, 'title': 'Add Seat'})

@staff_member_required
def seat_update(request, id):
    seat = get_object_or_404(Seat, id=id)
    form = SeatForm(request.POST or None, instance=seat)
    if form.is_valid():
        form.save()
        return redirect('seat_list')
    return render(request, 'form_template.html', {'form': form, 'title': 'Edit Seat'})

@staff_member_required
def seat_delete(request, id):
    seat = get_object_or_404(Seat, id=id)
    seat.delete()
    return redirect('seat_list')




def home(request):
    cities = City.objects.all()
    return render(request, 'index.html', {'cities': cities})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('home')
#         messages.error(request, 'Invalid username or password.')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form,'user':user})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url or 'home')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()       
    if 'next' in request.GET:
        messages.info(request, "Please enter your login credentials and proceed.")

    return render(request, 'login.html',{'form': form})



@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_on')
    paginator = Paginator(bookings, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Total fare calculation
    booking_total_fares = {
        booking.id: booking.seat.count() * booking.route.price
        for booking in page_obj
    }

    # Booking chart data
    monthly_data = Booking.objects.filter(user=request.user).annotate(
        month=TruncMonth('booked_on')
    ).values('month').annotate(count=Count('id')).order_by('month')

    chart_labels = [entry['month'].strftime('%b %Y') for entry in monthly_data]
    chart_counts = [entry['count'] for entry in monthly_data]

    return render(request, 'dashboard.html', {
        'recent_bookings': page_obj,
        'booking_total_fares': booking_total_fares,
        'chart_labels': json.dumps(chart_labels),
        'chart_counts': json.dumps(chart_counts),

    })


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# @login_required
# def search_bus(request):
#     routes = []
#     if request.method == 'GET':
        # from_city = request.GET.get('from_city')
        # to_city = request.GET.get('to_city')
        # date = request.GET.get('date')
        # if from_city and to_city and date:
        #     routes = Route.objects.filter(from_city__id=from_city, to_city__id=to_city, date=date)
#     cities = City.objects.all()
#     return render(request, 'search.html', {'routes': routes, 'cities': cities})

def search_bus(request):
    routes = Route.objects.none()
    today = date.today()
    cities = City.objects.all()
    source = request.GET.get('from_city')
    destination = request.GET.get('to_city')
    travel_date_str = request.GET.get('date')

    # ✅ Safe date fallback
    try:
        travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d").date() if travel_date_str else today
    except (ValueError, TypeError):
        travel_date = today

    # Filter by today's or selected date
    routes = Route.objects.filter(date=travel_date)

    if source and "select" not in source.lower():
        routes = routes.filter(from_city__id=source.strip())

    if destination and "select" not in destination.lower():
        routes = routes.filter(to_city__id=destination.strip())


    return render(request, 'search.html', {
        'routes': routes,
        'default_date': today,
        'cities':cities
    })

# @login_required
# def book_seat(request, route_id):
#     route = get_object_or_404(Route, id=route_id)
#     available_seats = Seat.objects.filter(route=route, is_booked=False)

#     if request.method == 'POST':
#         selected_seats = request.POST.getlist('seats')  # list of seat numbers
#         booking_ids = []

#         for seat_num in selected_seats:
#             seat = Seat.objects.get(route=route, seat_number=seat_num, is_booked=False)
#             seat.is_booked = True
#             seat.save()

#             booking = Booking.objects.create(
#                 user=request.user,
#                 route=route,
#                 seat=seat
#             )
#             booking_ids.append(str(booking.id))  # convert to string for URL

#         # redirect to dynamic payment URL: /payment/12-13-14/
#         ids_str = "-".join(booking_ids)
#         return redirect('dummy_payment_multiple', ids=ids_str)

#     return render(request, 'book_seat.html', {
#         'route': route,
#         'available_seats': available_seats
#     })



@login_required
def book_seats(request, route_id):
    route = get_object_or_404(Route, id=route_id)

    # Get all booked seats for this route
    booked_seats = Seat.objects.filter(booking__route=route, booking__is_cancelled=False).distinct()

    # Get available seats for this bus
    available_seats = Seat.objects.filter(route=route).exclude(id__in=booked_seats)

    if request.method == 'POST':
        selected_seats_ids = request.POST.getlist('seats')  # seats is name of checkbox
        if not selected_seats_ids:
            return render(request, 'book_seat.html', {
                'route': route,
                'available_seats': available_seats,
                'error': "Please select at least one seat.",
            })

        # Validate selected seats are still available
        selected_seats = Seat.objects.filter(id__in=selected_seats_ids).exclude(id__in=booked_seats)
        if len(selected_seats) != len(selected_seats_ids):
            return render(request, 'book_seat.html', {
                'route': route,
                'available_seats': available_seats,
                'error': "Some selected seats are no longer available.",
            })

        # Save booking
        booking = Booking.objects.create(user=request.user, route=route)
        booking.seat.set(selected_seats)
        return redirect('payment', booking_id=booking.id)

    return render(request, 'book_seat.html', {
        'route': route,
        'available_seats': available_seats
    })








# @login_required
# def dummy_payment(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id, user=request.user)
#     if request.method == 'POST':
#         messages.success(request, "Payment successful! Booking confirmed.")
#         return redirect('booking_history')
#     return render(request, 'payment.html', {'booking': booking})



@csrf_exempt
def dummy_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    total_fare = booking.seat.count() * booking.route.price

    if request.method == "POST":
        booking.is_paid = True
        booking.save()
        return redirect('payment_success', booking_id=booking.id)


    return render(request, 'payment.html', {
        'booking': booking,
        'total_fare': total_fare,
    })


def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'payment_success.html', {'booking': booking})



def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    html = render_to_string('ticket.html', {'booking': booking})
    return HttpResponse(html)


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_on')
    return render(request, 'booking_history.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.is_cancelled = True
    booking.seat.is_booked = False
    
    booking.save()
    messages.warning(request, "Booking cancelled.")
    return redirect('booking_history')


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.delete()
        return redirect('dashboard')  # or 'booking_history' if you have that

    return redirect('dashboard')  # fallback for GET


