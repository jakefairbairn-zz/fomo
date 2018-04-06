from django.db import models
from catalog import models as cmod
from cuser.models import AbstractCUser
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class User(AbstractCUser):
	first_name = models.TextField(null=True, blank=True)
	last_name = models.TextField(null=True, blank=True)
	birthdate = models.DateTimeField(null=True)
	address = models.TextField(null=True, blank=True)
	city = models.TextField(null=True, blank=True)
	state = models.TextField(null=True, blank=True)
	zipcode = models.TextField(null=True, blank=True)

	def get_shopping_cart(self):

		# Retrieve the user's cart (if any)
		try:
			cart = cmod.Order.objects.get(user=self, status='cart')
		# If the user doesn't have a cart, create and save the cart object here
		except ObjectDoesNotExist:
			cart = cmod.Order.objects.create(user=self)
		# Do you need to worry about multiple carts? Only one should exist per user
		# except MultipleObjectsReturned:
			
		return cart
