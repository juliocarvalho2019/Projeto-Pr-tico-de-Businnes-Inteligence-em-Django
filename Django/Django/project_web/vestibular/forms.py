from django import forms
class VestibularBuscaForm(forms.Form):
 q = forms.ChoiceField(label='Opções',choices=[('0', '--Selecione--'),('1','Etnia'),('2','Gênero'),('3','Escola Origem'),('4','Renda Familiar'),('5','Cidade'),('6','Estado'),('7','Faixa Etária'),('8','Situação Matrícula')])
 #q = forms.CharField(label='Buscar', max_length=200, required=True)