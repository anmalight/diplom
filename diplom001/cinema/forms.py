from django import forms
from django.core.exceptions import ValidationError

from cinema.models import MovieSession, Ticket, Movie, CinemaHall


class AddHallForm(forms.ModelForm):
    class Meta:
        model = CinemaHall
        fields = '__all__'


class AddMovieForm(forms.ModelForm):

    # def clean(self):
    #     super(AddMovieForm, self).clean()
    #     error_message = ''
    #     field = ''
    #     # reusable check
    #     if self.cleaned_data['reusable'] == 0:
    #         error_message = 'reusable should not be zero'
    #         field = 'reusable'
    #         self.add_error(field, error_message)
    #         raise ValidationError(error_message)

        # return self.cleaned_data
    class Meta:
        model = Movie
        fields = ['name', 'info', 'poster', 'display_date_start', 'display_date_end']
        widgets = {
            'display_date_start': forms.DateInput(format='%d/%m/%Y', attrs={
                'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            'display_date_end': forms.DateInput(format='%d/%m/%Y', attrs={
                'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'})
        }


class AddMovieSessionForm(forms.ModelForm):
    class Meta:
        model = MovieSession
        fields = ['film', 'hall', 'time_from', 'time_to', 'price', 'available_seats']
        widgets = {
            'time_from': forms.widgets.DateTimeInput(format="%d/%m/%Y %H:%M:%S",
                                                     attrs={'placeholder': "MM/DD/YYYY HH:MM:SS",
                                                            'type': 'datetime'
                                                            }),
            'time_to': forms.widgets.DateTimeInput(format="%d/%m/%Y %H:%M:%S",
                                                   attrs={'placeholder': "MM/DD/YYYY HH:MM:SS",
                                                          'type': 'datetime'
                                                          }),
        }


class AmountForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['amount', ]
