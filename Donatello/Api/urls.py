from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView)
from Api import views

urlpatterns = [
    path('deputys/', views.DeputyList.as_view()),
    path('deputy/<int:pk>', views.DeputyDetail.as_view()),
    #path('token/logout'),
]