from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Company, Contact, Address, Transaction, OTP


# فرم ثبت‌نام کاربران
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isdigit() or len(username) != 11:
            raise forms.ValidationError("شماره موبایل باید 11 رقم و عدد باشد.")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("این شماره موبایل قبلاً ثبت شده است.")
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit() or len(phone_number) != 11:
            raise forms.ValidationError("شماره موبایل باید 11 رقم و عدد باشد.")
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("این شماره موبایل قبلاً ثبت شده است.")
        return phone_number


# فرم ورود کاربران
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="شماره موبایل", max_length=15, required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isdigit() or len(username) != 11:
            raise forms.ValidationError("شماره موبایل باید 11 رقم و عدد باشد.")
        return username


# فرم تأیید OTP
class OTPForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        label="کد OTP",
        help_text="کدی که به شماره موبایل شما ارسال شد را وارد کنید."
    )

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError("کد OTP باید 6 رقم باشد.")
        return code


# فرم اطلاعات پایه کاربر
class UserBaseInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'phone_number', 'iban', 'bank_account_number',
            'bank_card_number', 'card_expiry_date', 'tax_id', 'bank_card_image'
        ]


# فرم اطلاعات شخصی کاربر
class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'full_name', 'birth_date', 'national_id', 'occupation', 'annual_income',
            'id_document_image', 'address', 'postal_code'
        ]


# فرم اطلاعات شرکت
class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'company_name', 'registration_number', 'national_id', 'economic_code',
            'office_address', 'warehouse_address', 'ceo_name', 'ceo_phone', 'ceo_email',
            'ceo_documents', 'contact_person_name', 'contact_person_position',
            'contact_person_phone', 'company_documents'
        ]


# فرم مدیریت شماره تماس کاربر
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['contact_type', 'phone_number', 'is_primary']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit() or len(phone_number) != 11:
            raise forms.ValidationError("شماره تماس باید 11 رقم باشد.")
        return phone_number


# فرم مدیریت آدرس کاربر
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'address_line', 'postal_code', 'is_primary']

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if not postal_code.isdigit() or len(postal_code) != 10:
            raise forms.ValidationError("کد پستی باید 10 رقم باشد.")
        return postal_code


# فرم مدیریت تراکنش‌ها
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'transaction_limit', 'settlement_method', 'settlement_cycle',
            'commission', 'outstanding_debt', 'total_transactions'
        ]
