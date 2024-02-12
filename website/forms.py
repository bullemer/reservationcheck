from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record
from .models import Email
from .models import Ausflugspaket, Subpaket


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
	organisation = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"organisation", "class":"form-control"}), label="")
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
	last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
	arrival_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
	planned_arrival_time = forms.ChoiceField( choices=[(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(10, 21) for m in [0, 30]], required=False, widget=forms.Select(attrs={"class":"form-control"}), label="Ankunftszeit")
	response_untill = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
	email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
	phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
	city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")
	busplan = forms.FileField(label="PDF File", required=False, widget=forms.ClearableFileInput(attrs={"class":"form-control"}))
	remark = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Bemerkung", "class":"form-control"}), label="")
	#ausflugspaket = forms.ModelChoiceField(queryset=Ausflugspaket.objects.all(), required=False, widget=forms.Select(attrs={"class":"form-control"}), label="Ausflugspaket")    
	#ausflugspaket = forms.ModelChoiceField(queryset=Ausflugspaket.objects.all(), required=False, widget=forms.Select(attrs={"class":"form-control"}), label="Ausflugspaket")
	#ausflugspaket = forms.ModelMultipleChoiceField(queryset=Ausflugspaket.objects.all(), required=False, widget=forms.SelectMultiple(attrs={"class":"form-control"}), label="Ausflugspaket")
	ausflugspaket = forms.ModelChoiceField(queryset=Ausflugspaket.objects.all(), required=False, widget=forms.Select(attrs={"class":"form-control"}), label="Ausflugspaket")
 
	#subpaket = forms.ModelMultipleChoiceField(queryset=Subpaket.objects.all(), required=False, widget=forms.SelectMultiple(attrs={"class":"form-control"}), label="Subpaket")
	subpaket = forms.ModelMultipleChoiceField(queryset=Subpaket.objects.all(), required=False, widget=forms.CheckboxSelectMultiple, label="Subpaket")
	amount_students_male    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Schüler", "class":"form-control"}), label="Anzahl Schüler")
	amount_organizer_male    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Begleiter", "class":"form-control"}), label="Anzahl Begleiter")    
	amount_organizer_female    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Begleiterinnen", "class":"form-control"}), label="Anzahl Begleiterinnen")
	amount_students_female    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Schülerinnen", "class":"form-control"}), label="Anzahl Schülerinnen")    
	traveldetail = forms.ChoiceField(choices=Record.TRAVEL_TYP, required=False, widget=forms.Select(attrs={"class":"form-control"}), label="Reisedetails")
	
	class Meta: 
		model = Record
		fields = '__all__'  # include all fields from the Record model
		ordering = ['arrival_date']
  
  
  
class UserAnswerForm(forms.ModelForm):
	arrival_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
	email = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
	phone = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
	busplan = forms.FileField(label="PDF File", required=False, widget=forms.ClearableFileInput(attrs={"class":"form-control"}))
	remark_client = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Bemerkung", "class":"form-control"}), label="")
	ausflugspaket = forms.ModelChoiceField(queryset=Ausflugspaket.objects.all(), required=False, widget=forms.Select(attrs={"class":"form-control"}), label="Ausflugspaket")    
	#subpaket = forms.ModelMultipleChoiceField(queryset=Subpaket.objects.all(), required=False, widget=forms.SelectMultiple(attrs={"class":"form-control"}), label="Subpaket")
	planned_arrival_time = forms.ChoiceField( choices=[(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(10, 21) for m in [0, 30]], required=False, widget=forms.Select(attrs={"class":"form-control"}), label="Ankunftszeit")
	subpaket = forms.ModelMultipleChoiceField(Subpaket.objects.none(), required=False, widget=forms.CheckboxSelectMultiple, label="Subpaket")
	amount_students_male    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Schüler", "class":"form-control"}), label="Anzahl Schüler")
	amount_organizer_male    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Begleiter", "class":"form-control"}), label="Anzahl Begleiter")    
	amount_organizer_female    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Begleiterinnen", "class":"form-control"}), label="Anzahl Begleiterinnen")
	amount_students_female    = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={"placeholder":"Anzahl Schülerinnen", "class":"form-control"}), label="Anzahl Schülerinnen")    
	traveldetail = forms.ChoiceField(choices=Record.TRAVEL_TYP, required=False, widget=forms.Select(attrs={"class":"form-control"}), label="Reisedetails")
	
	def __init__(self, *args, **kwargs):
		ausflugspaket_id = kwargs.pop('ausflugspaket_id', None)
		super(UserAnswerForm, self).__init__(*args, **kwargs)
		if ausflugspaket_id:
			self.fields['subpaket'].queryset = Subpaket.objects.filter(ausflugspaket_id=ausflugspaket_id)
		else:		
			self.fields['subpaket'].queryset = Subpaket.objects.all()

	class Meta: 	
		model = Record
		fields =  ['arrival_date', 'email', 'phone', 'busplan', 'remark_client', 'planned_arrival_time', 'subpaket', 'amount_students_male', 'amount_organizer_male', 'amount_organizer_female', 'amount_students_female', 'traveldetail' ]   # include all fields from the Record model
		exclude = ['organisation', 'city', 'first_name', 'last_name', 'response_untill']
		ordering = ['arrival_date']
  	

  
class EmailForm(forms.ModelForm):

    from_email = forms.EmailField(max_length=200, required=True)
    to_email = forms.EmailField(max_length=200, required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(max_length=200, required=True)

    class Meta:
        model = Email
        fields = ('from_email', 'to_email', 'subject', 'message')
