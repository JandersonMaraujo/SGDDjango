from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

# Create your models here.


class AccountHolder(models.Model):
    GENDER_OPTION = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('O', 'Outros')
    )

    # first_name = models.CharField(max_length=30, null=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    # password = models.CharField(max_length=200, null=False)
    # second_name = models.CharField(max_length=30)
    nick_name = models.CharField(max_length=15, null=False)
    # email = models.EmailField(max_length=50)
    birth_date = models.DateField(null=False)
    sex = models.CharField(max_length=1, choices=GENDER_OPTION, null=False, default='F')
    cep = models.CharField(max_length=8)
    street = models.CharField(max_length=200)
    number = models.IntegerField()
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    phone = models.CharField(max_length=11)
    prof_pic = models.ImageField(upload_to='pictures/%Y/%m/%d/', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.user.username


class Account(models.Model):
    #account_id = models.CharField(max_length=10, primary_key=True)
    account_name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(to=AccountHolder, on_delete=models.CASCADE)
    description = models.TextField()
    initials = models.CharField(max_length=15)
    percent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=10)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account_name_real_life = models.CharField(max_length=50)
    image = models.ImageField(blank=True)
    active = models.BooleanField(default=True)

class Transaction(models.Model):
    DEPOSITO = 'D'
    SAQUE = 'S'
    TRANSFERENCIA = 'T'
    OUTROS_DESCONTOS = 'OD'

    TRANSACTION_OPTION = (
        (DEPOSITO, 'Depósito'),
        (SAQUE, 'Saque'),
        (TRANSFERENCIA, 'Transferência'),
        (OUTROS_DESCONTOS, 'Outros descontos'),
    )

    user = models.ForeignKey(to=AccountHolder, on_delete=models.CASCADE)
    send_to_user = models.ForeignKey(to=AccountHolder, related_name='send_to_user', on_delete=models.CASCADE)
    account = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=2, choices=TRANSACTION_OPTION, null=False, default='D')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    send_to_account = models.ForeignKey(to=Account, related_name='send_to_account', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, null=True)
    