from rest_framework.test import APITestCase 
from sgdapi.models import AccountHolder
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model # in order to instantiate the User model(a temporary model django creates for testing)
from django.contrib.auth.models import User #

class AccountHolderTestCase(APITestCase):
    User = get_user_model()

    def setUp(self):
        User.objects.create(username="janderson")
        user = User.objects.filter(username="janderson").get()
        self.client.force_authenticate(user)
        self.list_url = reverse('Account-Holders-list')

        self.account_holder_1 = AccountHolder.objects.create(first_name='Joel', user_id='joel.rocha', password='TeAmoPai', second_name='Araujo',
                                                            nick_name='Pintinho', email='joel.r.araujo@gmail.com', birth_date='1991-11-24', sex='M',
                                                            cep='06835390', street='Avenida Hercílio Wustemberg',number=454, district='Jardim Pinheirinho',
                                                            city='Embu das Artes', state='SP', phone='11912345678', prof_pic=None, active=True
                                                            )


    def test_get_listing_accout_holders(self):
        """Testing the get request for listing accout holders"""
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        

    