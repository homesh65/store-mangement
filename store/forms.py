from django import forms
from .models import Store, AddStore, Sale

class StoreForm(forms.ModelForm):  
    class Meta: 
        model = Store 
        fields = "__all__"

class AddStoreForm(forms.ModelForm):  
    class Meta: 
        model = AddStore 
        fields = "__all__"

class SaleFrom(forms.ModelForm):  
    class Meta: 
        model = Sale 
        fields = "__all__"
