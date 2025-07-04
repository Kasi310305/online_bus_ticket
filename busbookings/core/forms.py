from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import UserProfile
from .models import City, Bus, Route, Seat ,Booking
from .models import Profile


class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets={
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'})
           
        }
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm,self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class':'form-control',})
        self.fields['password2'].widget.attrs.update({'class':'form-control',})


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['phone', 'profile_pic'] 

    

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['bus_name', 'bus_number', 'total_seats']


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['bus', 'from_city', 'to_city', 'date', 'time', 'price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ['route', 'seat_number', 'is_booked']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']
        widgets = {
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['route', 'seat']
        widgets = {
            'seat': forms.CheckboxSelectMultiple(),  # ✅ Multiple selection
        }


