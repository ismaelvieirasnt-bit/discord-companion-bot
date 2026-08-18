# Discord Companion Bot

Bot de IA para Discord pensado como um terceiro integrante de uma conversa entre Isma e Bia.

A proposta é combinar texto e voz em tempo real com memória de contexto e participação espontânea. O bot não deve apenas responder a comandos: deve observar a conversa, decidir quando contribuir e trazer perguntas, críticas, contradições e perspectivas novas, sabendo também quando permanecer em silêncio.

## Princípios

- Participação natural, sem interromper por qualquer motivo.
- Respostas contextualizadas e humanas, sem fingir ser uma pessoa real.
- Capacidade de discordar com respeito.
- Perguntas que aprofundem a conversa em vez de apenas encerrá-la.
- Memória separada entre fatos e padrões/conceitos aprendidos na conversa.
- Isma e Bia são os únicos participantes autorizados na conversa privada do projeto.

## Estrutura planejada

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

## Próximas etapas

1. Núcleo de conversa e personalidade.
2. Identificação dos dois participantes.
3. Memória de curto e longo prazo.
4. Decisão de participação espontânea.
5. Integração com texto do Discord.
6. Entrada e saída de voz em tempo real.
7. Testes de contexto, interrupção e naturalidade.
