from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company, Contact, Address, Transaction, OTP


# مدیریت ادمین برای مدل CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'phone_number', 'email', 'verified', 'otp_verified',
        'score', 'theme', 'is_active', 'is_staff', 'date_joined', 'last_login'
    )
    list_filter = ('is_active', 'is_staff', 'verified', 'otp_verified', 'theme', 'date_joined')
    search_fields = ('username', 'phone_number', 'email', 'full_name', 'national_id')
    ordering = ('-date_joined',)

    fieldsets = (
        ('اطلاعات ورود', {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('full_name', 'birth_date', 'phone_number', 'email', 'address', 'postal_code')}),
        ('اطلاعات بانکی', {'fields': ('iban', 'bank_account_number', 'bank_card_number',
                                      'card_expiry_date', 'tax_id', 'bank_card_image')}),
        ('اطلاعات تأیید', {'fields': ('verified', 'otp_verified')}),
        ('تنظیمات کاربری', {'fields': ('score', 'theme')}),
        ('مجوزها و گروه‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'password1', 'password2', 'phone_number', 'email', 'is_active', 'is_staff', 'is_superuser')}
         ),
    )


# مدیریت ادمین برای مدل OTP
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'expires_at')
    list_filter = ('expires_at',)
    search_fields = ('user__username', 'code')
    readonly_fields = ('user', 'code', 'expires_at')


# مدیریت ادمین برای مدل Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'company_name', 'registration_number', 'national_id',
        'ceo_name', 'ceo_phone', 'contact_person_name'
    )
    list_filter = ('company_name', 'ceo_name')
    search_fields = ('company_name', 'registration_number', 'ceo_name', 'contact_person_phone')
    readonly_fields = ('user',)


# مدیریت ادمین برای مدل Contact
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_type', 'phone_number', 'is_primary')
    list_filter = ('contact_type', 'is_primary')
    search_fields = ('user__username', 'phone_number')


# مدیریت ادمین برای مدل Address
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_type', 'postal_code', 'is_primary')
    list_filter = ('address_type', 'is_primary')
    search_fields = ('user__username', 'address_line', 'postal_code')


# مدیریت ادمین برای مدل Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'transaction_limit', 'settlement_method',
        'outstanding_debt', 'total_transactions', 'settlement_cycle'
    )
    list_filter = ('settlement_method', 'settlement_cycle')
    search_fields = ('user__username', 'settlement_method')
    readonly_fields = ('user',)


# ثبت مدل‌های سفارشی‌شده در ادمین
admin.site.register(CustomUser, CustomUserAdmin)
