from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, RecordForm, UserAnswerForm
from .models import Record, Ausflugspaket, Subpaket
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from post_office import mail
from post_office.models import Email, Log





def home(request, tab='open'):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Du bist eingeloggt!")
            return redirect('home')
        
        if Record.objects.filter(email=username, id=password).exists():
            return redirect('reservation_by_email', clientemail=username)
        
        messages.error(request, "There Was An Error Logging In, Please Try Again...")
        return redirect('home')
    records = Record.objects.all().order_by('arrival_date')
    if tab == 'open':
        records = Record.objects.filter(arrival_date__gte=timezone.now()).order_by('arrival_date')
    elif tab == 'close':
        records = Record.objects.filter(arrival_date__lt=timezone.now()).order_by('arrival_date')
    elif tab == 'emaillog':
        records = Email.objects.all()

   

        #records = Record.objects.all().order_by('arrival_date')
        
    context = {
        'tab': tab,
        'records': records,
    }
        
    return render(request, 'home.html', context)



def reservation_by_email(request, clientemail):

	customer = Record.objects.filter(email=clientemail).first()
 
 	# Get today's date
	today = timezone.now().date()

# Get tomorrow's date
	tomorrow = today + timedelta(days=1)


	if customer is None:
		messages.success(request, f"not found {clientemail}")
	else:
		customer_orders = Record.objects.filter(email=clientemail, arrival_date__lte=tomorrow) # Replace 'orders' with the actual related name
		upcoming_orders = Record.objects.filter(email=clientemail, arrival_date__gte=tomorrow)
		ausflugspaket = Ausflugspaket.objects.all()
		context = {
			"customer_orders": customer_orders,
   			"upcoming_orders": upcoming_orders,
			"customer": customer,
			"ausflugspaket": ausflugspaket,
		}

	return render(request, 'reservation_by_email.html', context)



def logout_user(request):
	logout(request)
	messages.success(request, "Du hast dich erfolgreich ausgeloggt!")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})



def customer_record(request, pk):
	
	# Look Up Records
	customer_record = Record.objects.get(uuid=pk)
	customer_email = Email.objects.filter(to=customer_record.email)
  
	context = {
			"customer_record":customer_record,
   			"customer_email": customer_email,
		}
	if request.user.is_authenticated:
		return render(request, 'record.html', context)
	else:
		customer_record = Record.objects.get(uuid=pk)
		return render(request, 'record_customerview.html', context)




def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
	form = RecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				form.Status = "open"
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
			else: messages.error(request, form.errors)
		return render(request, 'add_record.html', {'form':form})

	else:
			messages.success(request, "You Must Be Logged In...")
			return redirect('home')
	

def update_record(request, pk):

	current_record = Record.objects.get(uuid=pk)
        
	if request.method == 'POST':
        #form = RecordForm(request.POST, request.FILES, instance=current_record)
        
		if request.user.is_authenticated:
				form = RecordForm(request.POST, request.FILES, instance=current_record)
				template = 'update_record.html' 
		else:	
				# Hier ist der nicht eingeloggte users.
				form = UserAnswerForm(request.POST, request.FILES, instance=current_record)
				template = 'user_answer_form.html'

       
		if form.is_valid():
				#instance.subpaket.set(form.cleaned_data.get('subpaket'))
			#	if not request.user.is_authenticated: form.Status = "ANSWERED"
				instance = form.save(commit=False)
				form.save()	
				#instance.subpaket.set(form.cleaned_data.get('subpaket'))
			# form.save()
				messages.success(request, "Eintrag wurde aktualisiert.")
				return redirect('home') if request.user.is_authenticated else redirect('reservation_by_email', clientemail=current_record.email)
		else:
			messages.error(request, form.errors)


	if request.user.is_authenticated:
		form = RecordForm(instance=current_record)
		template = 'update_record.html' 
		subpakete = Subpaket.objects.all()
	else:
		ausflugspaket_id = current_record.ausflugspaket.id
		form = UserAnswerForm(instance=current_record, ausflugspaket_id=ausflugspaket_id)
		now = datetime.now().date() 
		template = 'user_answer_form.html'
	#	days_until = (current_record.arrival_date - now).days	
	#	if days_until > 9:template = 'user_answer_form.html'
	#	else: template = 'sperre.html'
		
 
  
 
	context = {
        'form': form,
        'record': current_record,
     #   'ausflugspaket': Ausflugspaket.objects.all(), 
     #   'ausflugspaket_id': current_record.ausflugspaket.id,
    }
	return render(request, template, context)


def send_reminder_email(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(uuid=pk)
		link = f"http://127.0.0.1:8000/update_record/"+ str(customer_record.uuid)
  
		mail.send(
    	customer_record.email, # List of email addresses also accepted
    	'test@san-pepelone.de',
    	template='schule',
    	context = {
			"firstname": customer_record.first_name,
   			"lastname": customer_record.last_name,
			"link": link,
			"email": customer_record.email,
   			"id": customer_record.id,
		},
		priority='now',
		)
		messages.success(request, "E-Mail wurde erfolgreich versendet.")
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		customer_record = Record.objects.get(uuid=pk)
		return render(request, 'record.html', {'customer_record':customer_record})

