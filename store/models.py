from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
catagories_choices = (
    ('green','GREEN'),
    ('blue', 'BLUE'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('black','BLACK'),
)

unit_choices =(
    ('KG', 'KG'),
    ('ltr', 'liter'),
    ('unit', 'unit')
)

class Store(models.Model):
    catagories = models.CharField(max_length=6, choices=catagories_choices, default='green')
    item_name = models.CharField(max_length = 50, primary_key=True)
    def __str__(self):
        return self.item_name

class AddStore(models.Model):
    item = models.OneToOneField(Store, on_delete=models.CASCADE, primary_key=True)
    quantityNo = models.FloatField(validators=[MinValueValidator(0.0)]) 
    quantityUnit = models.CharField(max_length=6, choices=unit_choices, default='green')
    costPrice = models.FloatField(validators=[MinValueValidator(0.0)])
    sellingPrice = models.FloatField(validators=[MinValueValidator(0.0)])
    def __str__(self):
        return str(self.item)

class Sale(models.Model):
    item = models.ForeignKey(AddStore, on_delete=models.SET_NULL, null=True)
    soldquantity = models.FloatField(validators=[MinValueValidator(0.0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        q =  AddStore.objects.get(item=self.item)  
        if( q.quantityNo-self.soldquantity>=0 ):
            q.quantityNo = q.quantityNo-self.soldquantity 
            q = q.save()
            super(Sale, self).save(*args, **kwargs)
        else:
            pass
    def __str__(self): 
        return str(self.item)
    
