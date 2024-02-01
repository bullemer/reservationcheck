from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid


class Record(models.Model):

	OPTION_ONE = 'Herr'
	OPTION_TWO = 'Frau'
	OPTION_THREE = 'Divers'
	
	OPTION_A = 'Schule'
	OPTION_B = 'Verein'
	OPTION_C = 'Uni'
	OPTION_D = 'Projekt'
	
	INITAL_TYP = [
		(OPTION_ONE, 'Herr'),
		(OPTION_TWO, 'Frau'),
		(OPTION_THREE, 'Divers'),
		]

	ORGANISATION_TYP = [
        (OPTION_A, 'Schule'),
        (OPTION_B, 'Verein'),
        (OPTION_C, 'Uni'),
		(OPTION_D, 'Projekt'),
    ]	
	
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)

	organisationtype = models.CharField(
		max_length=20,
		choices=ORGANISATION_TYP,
		default=OPTION_A,  # Set a default value if needed
		)
	
	organisation = models.CharField(null=True, max_length=50)

	schoolclass = models.CharField(null=True, max_length=50)
	city =  models.CharField(null=True, max_length=50)
	initals = models.CharField(
		max_length=20,
		choices=INITAL_TYP,
		default=OPTION_ONE,  # Set a default value if needed
		)
	first_name = models.CharField(null=True, max_length=50)
	last_name =  models.CharField(null=True,max_length=50)
	email =  models.CharField(null=True, max_length=100)
	phone =  models.CharField(null=True, max_length=15)

	arrival_date = models.DateTimeField(null=True)
	response_untill = models.DateTimeField(null=True)
	
	remark =  models.CharField(null=True, max_length=800, blank=True)
	busplan = models.FileField(upload_to='pdfs/',  null=True, blank=True)


	modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return(f"{self.first_name} {self.last_name}")
	
	def update_modified_by(sender, instance, **kwargs):
    # Set modified_by only if it's not set (for creation) or if the data has changed (for modification)
		if not instance.modified_by or instance.modified_by != instance._request_user:
			instance.modified_by = instance._request_user


def save(self, *args, **kwargs):
	if not self.reservation:
            # Set a default value if it doesn't exist
            # You can use any logic here to generate a unique value
		self.reservation = generate_unique_reservation_value()
		super().save(*args, **kwargs)
