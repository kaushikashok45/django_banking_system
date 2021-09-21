from django.shortcuts import render

# Create your views here.

from .models import Customer,Transaction
from django.views import generic
from urllib import request
from uuid import UUID
from .forms import InputForm
import uuid
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

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


def index2(request):
    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url="paymenthandler/"
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'index2.html', context=context)

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
            # if we don't find the required parameters in POST data
            return render(request, 'paymentsuccess.html')
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest("OK2")
