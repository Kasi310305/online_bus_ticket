from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),

    # User Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Dashboard and Profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Bus Search and Booking
    path('search/', views.search_bus, name='search_bus'),
    path('book-seats/<int:route_id>/', views.book_seats, name='book_seat'),
    # path('payment/<int:booking_id>/', views.dummy_payment_multiple, name='dummy_payment_multiple'),
    path('payment/<int:booking_id>/', views.dummy_payment, name='payment'),
    path('payment-success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('download-ticket/<int:booking_id>/', views.download_ticket, name='download_ticket'),



    # Booking Management
    path('my-bookings/', views.booking_history, name='booking_history'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),



    # City
    path('cities/', views.city_list, name='city_list'),
    path('cities/add/', views.city_create, name='city_add'),
    path('cities/<int:id>/edit/', views.city_update, name='city_edit'),
    path('cities/<int:id>/delete/', views.city_delete, name='city_delete'),

    # Bus
    path('buses/', views.bus_list, name='bus_list'),
    path('buses/add/', views.bus_create, name='bus_add'),
    path('buses/<int:id>/edit/', views.bus_update, name='bus_edit'),
    path('buses/<int:id>/delete/', views.bus_delete, name='bus_delete'),

    # Route
    path('routes/', views.route_list, name='route_list'),
    path('routes/add/', views.route_create, name='route_add'),
    path('routes/<int:id>/edit/', views.route_update, name='route_edit'),
    path('routes/<int:id>/delete/', views.route_delete, name='route_delete'),

    # Seat
    path('seats/', views.seat_list, name='seat_list'),
    path('seats/add/', views.seat_create, name='seat_add'),
    path('seats/<int:id>/edit/', views.seat_update, name='seat_edit'),
    path('seats/<int:id>/delete/', views.seat_delete, name='seat_delete'),



]
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
