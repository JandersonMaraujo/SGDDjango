from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from sgdapi.models import Account, AccountHolder, Transaction, Log
from sgdapi.serializers import (AccountSerializer, AccountHolderSerializer,
                                TransactionSerializer, AllTransactionsForAnAccountHolderSerializer,
                                AllTransactionsForAnAccountSerializer, LogSerializer, LogUserSerializer
                        )
# from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
    """Listing all accounts"""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # parser_classes = (MultiPartParser, FormParser) # apagar se não funciuonar o upload de imagens

    def perform_create(self, serializer):
        log_create(self, serializer, 'create account')

    def perform_update(self, serializer):
        log_update_if_something_has_changed(self, serializer, 'update account')

    def perform_destroy(self, instance):
        log_delete(self, instance, 'delete account')


class AccountHolderViewSet(viewsets.ModelViewSet):
    """Listing all AccountHolders"""
    queryset = AccountHolder.objects.all()
    serializer_class = AccountHolderSerializer
    filterset_fields = ['username'] # I had to install django-filter to be allowed to use it. This row means i can do something like: http://192.168.0.109:5001/account-holders?user_id=janderson.araujo&email=blablabla
    lookup_value_regex = '[^/]+' # issue abertta. As novas versões do django rest estão excluindo os caracteres "/" e ".". Fui orientado a escrever essa linha para que funcione o janderson.araujo como id de pesquisa na url

    def create(self, request): # rewriting the create method in order to send to header the key location with the uri/url for future uses (create doesnt do this by default).
        serializer = self.serializer_class(data=request.data) # serializer rceive all data from the request
        if serializer.is_valid(raise_exception=True): # It is obligatory checking the data content.
            self.perform_create(serializer)
            # serializer.save() # If it is ok, save data into model (because serializers always extend model)
            id = str(serializer.data['id']) # getting the id from the model(because it was already created. Before creation we dont have an id for it)
            response = Response(serializer.data, status=status.HTTP_201_CREATED) # The default create method has to have a response to be returned. Here we're preparing our response with the data and, which is a good practice, inform te status code
            response['Location'] = request.build_absolute_uri() + id # Finally we're creating the Location key and its value, which is the url path for this resource (plus its id :))
            return response # returning teh response with the Location. New level of maturity. Maybe it is a good idea to do it to other classes
    
    def perform_create(self, serializer):
        log_create(self, serializer, 'create account holder')

    def perform_update(self, serializer):
        log_update_if_something_has_changed(self, serializer, 'update account holder')

    def perform_destroy(self, instance):
        log_delete(self, instance, 'delete account holder')

class TransactionViewSet(viewsets.ModelViewSet):
    """Listing all Transaction"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = ['created_at',]

    # def perform_create(self, serializer):
        # return serializer.save(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        log_create(self, serializer, 'create transaction')

    def perform_update(self, serializer):
        log_update_if_something_has_changed(self, serializer, 'update transaction')

    def perform_destroy(self, instance):
        log_delete(self, instance, 'delete transaction')

class AllTransactionsForAnAccountHolderView(generics.ListAPIView):
    """Listing all transactions for an account holder"""
    def get_queryset(self):
        # print(self.kwargs)
        return Transaction.objects.filter(user=self.kwargs['pk'])
    serializer_class = AllTransactionsForAnAccountHolderSerializer

class AllTransactionsForAnAccountView(generics.ListAPIView):
    """Listing all transactions for an account"""
    def get_queryset(self):
        return Transaction.objects.filter(account=self.kwargs['pk'])
    serializer_class = AllTransactionsForAnAccountSerializer

class LogView(generics.ListAPIView):
    """Listing all application loggings"""
    queryset = Log.objects.all()
    serializer_class = LogSerializer


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_create(self, serializer, event):
        # before = None
        # before = Account.objects.get(id=serializer.id)
        # before_serialized = self.get_serializer(before).data
        ip = get_client_ip(self.request)
        user = self.request.user
        user_serialized = LogUserSerializer(user).data

        # salva o objeto
        serializer.save()

        # salva o log
        log = Log(
            before={},
            after=serializer.data,
            ip=ip,
            initiated_by=user_serialized,
            event=event
        )
        log.save()

def log_update_if_something_has_changed(self, serializer, event):
    #serializa o objeto no estado anterior
    before = self.get_queryset().get(id=self.kwargs['pk'])
    before_serialized = self.get_serializer(before).data
    ip = get_client_ip(self.request)
    user = self.request.user
    user_serialized = LogUserSerializer(user).data
    # salva o objeto
    serializer.save()
    after_serialized = serializer.data
    updated_at_before_removed = before_serialized.pop('updated_at')
    updated_at_after_removed = after_serialized.pop('updated_at')

    if before_serialized != after_serialized:
        # salva o log
        before_serialized['updated_at'] = updated_at_before_removed
        after_serialized['updated_at'] = updated_at_after_removed

        log = Log(
            before=before_serialized,
            after=serializer.data,
            ip=ip,
            initiated_by=user_serialized,
            event=event
        )
        log.save()

def log_delete(self, instance, event):
    before_serialized = self.get_serializer(instance).data
    ip = get_client_ip(self.request)
    user_serialized = LogUserSerializer(self.request.user).data

    instance.delete()

    log = Log(
        before=before_serialized,
        after={},
        ip=ip,
        initiated_by=user_serialized,
        event=event
    )
    log.save()