"""
São Silvestre 2026 — Monitor de Inscrições
Notifica por email quando as inscrições abrirem.
"""

import os
import smtplib
import requests
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# ── Configurações ──────────────────────────────────────────────────────────────
TARGET_URL = "https://www.saosilvestre.com.br"

# Palavras que indicam inscrição ABERTA
KEYWORDS_OPEN = [
    "inscrição aberta",
    "inscricao aberta",
    "inscrições abertas",
    "inscricoes abertas",
    "faça sua inscrição",
    "garanta sua vaga",
    "comprar ingresso",
    "inscreva-se agora",
    "vagas disponíveis",
]

# Palavras que confirmam que ainda está FECHADO
KEYWORDS_CLOSED = [
    "em breve",
    "aguarde",
    "inscrições encerradas",
    "em breve as inscrições",
    "fique atento",
    "lista de espera",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}

# ── Email ──────────────────────────────────────────────────────────────────────
GMAIL_USER   = os.environ["GMAIL_USER"]    # seu@gmail.com
GMAIL_PASS   = os.environ["GMAIL_PASS"]    # App Password do Gmail
NOTIFY_EMAIL = os.environ["NOTIFY_EMAIL"]  # destino da notificação


def send_email(subject: str, body_html: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_USER
    msg["To"]      = NOTIFY_EMAIL
    msg.attach(MIMEText(body_html, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())

    print(f"[{now()}] Email enviado para {NOTIFY_EMAIL}")


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_registration() -> dict:
    """
    Verifica o site e retorna:
      - status: 'OPEN' | 'CLOSED' | 'UNKNOWN'
      - evidence: trecho do texto que gerou a conclusão
      - page_title: título da página
    """
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[{now()}] Erro ao acessar o site: {exc}")
        return {"status": "ERROR", "evidence": str(exc), "page_title": "—"}

    soup      = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(separator=" ").lower()
    page_title = soup.title.string.strip() if soup.title else TARGET_URL

    # Procura evidência de inscrição aberta
    for kw in KEYWORDS_OPEN:
        if kw in page_text:
            idx   = page_text.find(kw)
            snip  = page_text[max(0, idx - 80): idx + 120].strip()
            return {"status": "OPEN", "evidence": snip, "page_title": page_title}

    # Procura evidência de inscrição fechada
    for kw in KEYWORDS_CLOSED:
        if kw in page_text:
            idx   = page_text.find(kw)
            snip  = page_text[max(0, idx - 80): idx + 120].strip()
            return {"status": "CLOSED", "evidence": snip, "page_title": page_title}

    return {"status": "UNKNOWN", "evidence": page_text[:300], "page_title": page_title}


def email_open(result: dict) -> None:
    subject = "🚨 SÃO SILVESTRE 2026 — INSCRIÇÕES ABERTAS!"
    body = f"""
    <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto;">
      <div style="background:#c0392b;padding:24px;border-radius:8px 8px 0 0;text-align:center;">
        <h1 style="color:#fff;margin:0;font-size:28px;">🏃 São Silvestre 2026</h1>
        <p style="color:#ffd6d6;margin:8px 0 0;">INSCRIÇÕES ABERTAS AGORA</p>
      </div>
      <div style="background:#fff;border:1px solid #ddd;padding:24px;border-radius:0 0 8px 8px;">
        <p style="font-size:18px;color:#222;">
          Maicon, <strong>as inscrições da São Silvestre 2026 estão abertas!</strong>
        </p>
        <p>Detectado em: <strong>{now()}</strong></p>
        <p>Título da página: <em>{result["page_title"]}</em></p>
        <p>Trecho detectado:</p>
        <blockquote style="background:#fff8f8;border-left:4px solid #c0392b;padding:12px;
                           font-size:13px;color:#555;">
          {result["evidence"]}
        </blockquote>
        <div style="text-align:center;margin:28px 0;">
          <a href="{TARGET_URL}" 
             style="background:#c0392b;color:#fff;padding:14px 32px;border-radius:6px;
                    font-size:18px;font-weight:bold;text-decoration:none;">
            👉 INSCREVA-SE AGORA
          </a>
        </div>
        <p style="font-size:12px;color:#999;">
          Monitoramento automático — São Silvestre Monitor 2026
        </p>
      </div>
    </body></html>
    """
    send_email(subject, body)


def email_heartbeat(result: dict) -> None:
    """Envia relatório diário de que o monitor está rodando."""
    subject = f"✅ São Silvestre Monitor — Checagem {now()}"
    body = f"""
    <html><body style="font-family:Arial,sans-serif;max-width:500px;margin:auto;">
      <div style="background:#2c3e50;padding:20px;border-radius:8px 8px 0 0;">
        <h2 style="color:#fff;margin:0;">São Silvestre Monitor</h2>
        <p style="color:#bdc3c7;margin:4px 0 0;">Relatório diário</p>
      </div>
      <div style="background:#fff;border:1px solid #ddd;padding:20px;border-radius:0 0 8px 8px;">
        <p>✅ O monitor está <strong>ativo e funcionando</strong>.</p>
        <p>📅 Última verificação: <strong>{now()}</strong></p>
        <p>📊 Status detectado: <strong>{result["status"]}</strong></p>
        <p>🌐 Página: <em>{result["page_title"]}</em></p>
        <p style="font-size:12px;color:#999;">Inscrições ainda não abertas. Você será notificado imediatamente quando abrirem.</p>
      </div>
    </body></html>
    """
    send_email(subject, body)


def main():
    print(f"[{now()}] Iniciando verificação — {TARGET_URL}")

    result = check_registration()
    print(f"[{now()}] Status: {result['status']} | Evidência: {result['evidence'][:80]}")

    if result["status"] == "OPEN":
        email_open(result)
        # Envia 3x com 1 min de intervalo para garantir que chega
        import time
        for i in range(2):
            time.sleep(60)
            email_open(result)
            print(f"[{now()}] Notificação {i+2}/3 enviada")
    else:
        # Heartbeat diário — GitHub Actions roda 1x/dia normalmente
        # O workflow só envia heartbeat quando a variável SEND_HEARTBEAT=true
        if os.environ.get("SEND_HEARTBEAT", "false").lower() == "true":
            email_heartbeat(result)

    print(f"[{now()}] Verificação concluída.")


if __name__ == "__main__":
    main()
