from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name="home_page"),
    path('about/',views.about_view,name="about_page"),
    path('category/',views.category_view,name="category_page"),
    path('search/',views.search_view,name="search_page"),
    path('login/',views.login_view,name="login_page"),
    path('signup/',views.signup_view,name="signup_page"),
    path('question/<int:question_id>',views.question_view,name="question_page"),
    path('add_question/',views.addquestion_view,name="addquestion_page"),
    path('profile/<int:user_id>',views.profile_view,name="profile"),

    path('logout/',views.logout_view,name="logout_page")
]
