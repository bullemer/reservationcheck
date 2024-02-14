
from django.db import models
from django.contrib.auth.models import User
import uuid



class Ausflugspaket(models.Model):
		bezeichnung = models.CharField(null=True, max_length=50)
		content = models.CharField(null=True,default=None,  max_length=800, blank=True)
		def __str__(self):
			return(f"{self.bezeichnung}")

class Subpaket(models.Model):
		ausflugspaket = models.ForeignKey(
        Ausflugspaket, on_delete=models.SET_NULL, blank=True, null=True)
 
		bezeichnung = models.CharField(null=True, max_length=50)
		content = models.CharField(null=True, default=None, max_length=800, blank=True)

		def __str__(self):
			return(f" {self.bezeichnung}")




class Record(models.Model):

	OPTION_ONE = 'Herr'
	OPTION_TWO = 'Frau'
	OPTION_THREE = 'Divers'
	
	OPTION_A = 'Schule'
	OPTION_B = 'Verein'
	OPTION_C = 'Uni'
	OPTION_D = 'Projekt'

	TRAVEL_A = 'San Pepelone Reisebus'
	TRAVEL_B = 'Eigener Bus'
	TRAVEL_C = 'Bahn'
	TRAVEL_D = 'PKW'


	EVENT_A = 'A - Ausflugspaket'
	EVENT_B = 'B - Ausflugspaket'

	STATUS_OPEN = 'UNANSWERED'
	STATUS_EMAIL = 'EMAIL SEND'
	STATUS_ANSWERED = 'ANSWERED'
	STATUS_FINISHED = 'FINISH'

	STATUS_TYP = [
	(STATUS_OPEN, 'CREATED'),
	(STATUS_EMAIL, 'EMAIL SEND'),
	(STATUS_ANSWERED, 'ANSWERED'),
	(STATUS_FINISHED, 'FINISH'),
		]

	
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
	
	TRAVEL_TYP = [
		(TRAVEL_A, 'San Pepelone Reisebus'),
		(TRAVEL_B, 'Eigener Bus'),
		(TRAVEL_C, 'Bahn'),
		(TRAVEL_D, 'PKW'),
		]
	
	EVENT_PACKAGE = [
		(EVENT_A, 'A - Ausflugspaket'),
		(EVENT_B, 'B - Ausflugspaket'),
		]
	



	uuid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True)

	organisationtype = models.CharField( blank=True,
		max_length=20,
		choices=ORGANISATION_TYP,
		default=OPTION_A,  # Set a default value if needed
		)
	
	organisation = models.CharField(blank=True, default=None, null=True, max_length=50)

	schoolclass = models.CharField(null=True, max_length=50, blank=True)
	city =  models.CharField(blank=True, null=True, max_length=50)
	initals = models.CharField(
		max_length=20,
		choices=INITAL_TYP,
		default=OPTION_ONE,  # Set a default value if needed
		blank=True,)
	first_name = models.CharField(null=True, max_length=50)
	last_name =  models.CharField(null=True,max_length=50)
	email =  models.CharField(null=True, max_length=100)
	phone =  models.CharField(blank=True, null=True, max_length=15)

	arrival_date = models.DateField(null=True, blank=True)
	planned_arrival_time = models.CharField(blank=True, default=None, null=True, max_length=5, choices=[(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(10, 21) for m in [0, 30]])

	amount_students_male = models.PositiveIntegerField(null=True, default=None, blank=True)
	amount_students_female = models.PositiveIntegerField(null=True, default=None, blank=True)
	amount_organizer_male = models.PositiveIntegerField(null=True, default=None, blank=True)
	amount_organizer_female = models.PositiveIntegerField(null=True, default=None, blank=True)
	response_untill = models.DateField(null=True, blank=True)

	traveldetail = models.CharField(
		max_length=40,
		choices=TRAVEL_TYP,
		default=TRAVEL_B, 
		 blank=True,  # Set a default value if needed
		)
	remark =  models.CharField(null=True, max_length=800, blank=True)
	remark_client =  models.CharField(null=True, max_length=800, blank=True)
	busplan = models.FileField(upload_to='pdfs/',  null=True, blank=True)

	modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	
	status = models.CharField(
		max_length=20,
		choices=STATUS_TYP,
		default=STATUS_OPEN,
  		blank=True,# Set a default value if needed
		)
 
	ausflugspaket = models.ForeignKey(Ausflugspaket, blank=True, null=True, on_delete=models.CASCADE)
	subpaket = models.ManyToManyField(to=Subpaket, related_name = "subpakete", blank=True)
	vdws_schein = models.BooleanField(default=False)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")
	
	def update_modified_by(sender, instance, **kwargs):
    # Set modified_by only if it's not set (for creation) or if the data has changed (for modification)
		if not instance.modified_by or instance.modified_by != instance._request_user:
			instance.modified_by = instance._request_user

