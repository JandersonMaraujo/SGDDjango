from django.forms import ImageField
from rest_framework.test import APITestCase 
from sgdapi.models import AccountHolder
from sgdapi.serializers import AccountHolderSerializer, serializers

class AccountHolderSerializerTestCase(APITestCase):
    def setUp(self):
        self.account_holder = AccountHolder(
                                    first_name='Jorge',
                                    user_id='jorge.araujo',
                                    password='teste123',
                                    second_name='Araujo',
                                    nick_name='Jorge',
                                    email='jorge.araujo@gmail.com',
                                    birth_date='1981-11-28',
                                    cep='06835390',
                                    street='Av. Hercílio Wustemberg',
                                    number=454,
                                    district='Jd. Pinheirinho',
                                    city='Embu das Artes',
                                    state='SP',
                                    phone='11912345678',
                                    sex='M',
                                    prof_pic=''
                            )
        self.serializer = AccountHolderSerializer(instance=self.account_holder)
    

    def test_verify_account_holder_serialized_fields(self):
        """Test that verifies serialized fields"""
        data = self.serializer.data # all fields from serializer
        self.assertEqual(set(data.keys()), set(['first_name', 'user_id', 'second_name', 'nick_name', 'email', 'birth_date', 'cep', 'street', 'number', 'district', 'city', 'state', 'phone', 'prof_pic', 'active', 'created_at', 'sex', 'updated_at']))

    def test_verify_account_holder_content_of_fields_serialized(self):
        """Teste that verifies the content serialized"""
        data = self.serializer.data
        self.assertEqual(data['first_name'], self.account_holder.first_name) # verifying wether the value passed from is the same as the
        self.assertEqual(data['user_id'], self.account_holder.user_id)
        self.assertEqual(data['second_name'], self.account_holder.second_name)
        self.assertEqual(data['nick_name'], self.account_holder.nick_name)
        self.assertEqual(data['email'], self.account_holder.email)
        self.assertEqual(data['birth_date'], self.account_holder.birth_date)
        self.assertEqual(data['cep'], self.account_holder.cep)
        self.assertEqual(data['street'], self.account_holder.street)
        self.assertEqual(data['number'], self.account_holder.number)
        self.assertEqual(data['district'], self.account_holder.district)
        self.assertEqual(data['city'], self.account_holder.city)
        self.assertEqual(data['state'], self.account_holder.state)
        self.assertEqual(data['phone'], self.account_holder.phone)