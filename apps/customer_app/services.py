from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction as db_transaction
from django.contrib.auth import authenticate
from random import randint
from .models import OTP, Transaction, CustomUser
import logging

logger = logging.getLogger(__name__)


# سرویس مدیریت OTP
class OTPService:
    @staticmethod
    def generate_otp(user):
        try:
            otp, created = OTP.objects.get_or_create(user=user)
            otp.code = f"{randint(100000, 999999)}"
            otp.expires_at = now() + timedelta(minutes=5)
            otp.save()
            logger.info(f"OTP برای کاربر {user.username} تولید شد.")
            return otp.code
        except Exception as e:
            logger.error(f"خطا در تولید OTP: {e}")
            raise Exception("خطا در تولید کد تأیید")

    @staticmethod
    def verify_otp(user, code):
        try:
            otp = OTP.objects.get(user=user)
            if otp.is_valid(code):
                otp.delete()
                logger.info(f"OTP برای کاربر {user.username} تأیید شد.")
                return True
            logger.warning(f"OTP واردشده توسط کاربر {user.username} نامعتبر است.")
            return False
        except OTP.DoesNotExist:
            logger.warning(f"OTP برای کاربر {user.username} یافت نشد.")
            return False

    @staticmethod
    def resend_otp(user):
        return OTPService.generate_otp(user)


# سرویس مدیریت کاربر
class UserService:
    @staticmethod
    def register_user(form):
        try:
            user = form.save()
            otp_code = OTPService.generate_otp(user)
            logger.info(f"کاربر {user.username} ثبت‌نام کرد و OTP ارسال شد.")
            return otp_code
        except Exception as e:
            logger.error(f"خطا در ثبت‌نام کاربر: {e}")
            raise Exception("خطا در ثبت‌نام کاربر")

    @staticmethod
    def authenticate_user(username, password):
        user = authenticate(username=username, password=password)
        if user:
            logger.info(f"کاربر {username} با موفقیت وارد شد.")
        else:
            logger.warning(f"تلاش ناموفق برای ورود با نام کاربری {username}")
        return user

    @staticmethod
    def update_base_info(user, data):
        try:
            user.phone_number = data.get("phone_number", user.phone_number)
            user.email = data.get("email", user.email)
            user.save()
            logger.info(f"اطلاعات پایه کاربر {user.username} به‌روزرسانی شد.")
        except Exception as e:
            logger.error(f"خطا در به‌روزرسانی اطلاعات کاربر: {e}")
            raise Exception("خطا در به‌روزرسانی اطلاعات کاربر")

    @staticmethod
    def increase_user_score(user, points):
        user.score += points
        user.save()
        logger.info(f"امتیاز کاربر {user.username} به {user.score} افزایش یافت.")


# سرویس مدیریت تراکنش
class TransactionService:
    @staticmethod
    @db_transaction.atomic
    def create_transaction(user, data):
        try:
            transaction = Transaction.objects.create(
                user=user,
                transaction_limit=data.get("transaction_limit"),
                settlement_method=data.get("settlement_method"),
                settlement_cycle=data.get("settlement_cycle"),
                commission=data.get("commission"),
                outstanding_debt=data.get("outstanding_debt"),
                total_transactions=data.get("total_transactions"),
            )
            logger.info(f"تراکنش برای کاربر {user.username} ایجاد شد.")
            return transaction
        except Exception as e:
            logger.error(f"خطا در ایجاد تراکنش برای کاربر {user.username}: {e}")
            raise Exception("خطا در ثبت تراکنش")

    @staticmethod
    def calculate_total_transactions(user):
        transactions = Transaction.objects.filter(user=user)
        total = sum(t.total_transactions or 0 for t in transactions)
        logger.info(f"مجموع تراکنش‌های کاربر {user.username}: {total}")
        return total


# سرویس ارسال ایمیل
class EmailService:
    @staticmethod
    def send_email(subject, message, recipient_list):
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            logger.info(f"ایمیل با موضوع '{subject}' به {recipient_list} ارسال شد.")
        except Exception as e:
            logger.error(f"خطا در ارسال ایمیل به {recipient_list}: {e}")
            raise Exception("خطا در ارسال ایمیل")
