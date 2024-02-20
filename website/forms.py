from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record
from .models import Ausflugspaket, Subpaket
from django.core.exceptions import ValidationError

class CustomDateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('format', '%d.%m.%Y')
        super().__init__(*args, **kwargs)
        

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label =''
		self.fields['username'].help_text= '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	




# Create Add Record Form
class RecordForm(forms.ModelForm):
	organisationtype = forms.ChoiceField(choices=[('', '---------')] + Record.ORGANISATION_TYP, initial='', required=True, widget=forms.Select(attrs={"class":"form-select form-select-sm"}), label="Art der Gruppe")
	organisation = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"*Name der Schule/Organisation", "class":"form-control"}), label="")
	initals = forms.ChoiceField(choices=Record.INITAL_TYP, required=False, widget=forms.Select(attrs={"class":"form-select form-select-sm"}), label="Anrede")
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"*Vorname", "class":"form-control"}), label="")
	last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"*Nachname", "class":"form-control"}), label="")
	#last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
	schoolclass = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Klasse", "class":"form-control"}), label="")
	planned_arrival_time = forms.ChoiceField( choices=[(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(10, 21) for m in [0, 30]], required=True, widget=forms.Select(attrs={"class":"form-select form-select-sm"}), label="Ankunftszeit")
	planned_departure_time = forms.ChoiceField( choices=[(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(10, 16) for m in [0, 30]], required=False, widget=forms.Select(attrs={"class":"form-select form-select-sm"}), label="Abreise")
	arrival_date = forms.DateField( widget=CustomDateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control'}),label="")
	#arrival_date = forms.DateField(widget=CustomDateInput())

 
	response_untill = forms.DateField(required=True, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control'}),label="")
	email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"*E-Mail", "class":"form-control"}), label="")
	phone = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Handynummer", "class":"form-control"}), label="")
	city = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")
	busplan = forms.FileField(label="PDF Busauftrag", required=False, widget=forms.ClearableFileInput(attrs={"class":"form-control"}))
	remark = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Bemerkung", "class":"form-control"}), label="")
	ausflugspaket = forms.ModelChoiceField(queryset=Ausflugspaket.objects.all(), required=True, widget=forms.Select(attrs={"class":"form-select form-select-sm"}), label="Bitte wähle")
	subpaket = forms.ModelMultipleChoiceField(queryset=Subpaket.objects.all(), required=False, widget=forms.CheckboxSelectMultiple, label="Subpaket")
	amount_students_male    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Schüler", "class":"form-control"}), label="Anzahl Schüler männlich")
	amount_organizer_male    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Begleiter", "class":"form-control"}), label="Anzahl Begleiter männlich")    
	amount_organizer_female    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Begleiterinnen", "class":"form-control"}), label="Anzahl Begleiter weiblich")
	amount_students_female    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Schülerinnen", "class":"form-control"}), label="Anzahl Schüler weiblich")    
	traveldetail = forms.ChoiceField(choices=Record.TRAVEL_TYP, required=False, widget=forms.Select(attrs={"class":"form-control"}), label="Anreise via")
	vdws_schein = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="VDWS Schein")

 
	class Meta: 
		model = Record
		fields = '__all__'  # include all fields from the Record model
		exclude = ['created_by', 'remark_client', 'created_by', 'status']
		ordering = ['arrival_date']
  
  
  
class UserAnswerForm(forms.ModelForm):
	arrival_date = forms.DateField(required=False, widget=forms.HiddenInput())
	email = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control", "readonly":"readonly"}), label="")
	phone = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
	busplan = forms.FileField(label="PDF File", required=False, widget=forms.ClearableFileInput(attrs={"class":"form-control"}))
	remark_client = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Bemerkung", "class":"form-control"}), label="")
	#ausflugspaket = forms.ModelChoiceField(queryset=Ausflugspaket.objects.all(), widget=forms.Select(attrs={"class":"form-control"}), label="Ausflugspaket")    
	planned_arrival_time = forms.ChoiceField( choices=[(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(10, 21) for m in [0, 30]], required=False, widget=forms.Select(attrs={"class":"form-select form-select-sm"}), label="Ankunftszeit")
	planned_departure_time = forms.ChoiceField( choices=[(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(10, 16) for m in [0, 30]], required=False, widget=forms.Select(attrs={"class":"form-select form-select-sm"}), label="Abreisezeit")
	ausflugspaket = forms.ModelChoiceField(queryset=Ausflugspaket.objects.all(), widget=forms.HiddenInput())
	subpaket = forms.ModelMultipleChoiceField(Subpaket.objects.none(), required=True, widget=forms.CheckboxSelectMultiple, label="Subpaket")
	amount_students_male    = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Schüler", "class":"form-control"}), label="Anzahl Schüler")
	amount_organizer_male    = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Begleiter", "class":"form-control"}), label="Anzahl Begleiter")    
	amount_organizer_female    = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Begleiterinnen", "class":"form-control"}), label="Anzahl Begleiterinnen")
	amount_students_female    = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Schülerinnen", "class":"form-control"}), label="Anzahl Schülerinnen")    
	traveldetail = forms.ChoiceField(choices=Record.TRAVEL_TYP, required=False, widget=forms.Select(attrs={"class":"form-select form-select-sm"}), label="Reisedetails")
	vdws_schein = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="VDWS Schein")
	organisation = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Schule/Organisation", "class":"form-control"}), label="")
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Vorname", "class":"form-control"}), label="")
	last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Nachname", "class":"form-control"}), label="")
	schoolclass = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Klasse", "class":"form-control"}), label="")
	#status = forms.ChoiceField(choices=Record.STATUS_TYP, required=False, widget=forms.Select(attrs={"class":"form-select form-select-sm"}), label="Status")

 
 
	def __init__(self, *args, **kwargs):
		ausflugspaket_id = kwargs.pop('ausflugspaket_id', None)
		ausflugspaket_bezeichnung = kwargs.pop('ausflugspaket_bezeichnung', None)
		super(UserAnswerForm, self).__init__(*args, **kwargs)
		if ausflugspaket_id:
			self.fields['subpaket'].queryset = Subpaket.objects.filter(ausflugspaket_id=ausflugspaket_id)
		else:		
			self.fields['subpaket'].queryset = Subpaket.objects.all()

   
	def clean_subpaket(self, *args, **kwargs):
		subpaket = self.cleaned_data.get('subpaket')
		ausflugspaket_bezeichnung = self.cleaned_data.get('ausflugspaket_bezeichnung')
		
		#ausflugspaket_id = self.cleaned_data.get('subpaket').first().ausflugspaket.id
  		#Wenn Ausflugspaket 2 ist , darf nur ein Subpaket ausgewählt werden.		
		if len(subpaket) > 1:
			raise ValidationError("Bei diesem Ausflugspaket darf nur ein Subpaket ausgewählt werden.")
		return subpaket

	class Meta: 	
		model = Record
		fields = '__all__'  # include all fields from the Record model
		exclude = [ 'city', 'response_untill', 'created_by', 'status', 'remark']
		ordering = ['arrival_date']
  	
   
class UserAnswerForm_readonly(forms.ModelForm):
	arrival_date = forms.DateField(required=False, widget=forms.HiddenInput())
	email = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control", "readonly":"readonly"}), label="")
	phone = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control", "readonly":"readonly"}), label="")
	busplan = forms.FileField(label="PDF File", required=False, widget=forms.ClearableFileInput(attrs={"class":"form-control", "readonly":"readonly"}))
	remark_client = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Bemerkung", "class":"form-control", "readonly":"readonly"}), label="")
	ausflugspaket = forms.ModelChoiceField(queryset=Ausflugspaket.objects.all(), widget=forms.Select(attrs={"class":"form-control", "readonly":"readonly"}), label="Ausflugspaket")    
	planned_arrival_time = forms.ChoiceField( choices=[(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(10, 21) for m in [0, 30]], required=False, widget=forms.Select(attrs={"class":"form-select form-select-sm", "readonly":"readonly"}), label="Ankunftszeit")
	planned_departure_time = forms.ChoiceField( choices=[(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(10, 16) for m in [0, 30]], required=False, widget=forms.Select(attrs={"class":"form-select form-select-sm", "readonly":"readonly"}), label="Abreisezeit")
	ausflugspaket = forms.ModelChoiceField(queryset=Ausflugspaket.objects.all(), widget=forms.HiddenInput())
	subpaket = forms.ModelMultipleChoiceField(Subpaket.objects.none(), required=False, widget=forms.CheckboxSelectMultiple, label="Subpaket")
	amount_students_male    = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Schüler", "class":"form-control", "readonly":"readonly"}), label="Anzahl Schüler")
	amount_organizer_male    = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Begleiter", "class":"form-control", "readonly":"readonly"}), label="Anzahl Begleiter")    
	amount_organizer_female    = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Begleiterinnen", "class":"form-control", "readonly":"readonly"}), label="Anzahl Begleiterinnen")
	amount_students_female    = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Schülerinnen", "class":"form-control", "readonly":"readonly"}), label="Anzahl Schülerinnen")    
	traveldetail = forms.ChoiceField(choices=Record.TRAVEL_TYP, required=False, widget=forms.Select(attrs={"class":"form-select form-select-sm", "readonly":"readonly"}), label="Reisedetails")
	vdws_schein = forms.BooleanField(required=False, widget=forms.CheckboxInput())
	organisation = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Schule/Organisation", "class":"form-control", "readonly":"readonly"}), label="")
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Vorname", "class":"form-control", "readonly":"readonly"}), label="")
	last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Nachname", "class":"form-control", "readonly":"readonly"}), label="")
	schoolclass = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Klasse", "class":"form-control", "readonly":"readonly"}), label="")


 
 
	def __init__(self, *args, **kwargs):
		ausflugspaket_id = kwargs.pop('ausflugspaket_id', None)
		ausflugspaket_bezeichnung = kwargs.pop('ausflugspaket_bezeichnung', None)
		#super(UserAnswerForm, self).__init__(*args, **kwargs)
	#	if ausflugspaket_id:
	#		self.fields['subpaket'].queryset = Subpaket.objects.filter(ausflugspaket_id=ausflugspaket_id)
	#	else:		
	#		self.fields['subpaket'].queryset = Subpaket.objects.all()

   

	class Meta: 	
		model = Record
		fields = '__all__'  # include all fields from the Record model
		exclude = [ 'city', 'response_untill', 'created_by', 'status']
		ordering = ['arrival_date']
  	