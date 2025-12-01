from django.db import models
from Customer.models import Customer

class Product(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name

class Service(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name

class Booking(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
	booking_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Booking by {self.customer.name} on {self.booking_date.strftime('%Y-%m-%d')}"
