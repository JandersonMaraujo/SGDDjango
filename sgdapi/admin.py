from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from sgdapi.models import Account, AccountHolder, Transaction

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'account_name', 'description', 'initials', 'balance', 'created_at', 'updated_at', 'account_name_real_life', 'active')
    list_display_links = ('id', 'account_name')
    search_fields = ('account_name',)
    list_per_page = 20

# class AccountHolderAdmin(admin.ModelAdmin):
#     list_display = ('user_id', 'nick_name', 'birth_date', 'sex', 'cep', 'street', 'number', 'district', 'city', 'state', 'phone', 'created_at', 'updated_at', 'active')
#     list_display_links = ('user_id', )
#     search_fields = ('user_id',)
#     list_per_page = 20
#     list_filter = ('user_id',)
#     ordering = ('user_id',)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'account', 'transaction_type', 'created_at', 'description', 'send_to_account', 'status')
    list_display_links = ('user',)
    search_fields = ('user',)
    list_per_page = 20


admin.site.register(AccountHolder, UserAdmin)
admin.site.register(Account, AccountAdmin)
# admin.site.register(AccountHolder, AccountHolderAdmin)
admin.site.register(Transaction, TransactionAdmin)

