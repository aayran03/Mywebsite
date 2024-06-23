
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = 'ShopHome'),
    path("about/", views.about, name = 'AboutUs'),
    path("contact/", views.contact, name = 'ContactUs'),
    path("tracker/", views.tracker, name = 'TrackingStatus'),
    path("search/", views.search, name = 'search'),
    path("productview/<int:myid>/", views.productView, name='ProductView'),
    path("checkout/", views.checkout, name = 'Checkout'),
    path("signup/", views.Signup.as_view(), name='signup'),
    path("login.html/", views.Login.as_view(), name='login'),
    path("logout/", views.logout_view, name='logout'),
    
]
