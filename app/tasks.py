from celery import task
import time

from django.http import HttpResponse
from django.template import loader
from django.core.mail import send_mail

from room_order import settings


@task
def send_html(url,reveiver):
    tilte = '激活链接'  # 邮件标题
    template = loader.get_template('mail.html')  # 模板加载
    template_str = template.render({'title': '激活', 'url': url})  # 模板渲染
    receivers = [reveiver,]  # 收件人列表
    email_from = settings.DEFAULT_FROM_EMAIL  # 发件人
    send_mail(tilte, '', email_from, receivers, html_message=template_str)  # 邮件发送
    return HttpResponse('已发送')
