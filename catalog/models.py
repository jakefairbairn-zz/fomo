from django.db import models
from polymorphic.models import PolymorphicModel
from django.conf import settings

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
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    def image_url(self):
        '''Always returns an image'''
        if not self.images.all():
            url = settings.STATIC_URL + 'catalog/media/products/image_unavailable.gif'
        else:
            url = settings.STATIC_URL + 'catalog/media/products/' + self.images.all()[0].filename
        return url

    def image_urls(self):
        if not self.images.all():
            return ['image_unavailable.gif']
        else:
            return self.images.all()

class BulkProduct(Product):
    '''A bulk product'''
    TITLE = 'Bulk'
    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()

class IndividualProduct(Product):
    '''A product tracked individually'''
    TITLE = 'Individual'
    pid = models.TextField()

class RentalProduct(Product):
    '''Rental product (tracked individually)'''
    TITLE = 'Rental'
    pid = models.TextField()
    max_rental_days = models.IntegerField(default=0)
    retire_date = models.DateField(null=True, blank=True)

class ProductImage(models.Model):
    '''Images for a product'''
    filename = models.TextField()
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
