from django.conf import settings
from django.db import models, transaction
from polymorphic.models import PolymorphicModel
from django.forms.models import model_to_dict
from decimal import Decimal
from datetime import datetime
import stripe
from localflavor.us.us_states import STATE_CHOICES

#######################################################################
# Category

class Category(models.Model):
    '''Category for products'''
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


#######################################################################
# Products

class Product(PolymorphicModel):
    '''A bulk, individual, or rental product'''
    TYPE_CHOICES = (
        ('BulkProduct', 'Bulk Product'),
        ('IndividualProduct', 'Individual Product'),
        ('RentalProduct', 'Rental Product')
    )
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive')
    )
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=STATUS_CHOICES, default='A')
    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    def image_url(self):
        '''Always returns an image'''
        if not self.images.all():
            url = settings.STATIC_URL + 'catalog/media/products/image_unavailable.gif'
        else:
            url = settings.STATIC_URL + 'catalog/media/products/' + \
                self.images.all()[0].filename
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
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE)


from django.db import models, transaction
from django.conf import settings
from django.forms.models import model_to_dict
from polymorphic.models import PolymorphicModel
from decimal import Decimal
from datetime import datetime
import stripe

#######################################################################
# Orders

class Order(models.Model):
    '''An order in the system'''
    STATUS_CHOICES = (
        ('cart', 'Shopping Cart'),
        ('payment', 'Payment Processing'),
        ('sold', 'Finalized Sale'),
    )
    order_date = models.DateTimeField(null=True, blank=True)
    name = models.TextField(blank=True, default="Shopping Cart")
    status = models.TextField(choices=STATUS_CHOICES,
                              default='cart', db_index=True)
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0)  # max number is 999,999.99
    user = models.ForeignKey(
        'account.User', related_name='orders',  on_delete=models.CASCADE)
    # shipping information
    ship_date = models.DateTimeField(null=True, blank=True)
    ship_tracking = models.TextField(null=True, blank=True)
    ship_name = models.TextField(null=True, blank=True)
    ship_address = models.TextField(null=True, blank=True)
    ship_city = models.TextField(null=True, blank=True)
    ship_state = models.CharField(
        max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    ship_zip_code = models.TextField(null=True, blank=True)

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'Order {}: {}: {}'.format(self.id, self.user.get_full_name(), self.total_price)

    def active_items(self, include_tax_item=True):
        '''Returns the active items on this order'''
        # create a query object (filter to status='active')

        # if we aren't including the tax item, alter the
        # query to exclude that OrderItem
        # I simply used the product name (not a great choice,
        # but it is acceptable for credit)

        # MY CODE
        if include_tax_item:
            active_items = OrderItem.objects.filter(status='active')
        else:
            active_items = OrderItem.objects.filter(status='active').exclude(product__name='tax_item')
        
        return active_items
        # END

    def get_item(self, product, create=False):
        '''Returns the OrderItem object for the given product'''
        item = OrderItem.objects.filter(order=self, product=product).first()
        if item is None and create:
            item = OrderItem.objects.create(
                order=self, product=product, price=product.price, quantity=0)
        elif create and item.status != 'active':
            item.status = 'active'
            item.quantity = 0
        item.recalculate()
        item.save()
        return item

    def num_items(self):
        '''Returns the number of items in the cart'''
        return sum(self.active_items(include_tax_item=False).values_list('quantity', flat=True))

    def recalculate(self):
        '''
        Recalculates the total price of the order,
        including recalculating the taxable amount.

        Saves this Order and all child OrderLine objects.
        '''
        # iterate the order items (not including tax item) and get the total price
        # call recalculate on each item

        # update/create the tax order item (calculate at 7% rate)

        # update the total and save

    def finalize(self, stripe_charge_token):
        '''Runs the payment and finalizes the sale'''
        # with transaction.atomic():
            # recalculate just to be sure everything is updated

            # check that all products are available

            # contact stripe and run the payment (using the stripe_charge_token)

            # finalize (or create) one or more payment objects

            # set order status to sold and save the order

            # update product quantities for BulkProducts
            # update status for IndividualProducts


#######################################################################
# OrderItems

class OrderItem(PolymorphicModel):
    '''A line item on an order'''
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('deleted', 'Deleted'),
    )
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS_CHOICES,
                              default='active', db_index=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    # max number is 999,999.99
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)
    # max number is 999,999.99
    extended = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'OrderItem {}: {}: {}'.format(self.id, self.product.name, self.extended)

    def recalculate(self):
        '''Updates the order item's price, quantity, extended'''
        # update the price if it isn't already set and we have a product

        # default the quantity to 1 if we don't have a quantity set

        # calculate the extended (price * quantity)

        # save the changes


class Payment(models.Model):
    '''A payment on a sale'''
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)
    # max number is 999,999.99
    amount = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=2)
    validation_code = models.TextField(null=True, blank=True)
