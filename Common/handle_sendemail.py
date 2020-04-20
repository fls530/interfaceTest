import os
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from Common.handle_path import REPORT_DIR


def send_smg():
    smtp = smtplib.SMTP_SSL(host="smtp.qq.com", port=465)
    # 登录smtp服务器（邮箱账号和授权码进行登录，注意点：不是邮箱的密码）
    smtp.login(user="530740300@qq.com", password="iykblaorhgqxcaba")

    # 第二步：构造一封多组件邮件
    msg = MIMEMultipart()
    msg["Subject"] = "测开平台接口自动化测试邮件"
    msg["To"] = "lemonban@qq.com"
    msg["From"] = "530740300@qq.com"

    # 构建邮件的文本内容
    text = MIMEText("邮件中的文本内容", _charset="utf8")
    msg.attach(text)

    # 构造邮件的附件
    with open(os.path.join(REPORT_DIR, "report.html"), "rb") as f:
        content = f.read()
    report = MIMEApplication(content)
    report.add_header('content-disposition', 'attachment', filename='python.html')
    msg.attach(report)

    # 第三步：发送邮件
    smtp.send_message(msg, from_addr="530740300@qq.com", to_addrs=["530740300@qq.com"])
