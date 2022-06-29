from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
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

    
    
    # , '', 'Educação', 'Necessidades', 'Diversão', 'Doações'
    # }
    saldos = [100, 200, 300, 400, 500, 600]
    return render(request, 'index.html', {'potes': potes})
