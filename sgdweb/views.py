from curses import has_key
import re
from wsgiref import headers
from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
from sgdapi.models import AccountHolder
# Create your views here.

auth=('janderson.araujo', 'protege123')

def index(request):
    print(f'usuario logado: {request.user} - id: {request.user.id}')
    a = AccountHolder.objects.filter(user=request.user).first()

    data = requests.get(url='http://192.168.0.110:5001/accounts/', auth=auth, verify=False).json()
    #print(data[-1])
    potes = {
                'Liberdade Financeira': {
                                        'saldo': 100,
                                        'imagem': 'liberdade-financeira.png'
                },
                'Poupança de Longo Prazo': {
                                        'saldo': 200,
                                        'imagem': 'poupanca2.png'
                },
                'Educacao': {
                                        'saldo': 300,
                                        'imagem': 'educacao.png'
                },
                'Necessidades': {
                                        'saldo': 2000,
                                        'imagem': 'necessidades.png'
                },
                'Diversão': {
                                        'saldo': 550,
                                        'imagem': 'cerveja.png'
                },
                'Doações': {
                                        'saldo': 300,
                                        'imagem': 'doacao.png'
                }
    }

    

    pote_do_banco = data
    # pote_do_banco[1]['image'] = '"http://192.168.0.110:5001/media/liberdade-financeira.png"'
    #print(pote_do_banco)

    saldos = [100, 200, 300, 400, 500, 600]
    
    senha = 's'
    if not senha:
        return redirect('login')


    return render(request, 'index.html',
                                        {
                                            'pote_do_banco': pote_do_banco,
                                            'account_holder': a.prof_pic
                                        }
            )
    # return render(request, 'index.html', {'potes': potes})

def login(request):
    return render(request, 'login.html')

def new_account(request):
    if request.method == 'GET':
        return render(request, 'new_account.html')
        
    if request.method == 'POST':
        # files = {'file': open('/home/janderson/django/django-rest/sgd-project/sgd/static/icons/cofre.png', 'rb')}
        # headers = {'Content-Type': 'multipart/form-data'}
        data = {
            "account_name": request.POST.get('nome'),
            "description": request.POST.get('descricao'),
            "initials": get_initials_from_a_string(request.POST.get('nome')),
            "percent": request.POST.get('percentual'),
            "balance": 0,
            "account_name_real_life": request.POST.get('conta_fisica'),
            "user": request.user.accountholder.id,
            # "image": request.FILES['imagem'],
            "active": True
            }

        r = requests.post(url='http://192.168.0.110:5001/accounts/', data=data, auth=auth, verify=False)
        # print(r.text)
        print(r.content)
        return redirect(to='index')

def account_statement(request):
    data = requests.get(url='http://192.168.0.110:5001/account/59/transactions/', auth=auth, verify=False).json()
    return render(request, 'account_statement.html', {'data': data})

def deposit(request):
    return render(request, 'deposit.html')

def withdraw(request):
    return render(request, 'withdraw.html')

def trasnfer(request):
    return render(request, 'transfer.html')


def creates_standard_accouts(request, user='janderson.araujo', **kwargs): # kwargs pra pessoa dizer quais serão as contas da vida real para cada conta virtual
    db_data = requests.get(url='http://192.168.0.110:5001/accounts/', auth=auth, verify=False).json()

    standard_accounts = ['Liberdade Financeira', 'Poupança de Longo Prazo', 'Educação', 'Necessidades', 'Diversão', 'Doações']
    message = []

    for i in db_data:
        if i.get('account_name') in standard_accounts:
            standard_accounts.remove(i['account_name'])
            message.append(i['account_name'])


    data = get_standard_accounts()
    
    for account in data:
        if account['account_name'] in standard_accounts:
            requests.post(url='http://192.168.0.110:5001/accounts/', data=account, auth=auth, verify=False)
    
    return redirect('index')
    

def get_initials_from_a_string(sentence):
    if len(sentence.split()) == 1:
        return sentence

    sentence = sentence.split()
    initials = ''
    for word in sentence:
        initials = initials + word[0].upper()
    return initials



def get_standard_accounts():
    data = [
            {
                "account_name": 'Liberdade Financeira',
                "description": 'Corresponde a 10% do dinheiro que entrar. Esse dinheiro deve ser guardado com o objetivo de alcançar sua liberdade financeira. Você pode utilizá-lo para gerar sua renda passiva (é a galinha dos ovos de ouro)',
                "initials": 'LFA',
                "percent": 10,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": "janderson.araujo",
                "image": None,
                "active": True
            },
            {
                "account_name": 'Poupança de Longo Prazo',
                "description": 'Corresponde a 10% do dinheiro que entrar. Esse dinheiro é utilizado para atender objetivos de longo prazo(5%),  mas também pode ser uzado  para objetivos de curto prazo (5%). Neste caso foi considerado 5% de cada pote nessa mesma conta',
                "initials": 'PDLP',
                "percent": 10,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": "janderson.araujo",
                "image": None,
                "active": True
            },
            {
                "account_name": 'Educação',
                "description": 'Corresponde a 10% do dinheiro que entrar. Essa conta sem dúvidas é uma das mais valiosas. Essa será destinada a educação. Certificações, treinamentos, intercâmbios, etc. Além da conta Liberdade Financeira, você deve olhar para essa conta como parte disso, educação faz parte dessa liberdade',
                "initials": 'EDU',
                "percent": 10,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": "janderson.araujo",
                "image": None,
                "active": True
            },
            {
                "account_name": 'Necessidades',
                "description": 'Corresponde a 55% do dinheiro que entrar. Utilize essa conta para atender suas necessidades do dia a dia como contas de água, energia, alimentação, etc',
                "initials": 'NEC',
                "percent": 55,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": "janderson.araujo",
                "image": None,
                "active": True
            },
            {
                "account_name": 'Diversão',
                "description": 'Corresponde a 10% do dinheiro que entrar. Essa conta deve ser utilizada para curtir a vida, alegrar corpo, alma e espírito.Utilize-a para curtir de todas as formas. É importante que você gaste TODO o saldo da sua conta Diversão todos os meses;',
                "initials": 'DIV',
                "percent": 10,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": "janderson.araujo",
                "image": None,
                "active": True
            },
            {
                "account_name": 'Doações',
                "description": 'Corresponde a 5% do dinheiro que entrar. Este dinheiro é utilizado para fazer o bem ao próximo, fazer obras de caridade.Se você contrubui com o dízimo o valor deve ser tirado dessa conta;',
                "initials": 'DOA',
                "percent": 5,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": "janderson.araujo",
                "image": None,
                "active": True
            }
    ]
    return data
