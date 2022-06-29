from rest_framework.test import APITestCase 
from sgdapi.models import AccountHolder

class AccountHolderTestCase(APITestCase):
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
    
    def test_verify_account_holder_atributes(self):
        """Test that verifies default values for an account holder"""
        self.assertEqual(self.account_holder.first_name, 'Jorge')
        self.assertEqual(self.account_holder.user_id, 'jorge.araujo')
        self.assertEqual(self.account_holder.password, 'teste123')
        self.assertEqual(self.account_holder.second_name, 'Araujo')
        self.assertEqual(self.account_holder.nick_name, 'Jorge')
        self.assertEqual(self.account_holder.email, 'jorge.araujo@gmail.com')
        self.assertEqual(self.account_holder.birth_date, '1981-11-28')
        self.assertEqual(self.account_holder.cep, '06835390')
        self.assertEqual(self.account_holder.street, 'Av. Hercílio Wustemberg')
        self.assertEqual(self.account_holder.number, 454)
        self.assertEqual(self.account_holder.district, 'Jd. Pinheirinho')
        self.assertEqual(self.account_holder.city, 'Embu das Artes')
        self.assertEqual(self.account_holder.state, 'SP')
        self.assertEqual(self.account_holder.phone, '11912345678')
        self.assertEqual(self.account_holder.prof_pic, '')