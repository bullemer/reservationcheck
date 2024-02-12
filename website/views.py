from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, RecordForm, UserAnswerForm
from .models import Record, Ausflugspaket, Subpaket
from datetime import timedelta
from django.utils import timezone
from .models import Email
from .forms import EmailForm
from datetime import datetime
from datetime import timedelta








def home(request, tab='open'):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        
        if Record.objects.filter(email=username, id=password).exists():
            return redirect('reservation_by_email', clientemail=username)
        
        messages.error(request, "There Was An Error Logging In, Please Try Again...")
        return redirect('home')
    records = Record.objects.all().order_by('arrival_date')
    if tab == 'open':
        records = Record.objects.filter(arrival_date__gte=timezone.now()).order_by('-arrival_date')
    elif tab == 'close':
        records = Record.objects.filter(arrival_date__lt=timezone.now()).order_by('-arrival_date')

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
	messages.success(request, "You Have Been Logged Out...")
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
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(uuid=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		customer_record = Record.objects.get(uuid=pk)
		return render(request, 'record.html', {'customer_record':customer_record})




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
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
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
				form = UserAnswerForm(request.POST, request.FILES, instance=current_record)
				template = 'user_answer_form.html'
       
		if form.is_valid():
				#instance.subpaket.set(form.cleaned_data.get('subpaket'))
				instance = form.save(commit=False)
				instance.save()
				form.save()	
				#instance.subpaket.set(form.cleaned_data.get('subpaket'))
			# form.save()
				messages.success(request, "Record Has Been Updated!")
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
		template = 'user_answer_form.html'
 
  
 
	context = {
        'form': form,
        'record': current_record,
     #   'ausflugspaket': Ausflugspaket.objects.all(), 
     #   'ausflugspaket_id': current_record.ausflugspaket.id,
    }
	return render(request, template, context)


def emails_list(request):
    filter_list = Email.objects.all()
    if request.GET.get('from_date', ''):
        from_date = request.GET.get('from_date', '')
        fd = datetime.strptime(from_date, "%Y-%m-%d").date()
        filter_list = filter_list.filter(send_time__gte=fd)
    if request.GET.get('to_date', ''):
        to_date = request.GET.get('to_date', '')
        td = datetime.strptime(to_date, "%Y-%m-%d")
        td = td + timedelta(seconds=(24 * 60 * 60 - 1))
        filter_list = filter_list.filter(send_time__lte=td)
    if request.GET.get('name', ''):
        name = request.GET.get('name', '')
        filter_list = filter_list.filter(to_email__startswith=name)
    return render(request, 'mail_all.html', {
        'filter_list': filter_list})

def email(request):
    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            from_email = request.POST.get('from_email', '')
            to_email = request.POST.get('to_email', '')
            file = request.FILES.get('files', None)
            status = request.POST.get('email_draft', '')
            email = EmailMessage(subject, message, from_email, [to_email])
            email.content_subtype = "html"
            f = form.save()
            if file is not None:
                email.attach(file.name, file.read(), file.content_type)
                f.file = file
            if status:
                f.status = "draft"
            else:
                email.send(fail_silently=False)
            f.save()
            return HttpResponseRedirect(reverse('emails:list'))
        else:
            return render(request, 'create_mail.html', {'form': form})
    else:
        form = EmailForm()
        return render(request, 'create_mail.html', {'form': form})


def email_sent(request):
    filter_list = Email.objects.filter(status="sent")
    if request.GET.get('from_date', ''):
        from_date = request.GET.get('from_date', '')
        fd = datetime.strptime(from_date, "%Y-%m-%d").date()
        filter_list = filter_list.filter(send_time__gte=fd)
    if request.GET.get('to_date', ''):
        to_date = request.GET.get('to_date', '')
        td = datetime.strptime(to_date, "%Y-%m-%d")
        td = td + timedelta(seconds=(24 * 60 * 60 - 1))
        filter_list = filter_list.filter(send_time__lte=td)
    if request.GET.get('name', ''):
        name = request.GET.get('name', '')
        filter_list = filter_list.filter(to_email__startswith=name)
    return render(request, 'mail_sent.html',
                  {'filter_list': filter_list})
