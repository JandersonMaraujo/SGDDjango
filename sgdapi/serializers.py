from pkg_resources import require
from rest_framework import serializers
from sgdapi.models import Account, AccountHolder, Transaction
from sgdapi.validators import *

class AccountSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(required=False) # tirara se o upload de imagens não funcionar
    class Meta:
        model = Account
        fields = '__all__'

class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        fields = '__all__'

    def validate(self, data):
        if not valid_phone(data['phone']):
            raise serializers.ValidationError({'phone': 'Phone needs to follow the example: 11912345678'})
        
        return data

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class AllTransactionsForAnAccountHolderSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='account.user.first_name') # Não é o campo do model, mas o campo de Transaction (account), que, por aqui, pode ser navegado, pois tem referência do model Account
    sent_to = serializers.ReadOnlyField(source='send_to_account.first_name') # Teve que ser send_to_account porque há duas FK nessatabela e o background do django conflita se account(linha abaixo já usa)
    transaction_type = serializers.SerializerMethodField()
    class Meta:
        model = Transaction
        fields = ['first_name', 'sent_to', 'transaction_type','created_at', 'description', 'status']

    def get_transaction_type(self, obj):
        return obj.get_transaction_type_display()

class AllTransactionsForAnAccountSerializer(serializers.ModelSerializer):
    account_name = serializers.ReadOnlyField(source='account.account_name')
    send_to_account_name = serializers.ReadOnlyField(source='account.account_name')
    account_holder = serializers.SerializerMethodField()
    send_to_account_holder = serializers.SerializerMethodField()
    transaction_type = serializers.SerializerMethodField()
    class Meta:
        model = Transaction
        fields = ['account', 'account_name', 'send_to_account', 'send_to_account_name', 'account_holder', 'send_to_account_holder', 'transaction_type','created_at', 'description', 'status']

    def get_account_holder(self, obj):
        return f'{obj.user.first_name} {obj.user.second_name}'
    
    def get_send_to_account_holder(self, obj):
        return f'{obj.user.first_name} {obj.user.second_name}'

    def get_transaction_type(self, obj):
        return obj.get_transaction_type_display()
