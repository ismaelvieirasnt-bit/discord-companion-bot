# Discord Companion Bot

Bot de IA para Discord pensado como um terceiro integrante de uma conversa entre Isma e Bia.

A proposta é combinar texto e voz em tempo real com memória de contexto e participação espontânea. O bot observa a conversa, decide quando contribuir e pode trazer perguntas, críticas, contradições e perspectivas novas, sabendo também quando permanecer em silêncio.

## Estado atual

A branch `feature/discord-companion` já contém o primeiro núcleo funcional:

- configuração por variáveis de ambiente;
- proteção contra publicação de segredos;
- personalidade do Companion;
- memória persistente básica;
- decisão separada entre falar e ficar em silêncio;
- integração textual com Discord;
- restrição opcional por IDs de usuário e canal;
- cooldown para reduzir interrupções.

## Estrutura

```text
Discord Companion Bot
├── main.py
├── requirements.txt
├── .env.example
├── SETUP.md
├── data/
└── bot/
    ├── __init__.py
    ├── config.py
    ├── companion.py
    ├── memory.py
    └── personality.py
```

## Conceito

```text
Discord
├── texto
└── voz
      ↓
conversação
      ↓
Isma + Bia + contexto
      ↓
memória
      ↓
modelo de IA
      ↓
responder / perguntar / criticar / silenciar
      ↓
texto / voz
```

## Configuração

Veja `SETUP.md` para configurar o Discord Developer Portal, as variáveis de ambiente e o primeiro teste local.

## Próximas etapas

1. Testar e ajustar a participação espontânea.
2. Melhorar memória de curto e longo prazo.
3. Adicionar comandos administrativos mínimos.
4. Integrar recepção de voz e segmentação de fala.
5. Adicionar speech-to-text e text-to-speech.
6. Criar testes de contexto, interrupção e naturalidade.
7. Preparar execução contínua em um servidor.
