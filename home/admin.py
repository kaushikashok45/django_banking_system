from django.contrib import admin

# Register your models here.

from .models import Customer,Transaction

#admin.site.register(Customer)
#admin.site.register(Transaction)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cid','last_name', 'first_name', 'email_id', 'phone','balance','transax')

admin.site.register(Customer, CustomerAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('tid','from_cid', 'to_cid', 'amount')

admin.site.register(Transaction, TransactionAdmin)
