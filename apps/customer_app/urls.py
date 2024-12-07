from django.urls import path
from . import views

urlpatterns = [
    # مسیرهای ثبت‌نام، ورود و خروج
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.user_logout, name='user_logout'),

    # مسیر تأیید شماره موبایل با OTP
    path('verify-otp/', views.verify_otp, name='verify_otp'),

    # داشبورد کاربران
    path('dashboard/', views.dashboard, name='dashboard'),

    # مسیرهای مدیریت اطلاعات کاربر
    path('edit/base-info/', views.edit_user_base_info, name='edit_user_base_info'),
    path('edit/personal-info/', views.edit_personal_info, name='edit_personal_info'),

    # مسیرهای مدیریت اطلاعات شرکتی
    path('edit/company-info/', views.edit_company_info, name='edit_company_info'),

    # مسیرهای مدیریت شماره تماس‌ها
    path('manage/contacts/', views.manage_contacts, name='manage_contacts'),

    # مسیرهای مدیریت آدرس‌ها
    path('manage/addresses/', views.manage_addresses, name='manage_addresses'),

    # مسیرهای مدیریت تراکنش‌ها
    path('manage/transactions/', views.manage_transactions, name='manage_transactions'),

    path('', views.index, name='index'),
]
