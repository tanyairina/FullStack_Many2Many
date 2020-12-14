from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('quotes', views.quotes),
    path('create', views.create),
    path('quotes/<int:quote_id>', views.onequote),
    path('quotes/edit/<int:quote_id>', views.edit),
    path('quotes/update/<int:quote_id>', views.update),
    path('delete/<int:quote_id>', views.delete),
    path('favorite/<int:quote_id>', views.favorite),
    path('unfavorite/<int:quote_id>', views.unfavorite),
    path('quotes/user/<int:user_id>', views.user),
    path('quotes/others/<int:user_id>', views.others),
    path('logout', views.logout)
]
