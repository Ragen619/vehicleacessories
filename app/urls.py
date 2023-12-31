from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm


urlpatterns = [
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),


    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),

    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    
    path('cardecoration/', views.cardecoration, name='cardecoration'),
    path('cardecoration/<slug:data>', views.cardecoration, name='cardecorationdata'),

    path('cars_serviceparts/', views.cars_serviceparts, name='cars_serviceparts'),
    path('cars_serviceparts/<slug:data>', views.cars_serviceparts, name='cars_servicepartsdata'),

    path('modifications/', views.modifications, name='modifications'),
    path('modifications/<slug:data>', views.modifications, name='modificationsdata'),

    path('bikes_serviceparts/', views.bikes_serviceparts, name='bikes_serviceparts'),
    path('bikes_serviceparts/<slug:data>', views.bikes_serviceparts, name='bikes_servicepartsdata'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

        
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),

    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),

    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

    

    path('registration/',views.CustomerRegistrationView.as_view(), name="customerregistration")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
