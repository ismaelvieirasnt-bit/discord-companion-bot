# Configuração do Discord Companion

## 1. Criar o bot no Discord

Abra o Discord Developer Portal e crie uma Application. Na aplicação, abra **Bot** e crie o usuário do bot.

Ative o **Message Content Intent**, porque o núcleo textual precisa ler o conteúdo das mensagens.

Na instalação do aplicativo, dê ao bot, no mínimo, estas permissões no servidor:

- View Channels
- Send Messages
- Read Message History
- Connect
- Speak

Para o primeiro teste, deixe o bot restrito a um canal privado.

## 2. Guardar as credenciais

Na raiz do projeto, crie um arquivo chamado `.env` baseado em `.env.example`.

Preencha:

```env
DISCORD_TOKEN=seu_token_do_bot
OPENAI_API_KEY=sua_chave_da_api
OPENAI_MODEL=gpt-5.6
```

Nunca publique o `.env` no GitHub.

## 3. Restringir a conversa a Isma e Bia

No Discord, copie o ID de usuário de Isma e de Bia com o Developer Mode ativado e coloque os dois IDs separados por vírgula:

```env
ALLOWED_USER_IDS=111111111111111111,222222222222222222
```

Também podemos restringir a um canal específico:

```env
ALLOWED_CHANNEL_ID=333333333333333333
```

## 4. Instalar e executar

Recomendado: Python 3.12 ou superior.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## 5. Teste inicial

Quando o bot estiver online, use:

```text
!status
```

Depois converse normalmente. O Companion decide quando participar e tem um cooldown para evitar interrupções.

## 6. Voz

A base textual está separada da camada de voz. O `discord.py` fornece conexão e reprodução de áudio, mas recepção de áudio de usuários precisa de uma extensão de voice receive. A próxima etapa do projeto usará uma camada compatível com o ecossistema atual de Discord e com o tratamento de áudio recebido.

A camada de voz deverá seguir este fluxo:

```text
Discord Voice
    ↓
áudio do Isma/Bia
    ↓
recepção + segmentação
    ↓
speech-to-text
    ↓
Companion
    ↓
text-to-speech
    ↓
audio de volta ao Discord
```

Não coloque tokens ou chaves de API em arquivos versionados.
