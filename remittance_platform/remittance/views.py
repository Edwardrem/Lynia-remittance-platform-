from django.shortcuts import render
from remittance.models import Transaction
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth import authenticate
from remittance.models import Transaction
# Create your views here.
def home(request):
    transactions = Transaction.objects.all()
    return render(request, 'remittance/home.html', {
        'transactions': transactions,
    })

def create_transaction(request):
    if request.method == 'POST':
        # Get the form data from the request
        form = TransactionForm(request.POST)

        # Validate the form data
        if form.is_valid():
            # Create a new transaction
            transaction = form.save()

            # Redirect the user to the home page
            return redirect('home')
    else:
        # The form hasn't been submitted yet, so show it to the user
        form = TransactionForm()

    return render(request, 'remittance/create_transaction.html', {
        'form': form,
    })

def transaction_history(request, user_id):
    user = User.objects.get(id=user_id)
    transactions = user.transactions.all()
    return render(request, 'remittance/transaction_history.html', {
        'transactions': transactions,
    })

def update_transaction_status(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)

    if request.method == 'POST':
        # Get the form data from the request
        form = TransactionStatusForm(request.POST, instance=transaction)

        # Validate the form data
        if form.is_valid():
            # Update the status of the transaction
            form.save()

            # Redirect the user to the home page
            return redirect('home')
    else:
        # The form hasn't been submitted yet, so show it to the user
        form = TransactionStatusForm(instance=transaction)

    return render(request, 'remittance/update_transaction_status.html', {
        'form': form,
    })

def login(request):
    if request.method == 'POST':
        # Get the username and password from the request
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # If the user is authenticated, log them in
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # The username or password is incorrect
            error_message = 'Invalid username or password.'
            return render(request, 'remittance/login.html', {
                'error_message': error_message,
            })
    else:
        # The user hasn't submitted the login form yet, so show it to them
        return render(request, 'remittance/login.html')

def logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        # Get the form data from the request
        form = UserCreationForm(request.POST)

        # Validate the form data
        if form.is_valid():
            # Create a new user
            user = form.save()

            # Log the user in
            login(request, user)

            # Redirect the user to the home page
            return redirect('home')
    else:
        # The form hasn't been submitted yet, so show it to the user
        form = UserCreationForm()

    return render(request, 'remittance/register.html', {
        'form': form,
    })


