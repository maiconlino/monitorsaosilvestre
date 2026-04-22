# 🏃 São Silvestre 2026 — Monitor de Inscrições

Monitora automaticamente o site da São Silvestre e envia um email quando
as inscrições abrirem. Roda 100% grátis no GitHub Actions.

---

## ⚡ Setup em 5 passos

### 1. Fork este repositório
Clique em **Fork** no canto superior direito do GitHub.

---

### 2. Gere sua Gmail App Password

> Você precisa de uma senha específica para apps — **não** a sua senha normal.

1. Acesse: https://myaccount.google.com/security
2. Ative a **Verificação em duas etapas** (se ainda não tiver)
3. Busque por **"Senhas de app"** na mesma página
4. Crie uma nova → selecione "Email" → copie a senha de 16 caracteres

---

### 3. Adicione os Secrets no GitHub

No seu fork, vá em:
**Settings → Secrets and variables → Actions → New repository secret**

Adicione os 3 secrets abaixo:

| Nome            | Valor                                      |
|-----------------|--------------------------------------------|
| `GMAIL_USER`    | seu email Gmail (ex: maicon@gmail.com)     |
| `GMAIL_PASS`    | a App Password de 16 dígitos               |
| `NOTIFY_EMAIL`  | email que vai receber os alertas           |

---

### 4. Ative o GitHub Actions

Vá em **Actions** no seu fork e clique em **"I understand my workflows, enable them"**.

---

### 5. Teste agora

Vá em **Actions → São Silvestre 2026 — Monitor → Run workflow**

Marque `send_heartbeat = true` e clique em **Run workflow**.

Você deve receber um email de confirmação em menos de 2 minutos.

---

## 📅 Frequência de monitoramento

| Período         | Frequência       | Lógica                              |
|-----------------|------------------|-------------------------------------|
| Janeiro–Setembro | 1x por dia (08h) | Inscrições historicamente não abrem |
| Outubro–Dezembro | A cada 5 minutos | Janela histórica das inscrições     |

> GitHub Actions tem mínimo de 5 minutos entre execuções (plano gratuito).
> É suficiente — as inscrições ficam abertas por horas, não segundos.

---

## 📬 Emails que você vai receber

- **🚨 INSCRIÇÕES ABERTAS** — quando detectar abertura (enviado 3x com 1 min de intervalo)
- **✅ Heartbeat semanal** — toda segunda-feira, confirmando que o monitor está vivo

---

## 🔍 Como o monitor detecta a abertura

O script busca palavras-chave no HTML da página:

**Abertura detectada por:**
- "inscreva-se", "inscrição aberta", "faça sua inscrição"
- "comprar ingresso", "garantir vaga", "registre-se"

**Confirmação de fechado:**
- "em breve", "aguarde", "inscrições encerradas"

---

## 🛠 Rodar localmente (opcional)

```bash
pip install -r requirements.txt

export GMAIL_USER="seu@gmail.com"
export GMAIL_PASS="abcd efgh ijkl mnop"
export NOTIFY_EMAIL="destino@email.com"
export SEND_HEARTBEAT="true"

python monitor.py
```

---

## ❓ Dúvidas frequentes

**O GitHub Actions para de rodar automaticamente?**
Sim, repositórios sem atividade por 60 dias têm os workflows pausados.
Para evitar: faça um commit qualquer ou use o botão "Run workflow" manualmente.

**E se o site mudar o layout?**
As keywords são robustas o suficiente para pegar qualquer variação comum.
Se quiser adicionar mais keywords, edite a lista `KEYWORDS_OPEN` em `monitor.py`.
