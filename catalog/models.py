from django.db import models
from polymorphic.models import PolymorphicModel

class Category(models.Model):
        '''Category for products'''
        create_date = models.DateTimeField(auto_now_add=True)
        last_modified = models.DateTimeField(auto_now=True)
        name = models.TextField()
        description = models.TextField()

        def __str__(self):
            return self.name

#pip3 install django-polymorphic
class Product(PolymorphicModel):
    '''A bulk, individual, or rental product'''
    TYPE_CHOICES = (
        ( 'BulkProduct', 'Bulk Product' ),
        ( 'IndividualProduct', 'Individual Product' ),
        ( 'RentalProduct', 'Rental Product' )
    )
    STATUS_CHOICES = (
        ( 'A', 'Active' ),
        ( 'I', 'Inactive' )
    )
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=STATUS_CHOICES, default='A')
    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)

class BulkProduct(Product):
    '''A bulk product'''
    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()

class IndividualProduct(Product):
    TITLE = 'Individual'
    '''A product tracked individually'''
    pid = models.TextField()

class RentalProduct(Product):
    '''Rental product (tracked individually)'''
    pid = models.TextField()
    max_rental_days = models.IntegerField(default=0)
    retire_date = models.DateField(null=True, blank=True)
