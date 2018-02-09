from django.db import models
from cuser.models import AbstractCUser

class User(AbstractCUser):
	first_name = models.TextField(null=True, blank=True)
	last_name = models.TextField(null=True, blank=True)
	birthdate = models.DateTimeField(null=True)
	street_address = models.TextField(null=True, blank=True)
	city = models.TextField(null=True, blank=True)
	state = models.TextField(null=True, blank=True)
	zipcode = models.TextField(null=True, blank=True)

	def get_purchases(self):
		return [ 'Roku Ultimate 4', 'Skis', 'Computer' ]
