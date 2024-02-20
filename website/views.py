from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, RecordForm, UserAnswerForm, UserAnswerForm_readonly
from .models import Record, Ausflugspaket, Subpaket
from datetime import timedelta
from django.utils import timezone
from datetime import datetime, date
from datetime import timedelta
from post_office import mail
from post_office.models import Email, Log, EmailTemplate
from django.conf import settings
import os





def home(request, tab='open'):
    
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		if user:
			login(request, user)
			messages.success(request, "Du bist eingeloggt!")
			return redirect('home')

		try:
			if Record.objects.filter(email=username, id=password).exists():
				request.session['clientemail'] = username
				dummy_user = User.objects.get(username='dummy')
				user = authenticate(request, username=dummy_user.username, password="passwordfuerdummy")
				if user is not None: login(request, user)
				return redirect('reservation_by_emailadress')

		except Exception as e:   
			messages.error(request, "There Was An Error Logging In, " + str(e))
			return redirect('home')
    
	
	if request.user.is_staff:
			records = Record.objects.all().order_by('arrival_date')
			if tab == 'open':
				records = Record.objects.filter(arrival_date__gte=timezone.now()).order_by('arrival_date')
			elif tab == 'close':
				records = Record.objects.filter(arrival_date__lt=timezone.now()).order_by('arrival_date')
			elif tab == 'emaillog':
				records = Email.objects.all()
	else:
		return render(request, 'home.html')
        
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



def reservation_by_emailadress(request):
    
	clientemail = request.session.get('clientemail')
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
	if request.user.is_staff:
		return render(request, 'record.html', context)
	else:
		customer_record = Record.objects.get(uuid=pk)
		return render(request, 'record_customerview.html', context)




def delete_record(request, pk):
	if request.user.is_staff:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
	form = RecordForm(request.POST or None)
	if request.user.is_staff:
		if request.method == "POST":
			if form.is_valid():
				#form.Status = Record.STATUS_UNANSWERED
				#add_record = form.save()
				record = form.save(commit=False)
				record.created_by = request.user
				record.status = Record.STATUS_UNANSWERED
				record.save()
				messages.success(request, "Record Added...")
				return redirect('home')
			else: messages.error(request, form.errors)
		return render(request, 'add_record.html', {'form':form})

	else:
			messages.success(request, "You Must Be Logged In...")
			return redirect('home')
	

def update_record(request, pk):

	current_record = Record.objects.get(uuid=pk)
	now = date.today()
	ausflugspaket_id = current_record.ausflugspaket.id
	days_until = 999
	show_vdws = "True"
 

	if  "surf" in str(current_record.ausflugspaket.bezeichnung.lower()): show_vdws = "True"
	else: show_vdws = "False"
        
	if request.method == 'POST':
        #form = RecordForm(request.POST, request.FILES, instance=current_record)
        
		if request.user.is_staff:
				form = RecordForm(request.POST, request.FILES, instance=current_record)
				template = 'update_record.html' 
		else:	
				# Hier ist der nicht eingeloggte users.
				form = UserAnswerForm(request.POST, request.FILES, instance=current_record)
				template = 'user_answer_form.html'

       
		if form.is_valid():
		
   
			instance = form.save(commit=False)
			#instance.created_by = request.user  # wenn nicht admin, dann ist niemand eingeloggt und der reaquestr.user ist None
			instance.save()
			instance.subpaket.set(form.cleaned_data.get('subpaket'))
			messages.success(request, "Eintrag wurde aktualisiert.")
			return redirect('home') if request.user.is_staff else redirect('reservation_by_email', clientemail=current_record.email)
		else:
			messages.error(request, form.errors)

	
    # Wenn der User eingeloggt ist, 
	if request.user.is_staff:
		form = RecordForm(instance=current_record)
		#context.update({form: RecordForm(instance=current_record)})
		template = 'update_record.html' 
		subpakete = Subpaket.objects.all()
		readonly = "False"
		
	else:  # Hier ist der nicht eingeloggte users
		if isinstance(current_record.arrival_date, date) and isinstance(now, date):
			days_until = (current_record.arrival_date - now).days
		else:
			days_until = 999  # or some default value
	
	# Wenn die Reise in weniger als 9 Tagen ist, dann ist das Formular readonly
		if days_until < 9: 
			form = UserAnswerForm_readonly(instance=current_record, ausflugspaket_id=ausflugspaket_id)
			readonly = "True"
		else:
			form = UserAnswerForm(instance=current_record, ausflugspaket_id=ausflugspaket_id)
			readonly = "False"
		
		template = 'user_answer_form.html'
		

	
		if isinstance(current_record.arrival_date, date) and isinstance(now, date):
			days_until = (current_record.arrival_date - now).days
		else:
			days_until = 999  # or some default value
		
		if days_until < 9: readonly = "True"

 
	context = {
        'form': form,
        'record': current_record,
        }
 
	context.update({'days_until': days_until, 'readonly': readonly, 'show_vdws': show_vdws,})
	return render(request, template, context)


def send_reminder_email(request, pk):
	if request.user.is_staff:
		# Look Up Records
		customer_record = Record.objects.get(uuid=pk)
		link =  request.build_absolute_uri('/') +"update_record/"+ str(customer_record.uuid)
		portallink = request.build_absolute_uri('/')
  
	# Hier werden die tags für die Emailtemplates verpackt
		context = {
			"firstname": customer_record.first_name,
   			"lastname": customer_record.last_name,
			"response_untill": customer_record.response_untill,
			"link": link,
			"portallink": portallink,
			"email": customer_record.email,
   			"id": customer_record.id,
		}
 
		if customer_record.organisationtype == "Uni":
			attachments = {
			'faq.pdf': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'faq.pdf'),
  			'hausordnung.pdf': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'hausordnung.pdf'),
			'kletterfelsenteilnahme.pdf': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'kletterfelsenteilnahme.pdf'),
			'teilnehmerliste.docx': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'teilnehmerliste.docx'),
   			'reiseinfos_uni.pdf': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'reiseinfos_uni.pdf'),

		}
		else:
			attachments = {
			'elternbrief.pdf': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'elternbrief.pdf'),
			'faq.pdf': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'faq.pdf'),
			'hausordnung.pdf': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'hausordnung.pdf'),
			'kletterfelsenteilnahme.pdf': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'kletterfelsenteilnahme.pdf'),
			'teilnehmerliste.docx': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'teilnehmerliste.docx'),
		}
		# Verschiedene Emails für verschieden Ausflugspakete für nicht uni buchungen
			if  "surf" in str(customer_record.ausflugspaket.bezeichnung.lower()):
				attachments.update({'reiseinfos1.pdf': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'reiseinfos1.pdf'),})
			else:
				attachments.update({'reiseinfos2.pdf': os.path.join(settings.BASE_DIR, 'website', 'attachments', 'reiseinfos2.pdf'),})
    
		# Send Email
			if (customer_record.busplan) and customer_record.traveldetail == "San Pepelone Reisebus":
				attachments.update({'busplan.pdf': customer_record.busplan.path})
				context.update({'wort_busauftrag': " 6. Busauftrag"})

		# Verschiedene Emailtemplates für verschieden Organistationen 
		if  customer_record.organisationtype == "Uni": emailtemplate = 'uni' 
		else: emailtemplate = 'nicht-uni'
  
		try:
			mail.send(
    			customer_record.email, # List of email addresses also accepted
    			settings.EMAIL_SENDER,
    			template=emailtemplate,
    			context=context,
				priority='now',
  				attachments=attachments,
			)
			customer_record.status = Record.STATUS_EMAILSEND
			customer_record.save()
			messages.success(request, "E-Mail wurde erfolgreich versendet." + customer_record.ausflugspaket.bezeichnung + str(context) + str(attachments))

		except Exception as e:
			messages.error(request, "Fehler beim Senden der E-Mail: " + str(e))
		
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		#customer_record = Record.objects.get(uuid=pk)
		#return render(request, 'record.html', {'customer_record':customer_record})
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')