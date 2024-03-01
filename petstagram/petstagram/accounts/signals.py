# With signals, we can follow different situations with CRUD operations
#
# from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# UserModel = get_user_model()
#
#
# @receiver(signal=post_save, sender=UserModel)
# def send_email_on_successful_sign_up(created, instance, **kwargs):
#     if not created:
#         return
#
#     send_mail(
#         # from setting.py receiving configurations and connect with smtp server
#         subject='Welcome to Petstagram!',
#         message=f'You just signed up!',
#         from_email=None,
#         recipient_list=(instance.email,),
#     )
