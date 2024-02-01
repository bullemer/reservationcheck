from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from .forms import AddRecordForm



def home(request):
	records = Record.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return render(request, 'home.html', {'records': records})
		else:
			try:
				customer_record = None
				customer_record = Record.objects.get(email=username, id=password)
			except:	
				Record.DoesNotExist
				try:
					customer_record = Record.objects.get(uuid=username)
				except:
					Record.DoesNotExist
					customer_record = None

		if customer_record is not None:
			return redirect('specials' , clientreservation = password, clientemail = username)#render (request,'specials.html',{'customer_record':customer_record})
		else: ## Kein Superuser und keine Reervierung
			messages.error(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records': records})
	
	
	q = Entry.objects.filter(headline__startswith="What")


def specials(request, clientreservation, clientemail):
    try:
        # Use .filter() to get a queryset of matching records
        customer = Record.objects.filter(email=clientemail, id=clientreservation).first()

        if customer:
            # Assuming orders are stored within the customer model
            customer_orders = Record.objects.all()  # Replace 'orders' with the actual related name
        else:
            customer_orders = None

    except Record.DoesNotExist:
        customer = None
        customer_orders = None
        messages.success(request, "not found" + clientreservation + " " + clientemail)

    # Create a dictionary with the variables
    return render(request, 'specials.html', {'customer_orders': customer_orders, 'customer': customer})



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
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



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
	form = AddRecordForm(request.POST or None)
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
	current_record = Record.objects.get(id=pk)
	template = 'update_record.html'
	
	if request.method == 'POST':
		if request.user.is_authenticated:
			form = AddRecordForm(request.POST, request.FILES, instance=current_record)
		else:
			# If the user is not logged in, create a form without the user-specific fields
			template = 'update_record_by_user.html'
			form = AddRecordForm(request.POST, instance=current_record)

		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
	else:
        # Handle GET requests separately to display the form
		if request.user.is_authenticated:
			form = AddRecordForm(instance=current_record)
		else:
			template = 'update_record_by_user.html'
			form = AddRecordForm(instance=current_record)
	return render(request, template, {'form': form})

