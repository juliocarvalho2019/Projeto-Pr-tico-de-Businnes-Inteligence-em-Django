from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .admin import Dados
from django.conf import settings
from vestibular.forms import VestibularBuscaForm
import io
import matplotlib.pyplot as plt
import urllib, base64
import numpy as np

def index(request):
    form = VestibularBuscaForm(request.POST or None)
    vestibular = Dados.get_vestibular()
    dados = vestibular
    img = False
    select = request.POST.get('q')
    if request.POST:
        # valido, se select for diferente de 0;
        if form.is_valid() and select != '0':
            img = True
            labelDados = None
            sizeDados = None
            req = request.POST.get('q')
            labelDados = Dados.get_vestibular(request.POST.get('q'))
            sizeDados = Dados.get_dados(request.POST.get('q'))
            
            label = []

            size = []

            # Coluna do banco
            coluna = 'etnia','sexo','escola_origem','renda_familiar','cidade','estado','data_nascimento', 'matr_situacao'
            colunaSelecionada = None
            #Pega as opções da coluna 
            for vest in labelDados:
                if req == '1':
                    label.append(vest[coluna[0]])
                    colunaSelecionada = 'Etnia'
                elif req =='2':
                    label.append(vest[coluna[1]])
                    colunaSelecionada = 'Gênero'
                elif req =='3':
                    label.append(vest[coluna[2]])
                    colunaSelecionada = 'Escola de Origem'
                elif req =='4':
                    label.append(vest[coluna[3]])
                    colunaSelecionada = 'Renda Familiar'
                elif req =='5':
                    label.append(vest[coluna[4]])
                    colunaSelecionada = 'Cidade'
                elif req =='6':
                    label.append(vest[coluna[5]])
                    colunaSelecionada = 'Estado'
                elif req =='7':
                    label.append(vest[coluna[6]])
                    colunaSelecionada = 'Faixa Etária'
                elif req =='8':
                    label.append(vest[coluna[7]])
                    colunaSelecionada = 'Situação da Matricula'

            #Pega os dados desta coluna
            for vest in sizeDados:
                if req == '1':
                    size.append(vest[coluna[0]])
                elif req =='2':
                    size.append(vest[coluna[1]])
                elif req =='3':
                    size.append(vest[coluna[2]])
                elif req =='4':
                    size.append(vest[coluna[3]])
                elif req =='5':
                    size.append(vest[coluna[4]])
                elif req =='6':
                    size.append(vest[coluna[5]])
                elif req =='7':
                    size.append(vest[coluna[6]])
                elif req =='8':
                    size.append(vest[coluna[7]])
                
            contador_size = []
            contador = None
            for lb in label:
                contador = 0

                for sz in size:
                    if lb == sz:
                        contador = contador + 1

                contador_size.append(contador)    
            total = len(size)

            porcentagem = []

            for cnt in contador_size:
                porcentagem.append((cnt / total) * 100)
# Aqui foi feito para melhorar a visualização do gráfico para usuário final;
            explodeDinamico = []
            for pct in porcentagem:
                if pct < 0.5:
                    explodeDinamico.append(0.9)
                elif pct < 0.9 and pct > 0.5:
                    explodeDinamico.append(0.5)
                elif pct < 1.2 and pct > 0.9:
                    explodeDinamico.append(0.4)
                elif pct < 3.5 and pct > 1.2:
                    explodeDinamico.append(0.3)
                elif pct < 5 and pct > 3.5:
                    explodeDinamico.append(0.1)
                elif pct < 10 and pct > 5:
                    explodeDinamico.append(0.1)
                elif pct < 20 and pct > 10:
                    explodeDinamico.append(0.1)
                elif pct < 40 and pct > 20:
                    explodeDinamico.append(0.1)
                else:
                    explodeDinamico.append(0.1)
# Aqui, como no banco esta como f e m, substituí para masculino e femino.
            newLabel = []
            if label[0] == 'F':
                for lb in label:
                    if lb == 'M':
                        newLabel.append('Masculino')
                    else:
                        newLabel.append('Feminino')
                label = newLabel
            #Gráfico de pizza Inicio   
            labels = [(lb) for lb in label]
            sizes = porcentagem
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explodeDinamico, labels=labels, autopct='%1.1f%%',
            # aqui, defino o angulo do gráfico
            shadow=False, startangle=90)
            ax1.axis('equal')  
            #Converte para imagem
            fig = plt.gcf()
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)  
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            #Gráfico Pizza Fim

            #aqui, verifico se possui mais de 4 itens a mostrar no gráfico, se possui, não mostra estes gráficos.
            if len(label) <= 4:
                
                fig2, ax2 = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

                recipe = [(lb) for lb in label]
                
                ingredients = [(lb) for lb in label]

                data = porcentagem


                def func(pct, allvals):
                    absolute = int(pct/100.*np.sum(allvals))
                    return "{:.1f}%\n({:d})".format(pct, absolute)


                wedges, texts, autotexts = ax2.pie(data, autopct=lambda pct: func(pct, data),
                                                textprops=dict(color="w"))

                ax2.legend(wedges, ingredients,
                            title="Dados",
                            loc="center left",
                            bbox_to_anchor= [(lb) for lb in explodeDinamico])
                plt.setp(autotexts, size=10, weight="bold")
                #Converte para imagem
                fig2 = plt.gcf()
                buf2 = io.BytesIO()
                fig2.savefig(buf2, format='png')
                buf2.seek(0)
                    
                string2 = base64.b64encode(buf2.read())
                uri2 = urllib.parse.quote(string2)

            if len(label) <= 4:
                
                fig3, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

                recipe = [(lb) for lb in label]

                data = porcentagem

                wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=90)

                bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
                kw = dict(arrowprops=dict(arrowstyle="-"),
                        bbox=bbox_props, zorder=0, va="center")

                for i, p in enumerate(wedges):
                    ang = (p.theta2 - p.theta1)/2. + p.theta1
                    y = np.sin(np.deg2rad(ang))
                    x = np.cos(np.deg2rad(ang))
                    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
                    kw["arrowprops"].update({"connectionstyle": connectionstyle})
                    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                                horizontalalignment=horizontalalignment, **kw)

                #Converte para imagem
                fig3 = plt.gcf()
                buf3 = io.BytesIO()
                fig3.savefig(buf3, format='png')
                buf3.seek(0)
                    
                string3 = base64.b64encode(buf3.read())
                uri3 = urllib.parse.quote(string3)

            if req != '0':
                if len(label) <= 4:
                    lengh4 = True
                    context = {'vestibular': vestibular,
                'media_url': settings.MEDIA_URL, 'form': form, 'data':uri,'data2':uri2,'data3':uri3,'img': img, 'len': lengh4, 'label':label, 'column':colunaSelecionada, 'contador':contador_size, 'porcentagem':porcentagem}
                else:
                    lengh4 = False
                    context = {'vestibular': vestibular,
                'media_url': settings.MEDIA_URL, 'form': form, 'data':uri,'img': img, 'len': lengh4, 'label':label, 'column':colunaSelecionada, 'contador':contador_size, 'porcentagem':porcentagem}
            else:
                context = {'vestibular': vestibular,
                'media_url': settings.MEDIA_URL, 'form': form,'img': img}
        else:
            context = {'vestibular': vestibular,
               'media_url': settings.MEDIA_URL, 'form': form,'img': img}

    else:
        context = {'vestibular': vestibular,
               'media_url': settings.MEDIA_URL, 'form': form,'img': img}
    return render(request, 'vestibular/index.html', context)


def vestibular(request, pk):
    vestibular = get_object_or_404(Dados, pk=pk)

    context = {'vestibular': vestibular, 'media_url': settings.MEDIA_URL}
    return render(request, 'vestibular/vestibular.html', context)
