from django import forms
from .models import User,Hobby
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
class newform(forms.ModelForm):
 

    class Meta:
        model = User
        fields = ['name', 'age','gender', 'email', 'country','choices', 'image']
        labels = {'choices': 'Hobbies'}
        widgets = {
            'gender': forms.Select,
            'choices': forms.CheckboxSelectMultiple,
            'country': CountrySelectWidget(),
        }
        
    def __init__(self, *args, **kwargs):
        super(newform, self).__init__(*args, **kwargs)
        country_choices = list(self.fields['country'].choices)
        self.fields['country'].choices = [('', 'Select country')] + country_choices
        india_choice = next((choice for choice in country_choices if choice[1] == 'India'), None)
        if india_choice:
            country_choices.remove(india_choice)
            country_choices.insert(0, india_choice)
        self.fields['country'].choices = [('', 'Select country')] + country_choices
        