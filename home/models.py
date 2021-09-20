from django.db import models
# Create your models here.

from django.urls import reverse 
from phone_field import PhoneField
import uuid

class Customer(models.Model):
    cid=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique Customer ID')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_id=models.EmailField(max_length=254,unique=True)
    balance = models.FloatField(max_length=100)
    phone=PhoneField(blank=True,help_text='Contact phone number')
    transax=models.IntegerField(default=0)
    def __str__(self):
        return  str(self.cid)

    def get_absolute_url(self):
        return reverse('customer-detail', args=[str(self.cid)]) 


class Transaction(models.Model):
    tid=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique Transaction ID')
    from_cid = models.ForeignKey('Customer',null=True,blank=True,on_delete=models.SET_NULL,editable=True,related_name='fcid')
    to_cid = models.ForeignKey('Customer',null=True,blank=True,on_delete=models.SET_NULL,editable=True,related_name='tcid')
    amount = models.FloatField(max_length=100)
    def __str__(self):
        return str(self.tid)

    def get_absolute_url(self):
        return reverse('transaction-detail', args=[str(self.tid)])




