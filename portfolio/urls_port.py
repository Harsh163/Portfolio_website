from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('inner-page/', views.inner_page, name='inner'),
    path('portfolio-details/', views.portfolio_details, name='details'),
    path('import-linkedin/', views.upload_linkedin_zip, name='import_linkedin'),
]
