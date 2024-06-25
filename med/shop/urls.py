
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index), name='ShopHome'),
    path('about/', login_required(views.about), name='AboutUs'),
    path('contact/', login_required(views.contact), name='ContactUs'),
    path('tracker/', login_required(views.tracker), name='TrackingStatus'),
    path('search/', login_required(views.search), name='search'),
    path('checkout/', login_required(views.checkout), name='Checkout'),
    path('signup/', views.Signup.as_view(), name='signup'),  # No login required for signup
    path('login/', views.Login.as_view(), name='login'),  # No login required for login
    path('logout/', views.logout_view, name='logout'),  # No login required for logout
    path('products/<int:myid>/', login_required(views.productView), name='ProductView'),
    path("uploadPres/", login_required(views.uploadPres), name="uploadPres"),
    
]
