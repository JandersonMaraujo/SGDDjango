from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from sgdapi.models import Account, AccountHolder, Transaction
from sgdapi.serializers import AccountSerializer, AccountHolderSerializer, TransactionSerializer, AllTransactionsForAnAccountHolderSerializer, AllTransactionsForAnAccountSerializer

# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
    """Listing all accounts"""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountHolderViewSet(viewsets.ModelViewSet):
    """Listing all AccountHolders"""
    queryset = AccountHolder.objects.all()
    serializer_class = AccountHolderSerializer
    filterset_fields = ['user_id', 'email'] # I had to install django-filter to be allowed to use it. This row means i can do something like: http://192.168.0.109:5001/account-holders?user_id=janderson.araujo&email=blablabla
    lookup_value_regex = '[^/]+' # issue abertta. As novas versões do django rest estão excluindo os caracteres "/" e ".". Fui orientado a escrever essa linha para que funcione o janderson.araujo como id de pesquisa na url

    def create(self, request): # rewriting the create method in order to send to header the key location with the uri/url for future uses (create doesnt do this by default).
        serializer = self.serializer_class(data=request.data) # serializer rceive all data from the request
        if serializer.is_valid(raise_exception=True): # It is obligatory checking the data content.
            serializer.save() # If it is ok, save data into model (because serializers always extend model)
            id = str(serializer.data['user_id']) # getting the id from the model(because it was already created. Before creation we dont have an id for it)
            response = Response(serializer.data, status=status.HTTP_201_CREATED) # The default create method has to have a response to be returned. Here we're preparing our response with the data and, which is a good practice, inform te status code
            response['Location'] = request.build_absolute_uri() + id # Finally we're creating the Location key and its value, which is the url path for this resource (plus its id :))
            return response # returning teh response with the Location. New level of maturity. Maybe it is a good idea to do it to other classes

class TransactionViewSet(viewsets.ModelViewSet):
    """Listing all Transaction"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = ['created_at',]

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