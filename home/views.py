from django.shortcuts import render

# Create your views here.

from .models import Customer,Transaction
from django.views import generic
from urllib import request
from uuid import UUID
from .forms import InputForm
import uuid

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
 

class CustomerDetailView(generic.DetailView):
    model = Customer
    
 


def transac(request,cid):
    fcid=cid
    context={
       'fcid':fcid,
    }
    context["customer_list"] = Customer.objects.all().exclude(cid__exact=fcid)
    return render(request,'paylist.html',context)

class CustomerPayView(generic.DetailView):
    model = Customer


def pay(request,tcid,fcid):
    context={
       'fcid':fcid,
       'tcid':tcid,
       'form':InputForm(),
    }
    return render(request,'payment.html',context)

def process(request,tcid,fcid):
    amountr=request.POST['amount']
    fc = Customer.objects.get(cid=fcid)
    tc = Customer.objects.get(cid=tcid)
    if float(amountr)>fc.balance:
         return render(request,'error.html')
    elif float(amountr)<1.0:
         return render(request,'error2.html')
    else:
      fc.balance=fc.balance-float(amountr)
      tc.balance=tc.balance+float(amountr)
      fc.transax=fc.transax+1
      tc.transax=tc.transax+1
      fc.save()
      tc.save()
      tuuid=uuid.uuid4()
      context={
        'tid':tuuid,
      }
      payment=Transaction(tid=tuuid,from_cid=Customer.objects.get(cid=fcid),to_cid=Customer.objects.get(cid=tcid),amount=amountr)
      payment.save()
      return render(request,'success.html',context)
