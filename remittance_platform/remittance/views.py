from django.shortcuts import render
from remittance.models import Transaction
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth import authenticate
from remittance.models import Transaction
from .forms import TransactionForm
from .forms import RegisterForm
from .forms import TransactionStatusForm
from django.shortcuts import redirect
from stellar_sdk import TransactionBuilder, Network, Asset
from stellar_sdk.exceptions import BaseHorizonError
from stellar_sdk import Keypair
from django.conf import settings
from .stellar_utils import server
from remittance.models import User
from .coinbase_utils import create_payment_request, generate_payment_address, check_payment_status
from django.views.decorators.csrf import csrf_exempt


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

    keypair = Keypair.random()
    public_key = keypair.public_key
    secret_key = keypair.secret
    if request.method == 'POST':
        # Get the form data from the request
        form = RegisterForm(request.POST)

        # Validate the form data
        if form.is_valid():
            # Create a new user
            user = form.save()

            # Log the user in
            login(request, user)

            # Redirect the user to the home page
            return RegisterForm('home')
    else:
        # The form hasn't been submitted yet, so show it to the user
        form = RegisterForm()

    return render(request, 'remittance/register.html', {
        'form': form,
    })


def send_transaction(request):
    # your send transaction logic here
    source_keypair = Keypair.from_secret(request.user.secret_key)
    destination_public_key = request.POST['destination_public_key']
    amount = request.POST['amount']
    asset = Asset.native()
    transaction = (
        TransactionBuilder(
            source_account=server.load_account(source_keypair.public_key),
            network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE,
            base_fee=server.fetch_base_fee(),
        )
        .append_payment_op(destination_public_key, amount, asset)
        .set_timeout(30)
        .build()
    )
    transaction.sign(source_keypair)
    response = server.submit_transaction(transaction)
    # handle response

def deposit_funds(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    amount = request.POST['amount']
    currency = request.POST['currency']
    payment_request_id = create_payment_request(amount, currency, user_id)
    payment_address = generate_payment_address(payment_request_id)
    user.payment_address = payment_address
    user.save()
    return render(request, 'remittance/deposit_funds.html', {
        'payment_address': payment_address,
    })

@csrf_exempt
def deposit_callback(request):
    payment_request_id = request.POST['payment_request_id']
    payment_status = check_payment_status(payment_request_id)
    if payment_status == 'completed':
        user = User.objects.get(payment_request_id=payment_request_id)
        user.balance += payment_status['amount']
        user.save()
    return HttpResponse(status=200)