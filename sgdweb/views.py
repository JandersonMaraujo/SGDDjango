from curses import has_key
from datetime import datetime
from wsgiref import headers
from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
from sgdapi.models import AccountHolder, Account
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

auth=('janderson.araujo', 'protege123')
server = settings.SERVER_NAME

@login_required(login_url='login/')
def index(request):
    print(f'usuario logado: {request.user} - id: {request.user.id}')
    # a = AccountHolder.objects.filter(user=request.user).first()

    data = requests.get(url=server + '/api/accounts/', auth=auth, verify=False).json()

    # pote_do_banco[1]['image'] = '"http://192.168.0.110:5001/api/apimedia/liberdade-financeira.png"'
    #print(pote_do_banco)
    
    senha = 's'
    if not senha:
        return redirect('login')

    return render(request, 'index.html',
                                        {
                                            'pote_do_banco': data,
                                            'page': 'Home',
                                            'account_holder_pic': request.user.prof_pic
                                        }
            )
    # return render(request, 'index.html', {'potes': potes})

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user=user)
            return redirect('index')
        return render(request, 'login.html')
    
    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login/')
def new_account(request):
    if request.method == 'GET':
        return render(
            request,
            'new_account.html',
            {
                'page': 'Nova Conta',
                'account_holder_pic': request.user.prof_pic
            }
        )
        
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
            "user": request.user.id,
            # "image": request.FILES['imagem'],
            "active": True
            }

        r = requests.post(url=server + '/api/accounts/', data=data, auth=auth, verify=False)
        # print(r.text)
        print(r.content)
        return redirect(to='index')
    
@login_required(login_url='login/')
def account_statement(request, account_id: int):
    data = requests.get(url=server + '/api/account/' + str(account_id) + '/transactions/', auth=auth, verify=False).json()
    
    date_list = []
    for i in data:
        i['created_at'] = datetime.strptime(i['created_at'], '%Y-%m-%d %H:%M:%S')
        compacted_date = i['created_at'].strftime('%Y-%m-%d')
        compacted_date = datetime.strptime(compacted_date, '%Y-%m-%d')

        if compacted_date not in date_list:
            date_list.append(compacted_date)

    return render(
        request,
        'account_statement.html',
        {
            'data': data,
            'page': 'Extrato',
            'account_holder_pic': request.user.prof_pic,
            'date_list': date_list
        }
    )

@login_required(login_url='login/')
def deposit(request, account_id: int):
    if request.POST:
        amount = request.POST.get('valor')
        description = request.POST.get('descricao')

        account_response = requests.get(url=server + '/api/accounts/' + str(account_id), auth=auth, verify=False)
        current_balance = account_response.json().get('balance')
        new_balance = float(current_balance) + float(amount)
        deposit_data = {
            "balance": new_balance,
        }

        account_response = requests.patch(url=server + '/api/accounts/' + str(account_id) + '/', data=deposit_data, auth=auth, verify=False)

        if account_response.status_code != 200:
            return redirect('deposit', account_id=account_id)

        transaction_data = {
            "transaction_type": "D",
            "description": description,
            "status": "Success",
            "amount": amount,
            "send_to_user": 1,
            "account": account_id,
            "send_to_account": account_id,
            'balance': new_balance
        }

        requests.post(url=server + '/api/transactions/', data=transaction_data, auth=auth, verify=False)


        return redirect(to='index')

    return render(
        request,
        'deposit.html',
        context={
            'account_id': account_id,
            'page': 'Depósito',
            'account_holder_pic': request.user.prof_pic
            }
        )

@login_required(login_url='login/')
def withdraw(request, account_id: int):
    if request.POST:
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        credit = request.POST.get('credit') == 'on'

        account_response = requests.get(url=server + '/api/accounts/' + str(account_id), auth=auth, verify=False)
        current_balance = account_response.json().get('balance')
        new_balance = float(current_balance) - float(amount)
        withdraw_data = {
            "balance": new_balance,
        }
        
        account_reponse = requests.patch(url=server + '/api/accounts/' + str(account_id) + '/', data=withdraw_data, auth=auth, verify=False)

        if account_reponse.status_code != 200:
            return redirect('withdraw', account_id=account_id)

        transaction_data = {
            "transaction_type": "S",
            "description": description,
            "status": "Success",
            "amount": amount,
            "send_to_user": request.user.id,
            "account": account_id,
            "send_to_account": account_id,
            "credit": credit,
            'balance': new_balance
        }

        r = requests.post(url=server + '/api/transactions/', data=transaction_data, auth=auth, verify=False)
        print(f'transação: {r.text}')
        return redirect(to='index')

    return render(
        request,
        'withdraw.html',
        {
            'account_id': account_id,
            'page': 'Saque',
            'account_holder_pic': request.user.prof_pic
        }
    )

@login_required(login_url='login/')
def trasnfer(request):
    return render(
        request,
        'transfer.html',
        {
            'page': 'Tranferência',
            'account_holder_pic': request.user.prof_pic
        }
    )

@login_required(login_url='login/')
def edit_account(request, account_id, account_name, account_name_real_life, description, percent):
    if request.method == 'GET':
        return render(
            request,
            'edit_account.html',
            context={
                'account_id': account_id,
                'account_name': account_name,
                'account_name_real_life': account_name_real_life,
                'description': description,
                'percent': percent
            }
        )
    
    data = {
        "account_name": request.POST.get('nome'),
        "description": request.POST.get('descricao'),
        "initials": get_initials_from_a_string(request.POST.get('nome')),
        "percent": request.POST.get('percentual'),
        "account_name_real_life": request.POST.get('conta_fisica'),
    }

    requests.patch(
        server + '/api/accounts/' + str(account_id) + '/',
        data,
        auth=auth,
        verify=False
    )
    return redirect('index')

@login_required(login_url='login/')
def delete_account(request, account_id):
    requests.delete(
        server + '/api/accounts/' + str(account_id),
        auth=auth,
        verify=False
    )
    return redirect('index')

@login_required(login_url='login/')
def creates_standard_accouts(request, user='janderson.araujo', **kwargs): # kwargs pra pessoa dizer quais serão as contas da vida real para cada conta virtual
    accounts_response = requests.get(url=server + '/api/accounts/', auth=auth, verify=False).json()

    standar_account_list = ['Liberdade Financeira', 'Poupança de Longo Prazo', 'Educação', 'Necessidades', 'Diversão', 'Doações']
    message = []

    for item in accounts_response:
        if item.get('account_name') in standar_account_list:
            standar_account_list.remove(item['account_name'])
            message.append(item['account_name'])


    standar_account_dict = get_standard_accounts(request.user.id)
    
    for account in standar_account_dict:
        if account['account_name'] in standar_account_list:
            r = requests.post(url=server + '/api/accounts/', data=account, auth=auth, verify=False)
    
    return redirect('index')
    

def get_initials_from_a_string(sentence):
    if len(sentence.split()) == 1:
        return sentence

    sentence = sentence.split()
    initials = ''
    for word in sentence:
        initials = initials + word[0].upper()
    return initials



def get_standard_accounts(user):
    data = [
            {
                "account_name": 'Liberdade Financeira',
                "description": 'Corresponde a 10% do dinheiro que entrar. Esse dinheiro deve ser guardado com o objetivo de alcançar sua liberdade financeira. Você pode utilizá-lo para gerar sua renda passiva (é a galinha dos ovos de ouro)',
                "initials": 'LFA',
                "percent": 10,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": user,
                "image": '',
                "active": True
            },
            {
                "account_name": 'Poupança de Longo Prazo',
                "description": 'Corresponde a 10% do dinheiro que entrar. Esse dinheiro é utilizado para atender objetivos de longo prazo(5%),  mas também pode ser uzado  para objetivos de curto prazo (5%). Neste caso foi considerado 5% de cada pote nessa mesma conta',
                "initials": 'PDLP',
                "percent": 10,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": user,
                "image": '',
                "active": True
            },
            {
                "account_name": 'Educação',
                "description": 'Corresponde a 10% do dinheiro que entrar. Essa conta sem dúvidas é uma das mais valiosas. Essa será destinada a educação. Certificações, treinamentos, intercâmbios, etc. Além da conta Liberdade Financeira, você deve olhar para essa conta como parte disso, educação faz parte dessa liberdade',
                "initials": 'EDU',
                "percent": 10,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": user,
                "image": '',
                "active": True
            },
            {
                "account_name": 'Necessidades',
                "description": 'Corresponde a 55% do dinheiro que entrar. Utilize essa conta para atender suas necessidades do dia a dia como contas de água, energia, alimentação, etc',
                "initials": 'NEC',
                "percent": 55,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": user,
                "image": '',
                "active": True
            },
            {
                "account_name": 'Diversão',
                "description": 'Corresponde a 10% do dinheiro que entrar. Essa conta deve ser utilizada para curtir a vida, alegrar corpo, alma e espírito.Utilize-a para curtir de todas as formas. É importante que você gaste TODO o saldo da sua conta Diversão todos os meses;',
                "initials": 'DIV',
                "percent": 10,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": user,
                "image": '',
                "active": True
            },
            {
                "account_name": 'Doações',
                "description": 'Corresponde a 5% do dinheiro que entrar. Este dinheiro é utilizado para fazer o bem ao próximo, fazer obras de caridade.Se você contrubui com o dízimo o valor deve ser tirado dessa conta;',
                "initials": 'DOA',
                "percent": 5,
                "balance": 0,
                "account_name_real_life": 'Conta Corrente Itaú',
                "user": user,
                "image": '',
                "active": True
            }
    ]
    return data
