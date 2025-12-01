from django.db import models

class Customer(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	# Add more fields as needed

	def __str__(self):
		return self.name
