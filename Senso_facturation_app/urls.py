from django.urls import path, include
from Senso_facturation_app import views

webpages_patterns = [
    path('', views.index, name = 'index'),
    path('test', views.test, name = 'test'),
    path('accueil', views.accueil, name = 'accueil')
]

forms_patterns = [

]

github_patterns = [
    path("update_server/", views.update, name="update")
]

urlpatterns = [
    path('', include(webpages_patterns)),
    path('', include(forms_patterns)),
    path('', include(github_patterns))
]