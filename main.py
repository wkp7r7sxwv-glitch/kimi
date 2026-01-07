import os, requests, smtplib, ssl
from email.mime.text import MIMEText
from datetime import datetime

# ---------- 1. 让 Kimi 总结热点 ----------
def kimi_summary() -> str:
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('KIMI_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system", "content": "你是专业财经科技新闻助理，输出纯中文摘要，不带多余符号。"},
            {"role": "user", "content":
             "请总结昨日与今日投资、金融、科技三大板块的热点新闻，每条 20 字以内，按时间倒序，共 10 条。"}
        ],
        "temperature": 0.3
    }
    r = requests.post(url, json=payload, timeout=60, headers=headers)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# ---------- 2. 发邮件 ----------
def send_mail(body: str):
    user = os.getenv("EMAIL_USER")
    pwd  = os.getenv("EMAIL_PASS")
    to   = os.getenv("EMAIL_TO")
    msg  = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"{datetime.now():%m-%d} 热点简报"
    msg["From"] = user
    msg["To"] = to
    with smtplib.SMTP_SSL("smtp.qq.com", 465,
                          context=ssl.create_default_context()) as s:
        s.login(user, pwd)
        s.sendmail(user, to.split(","), msg.as_string())

if __name__ == "__main__":
    send_mail(kimi_summary())
