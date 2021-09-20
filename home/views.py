from django.shortcuts import render

# Create your views here.

from .models import Customer,Transaction
from django.views import generic

def index(request):
   
    num_customers = Customer.objects.all().count()
    num_transactions = Transaction.objects.all().count()

    context = {
        'num_customers': num_customers,
        'num_transactions': num_transactions,
    }

    return render(request, 'index.html', context=context)

class CustomerListView(generic.ListView):
    model= Customer
    template_name = 'customers/customer_list.html'
 
    
