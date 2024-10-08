"""
URL configuration for azarovProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from payments import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.payment_view, name='payment'),
    path('payment/webhook/', views.payment_webhook_view, name='payment_webhook'),
    path('payment/success', views.payment_success_view, name='payment_success'),
    path('info/', views.info_view, name='info'),
    path('add_child/', views.add_child_view, name='add_child'),
    path('child/<int:pk>/', views.child_detail_view, name='child_detail'),
    path('get_children/', views.get_children, name='get_children'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('pdfs/', views.pdf_page_view, name='pdf_list'),
    path('results', views.business_summary, name='results'),
    path('applications/', views.application_list, name='applications'),
    path('applications/<int:pk>/update/', views.application_update, name='application-update'),
    path('admin-page', views.admin_page, name='admin_page')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)