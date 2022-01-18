from django.urls import path
from . import views


urlpatterns = [
    path("",views.home,name="home_page"),
    path("file/",views.file_check,name="file_checking"),
    path('set_feedback/<slug:pk>/',views.feedback,name="feedback"),
    path('get_terms/',views.get_terms,name="terms"),
    path('privacypolicy/',views.privacypolicy,name="PrivacyPolicy")
    # path("set_language/<str:user_language>/", views.set_language_from_url, name="set_language_from_url")
    
    
]


