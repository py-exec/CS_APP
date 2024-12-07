from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .forms import (
    RegistrationForm, LoginForm, OTPForm, UserBaseInfoForm, TransactionForm
)
from .services import UserService, OTPService, TransactionService


# ثبت‌نام کاربر
def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, "شما قبلاً وارد سیستم شده‌اید.")
        return redirect('dashboard')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            otp_code = UserService.register_user(form)
            messages.success(request, "ثبت‌نام موفقیت‌آمیز بود. لطفاً کد تأیید را وارد کنید.")
            print(f"کد OTP: {otp_code}")
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


# ورود کاربر
def login_user(request):
    if request.user.is_authenticated:
        messages.warning(request, "شما قبلاً وارد سیستم شده‌اید.")
        return redirect('dashboard')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = UserService.authenticate_user(form.cleaned_data['username'], form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, "ورود موفقیت‌آمیز بود.")
                return redirect('dashboard')
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# تأیید OTP
@login_required
def verify_otp(request):
    if request.user.verified:
        messages.info(request, "شماره موبایل شما قبلاً تأیید شده است.")
        return redirect('dashboard')
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid() and OTPService.verify_otp(request.user, form.cleaned_data['code']):
            request.user.verified = True
            request.user.save()
            messages.success(request, "شماره موبایل تأیید شد.")
            return redirect('dashboard')
        messages.error(request, "کد واردشده نامعتبر یا منقضی شده است.")
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})


# مدیریت تراکنش‌ها
@login_required
@permission_required('app_name.can_manage_transactions', raise_exception=True)
def manage_transactions(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            TransactionService.create_transaction(request.user, form.cleaned_data)
            messages.success(request, "تراکنش جدید با موفقیت ثبت شد.")
            return redirect('manage_transactions')
    else:
        form = TransactionForm()
    total_transactions = TransactionService.calculate_total_transactions(request.user)
    return render(request, 'manage_transactions.html', {'form': form, 'total_transactions': total_transactions})
