from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
path('', views.home, name='home'),
path('home/<str:tab>/', views.home, name='home'),
#path('login/', views.login_user, name='login'),    
path('reservation_by_email/<str:clientemail>/', views.reservation_by_email, name='reservation_by_email'),
path('logout/', views.logout_user, name='logout'),
path('register/', views.register_user, name='register'),
path('record/<uuid:pk>', views.customer_record, name='record'),
path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
path('add_record/', views.add_record, name='add_record'),
    #path('update_record/<int:pk>', views.update_record, name='update_record'),
path('update_record/<uuid:pk>/', views.update_record, name='update_record'),
path('emails_list/', views.emails_list, name="emails_list"),
path('compose/', views.email, name="compose"),
path('email_sent/', views.email_sent, name="email_sent"),
path('email/<int:pk>/', views.email, name="email"),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
