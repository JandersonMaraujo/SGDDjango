from rest_framework.test import APITestCase 
from sgdapi.models import AccountHolder
from django.urls import reverse
from rest_framework import status
import base64

class AccountHolderTestCase(APITestCase):
    
    def setUp(self):
        self.credentials = {
            'username': 'sgd',
            'password': 'kdfhgkjfsue84535f_UGj47'
        }
        self.list_url = reverse('Account-Holders-list')
        self.account_holder_1 = AccountHolder.objects.create(
            first_name='Joel',
            user_id='joel.rocha',
            password='TeAmoPai',
            second_name='Araujo',
            nick_name='Pintinho',
            email='joel.r.araujo@gmail.com',
            birth_date='1991-11-24',
            sex='M',
            cep='06835390',
            street='Avenida Hercílio Wustemberg',
            number=454,
            district='Jardim Pinheirinho',
            city='Embu das Artes',
            state='SP',
            phone='11912345678',
            # prof_pic=''
            # created_at='' 
            # updated_at= 
            active=True
        )


    def test_get_listing_accout_holders(self):
        """Testing the get request for listing accout holders"""
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode('sgd:kdfhgkjfsue84535f_UGj47'.encode()).decode(),
            }
        response = self.client.get(self.list_url, self.credentials)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        

    