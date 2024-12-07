from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta
from fernet_fields import EncryptedCharField


# مدل کاربر سفارشی
class CustomUser(AbstractUser):
    username = models.CharField(max_length=15, unique=True, help_text="شماره موبایل به عنوان یوزرنیم")
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    verified = models.BooleanField(default=False, help_text="آیا شماره موبایل کاربر تأیید شده است؟")
    otp_verified = models.BooleanField(default=False, help_text="آیا کد OTP تأیید شده است؟")
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    iban = models.CharField(max_length=34, null=True, blank=True)
    bank_account_number = models.CharField(max_length=20, null=True, blank=True)
    bank_card_number = models.CharField(max_length=16, null=True, blank=True)
    card_expiry_date = models.DateField(null=True, blank=True)
    tax_id = models.CharField(max_length=20, null=True, blank=True)
    bank_card_image = models.ImageField(upload_to='bank_card_images/', null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    national_id = EncryptedCharField(max_length=20, help_text="شماره ملی رمزگذاری‌شده")
    occupation = models.CharField(max_length=50, null=True, blank=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    id_document_image = models.ImageField(upload_to='id_documents/', null=True, blank=True)
    score = models.IntegerField(default=0, help_text="امتیاز کاربر")
    theme = models.CharField(max_length=10, choices=[('light', 'روشن'), ('dark', 'تاریک')], default='light')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="customuser_groups",
        blank=True,
        verbose_name="گروه‌ها",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="customuser_permissions",
        blank=True,
        verbose_name="مجوزها",
    )

    class Meta:
        permissions = [
            ("can_view_dashboard", "Can view the dashboard"),
            ("can_manage_users", "Can manage user accounts"),
            ("can_manage_transactions", "Can manage transactions"),
            ("can_view_reports", "Can view reports"),
            ("can_manage_dashboard", "Can access dashboard"),
            ("can_manage_profile", "Can manage personal profile"),
            ("can_manage_company", "Can manage company information"),
            ("can_manage_contacts", "Can manage contacts"),
            ("can_manage_addresses", "Can manage addresses"),
        ]

    def __str__(self):
        return self.username


# مدل OTP برای تأیید شماره موبایل
class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='otp')
    code = models.CharField(max_length=6, editable=False)
    expires_at = models.DateTimeField()

    def generate_code(self):
        from random import randint
        self.code = f"{randint(100000, 999999)}"
        self.expires_at = now() + timedelta(minutes=5)
        self.save()

    def is_valid(self, code):
        return self.code == code and now() < self.expires_at


# داده‌های حساس کاربر
class UserSensitiveData(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    card_number = EncryptedCharField(max_length=16, help_text="شماره کارت بانکی رمزگذاری‌شده")

    def __str__(self):
        return f"{self.user.username} - Sensitive Data"


# مدل اطلاعات شرکت‌ها
class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="company")
    company_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    national_id = models.CharField(max_length=10)
    economic_code = models.CharField(max_length=50)
    office_address = models.TextField()
    warehouse_address = models.TextField(null=True, blank=True)
    ceo_name = models.CharField(max_length=100)
    ceo_phone = models.CharField(max_length=15)
    ceo_email = models.EmailField(null=True, blank=True)
    ceo_documents = models.FileField(upload_to='ceo_documents/')
    contact_person_name = models.CharField(max_length=100)
    contact_person_position = models.CharField(max_length=50, null=True, blank=True)
    contact_person_phone = models.CharField(max_length=15)
    company_documents = models.FileField(upload_to='company_documents/')

    def __str__(self):
        return self.company_name


# مدل شماره تماس
class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="contacts")
    contact_type = models.CharField(max_length=20, choices=[('mobile', 'Mobile'), ('home', 'Home'), ('work', 'Work')])
    phone_number = models.CharField(max_length=15)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"


# مدل آدرس
class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
    address_type = models.CharField(max_length=20,
                                    choices=[('home', 'Home'), ('office', 'Office'), ('warehouse', 'Warehouse')])
    address_line = models.TextField()
    postal_code = models.CharField(max_length=10)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.address_line}"


# مدل تراکنش‌ها
class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="transactions")
    transaction_limit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    settlement_method = models.CharField(max_length=20,
                                         choices=[('bank_card', 'Bank Card'), ('iban', 'IBAN'), ('cash', 'Cash')])
    settlement_cycle = models.CharField(max_length=20, choices=[('daily', 'Daily'), ('monthly', 'Monthly')], null=True,
                                        blank=True)
    commission = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    outstanding_debt = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_transactions = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.total_transactions}"


# مدل لاگ امنیتی
class SecurityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=100, help_text="عملیات انجام‌شده")
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
