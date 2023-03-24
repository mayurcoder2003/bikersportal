from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path("brands/", views.index, name="ShopHome"),
    path("",views.home,name="home"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    # Mechanic
    path('mechanic/',views.BookMechanicView,name="mechanics"),
    path('mechanic/book/<int:pk>/',views.BookInnerView,name='book_mechanic'),
    path('mechanic/<int:pk>/update/',views.UpdateBookMechanic.as_view(),name="update_mechanic"),
    # Signup
    path('login/',views.Login,name="login"),
    path('signup/',views.Signup,name="signup"),
    path("logout/",views.Logout,name="logout"),
    path('profile/',views.MyProfile,name="my_profile"),
    path('profile/edit/',views.update_profile,name="update_myprofile"),
    path('profile/change_password/',views.ChangePassword,name="change_password"),
    path('profile/change_photo/',views.ChangeProfilePhoto,name='change_profile_photo'),
    # Book Now
    path('book/<int:pk>/',views.booknow,name='booknow'),
]
