"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from balcao.views import balcao_view, novo_prod_view, venda_view, historico_view
from fornecedores.views import fornecedores_view, novo_fornec_view, novo_grupo_view, rel_simples_fornec, rel_comp_fornec, ordem_compra_view, listar_ordem_compra
from notas_fiscais.views import notas_entrada_view, notas_saida_view, get_oc_details
from accounts.views import register_view, login_view, logout_view

"""
Explicando: + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

Aqui no urls.py Usamos o static pra mapear MEDIA_URL > MEDIA_ROOT e servir
os arquivos em desenvolvimento (mapeamos que no local MEDIA_URL o arquivo
encontra-se no MEDIA_ROOT)

urls.py --> Faz o mapeamento e serve os arquivos(em desenvolvimento)

"""

urlpatterns = [
    path("", login_view, name="login"),

    path("admin/", admin.site.urls),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("balcao/", balcao_view, name="balcao_list"),
    path("grupo_fornecedor/", novo_grupo_view, name="grupo_list"),
    path("novo_produto/", novo_prod_view, name="novo_prod"),
    path("venda/", venda_view, name="venda"),
    path("historico_venda/", historico_view, name="historico_venda"),
    path("fornecedores/", fornecedores_view, name="fornec_list"),
    path("novo_fornecedor/", novo_fornec_view, name="novo_fornecedor"),
    path("ordem_compra/", ordem_compra_view, name="ordem_compra"),
    path("listar_ordens/", listar_ordem_compra, name="listar_ordens_compra"),
    path("relatorio_simples/", rel_simples_fornec, name="rel_simp_fornec"),
    path("relatorio_completo/", rel_comp_fornec, name="rel_comp_fornec"),
    path("notas_entrada/", notas_entrada_view, name="notas_entrada"),
    path("notas_saida/", notas_saida_view, name="notas_saida"),
    path('get-oc-details/<int:id_oc>/', get_oc_details, name='get_oc_details'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
