from pkg_resources import require
from rest_framework import serializers
from sgdapi.models import Account, PhysicalAccount, Transaction, Log
from sgdapi.validators import *
from django.contrib.auth import get_user_model

class AccountSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(required=False) # tirara se o upload de imagens não funcionar
    class Meta:
        model = Account
        fields = '__all__'

class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password']
        # fields = ['id', 'user', 'description', 'initials', 'percent', 'balance', 'created_at', 'updated_at', 'account_name_real_life', 'image', 'active']
    
    def validate(self, data):
        if data.get('phone'):
            if not valid_phone(data['phone']):
                raise serializers.ValidationError({'phone': 'Phone needs to follow the example: 11912345678'})
        
        return data
    
class PhysicalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalAccount
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user',]

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
        fields = ['account', 'account_name', 'send_to_account', 'send_to_account_name', 'account_holder', 'send_to_account_holder', 'transaction_type','created_at', 'description', 'status', 'created_at', 'amount', 'balance']

    def get_account_holder(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    def get_send_to_account_holder(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def get_transaction_type(self, obj):
        return obj.get_transaction_type_display()

class LogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
