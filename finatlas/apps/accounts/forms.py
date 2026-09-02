from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Assessor


CSS_INPUT = "w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal focus:border-teal outline-none text-sm text-slate-800"

# Cria a conta de usuário (CustomUser) e o perfil (Assessor) ao mesmo tempo.
class CadastrarAssessorForm(forms.Form):
    
    first_name = forms.CharField(label="Nome", max_length=50, widget=forms.TextInput(attrs={"class": CSS_INPUT}))
    last_name = forms.CharField(label="Sobrenome", max_length=50, widget=forms.TextInput(attrs={"class": CSS_INPUT}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class": CSS_INPUT}))
    username = forms.CharField(label="Usuário", max_length=150, widget=forms.TextInput(attrs={"class": CSS_INPUT, "placeholder": "Ex: nome.sobrenome"}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={"class": CSS_INPUT}))
    codigo_assessor = forms.CharField(label="Código do Assessor", max_length=30, widget=forms.TextInput(attrs={"class": CSS_INPUT, "placeholder": "Ex: A12345"}))
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Já existe um usuário com este e-mail.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username
    
    def clean_codigo_assessor(self):
        codigo = self.cleaned_data["codigo_assessor"]
        
        if Assessor.objects.filter(codigo_assessor=codigo).exists():
            raise forms.ValidationError("Já existe um assessor com este código.")
        return codigo
    
    def save(self):
        data = self.cleaned_data
        
        # Cria o usuário com o perfil de ASSESSOR
        user = CustomUser.objects.create(
            username=data["username"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            role=CustomUser.Role.ASSESSOR,
            password=make_password(data["password"]),
        )
         
        # Cria o perfil de Assessor vinculado ao usuário criado
        assessor = Assessor.objects.create(
            user=user,
            codigo_assessor=data["codigo_assessor"],
        )

        return assessor


class EditarAssessorForm(forms.Form):
    first_name = forms.CharField(label="Nome", max_length=50, widget=forms.TextInput(attrs={"class": CSS_INPUT}))
    last_name = forms.CharField(label="Sobrenome", max_length=50, widget=forms.TextInput(attrs={"class": CSS_INPUT}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class": CSS_INPUT}))
    codigo_assessor = forms.CharField(label="Código do Assessor", max_length=30, widget=forms.TextInput(attrs={"class": CSS_INPUT}))
    is_active = forms.BooleanField(label="Assessor Ativo", required=False)
    nova_senha = forms.CharField(
        label="Nova senha (opcional)",
        required=False,
        widget=forms.PasswordInput(attrs={"class": CSS_INPUT, "placeholder": "Deixe em branco para não alterar"}),
    )
    
    def __init__(self, *args, assessor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._assessor = assessor
        
        # Preenche os campos com os valores atuais do assessor
        if assessor:
            self.fields["first_name"].initial = assessor.user.first_name
            self.fields["last_name"].initial = assessor.user.last_name
            self.fields["email"].initial = assessor.user.email
            self.fields["codigo_assessor"].initial = assessor.codigo_assessor
            self.fields["is_active"].initial = assessor.is_active
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        
        # Permite manter o e-mail atual dele, mas não deixa usar o e-mail de outro usuário
        if CustomUser.objects.filter(email=email).exclude(pk=self._assessor.user.pk).exists():
            raise forms.ValidationError("Já existe outro usuário com este e-mail.")
        return email
    
    def clean_codigo_assessor(self):
        codigo = self.cleaned_data["codigo_assessor"]
        
        # Permite manter o código atual dele, mas não deixa duplicar com outro assessor
        if Assessor.objects.filter(codigo_assessor=codigo).exclude(pk=self._assessor.pk).exists():
            raise forms.ValidationError("Já existe outro assessor com este código.")
        return codigo
    
    def save(self):
        data = self.cleaned_data
        user = self._assessor.user
        
        # Atualiza o CustomUser
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.is_active = data["is_active"]
        if data["nova_senha"]:
            user.password = make_password(data["nova_senha"])
        user.save()

        # Atualiza o Assessor
        self._assessor.codigo_assessor = data["codigo_assessor"]
        self._assessor.is_active = data["is_active"]
        self._assessor.save()
        
        return self._assessor