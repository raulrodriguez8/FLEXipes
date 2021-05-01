from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('results/', views.recipe_results, name='recipe_results'),
    path('results/<int:recipe_id>', views.recipe_details, name='recipe_details'),
    
]