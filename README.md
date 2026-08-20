# Central de Estudos

Repositório para transformar vídeos do YouTube em material de estudo organizado: transcrição
completa, com timestamps, indexada e pesquisável.

## Guias

**📗 [GUIA-SAAS.md](GUIA-SAAS.md) — o tema principal.** Micro SaaS e produto com IA: como construir
sem programar, o método do clone, distribuição (a parte que os vídeos escondem), preço e churn, o
framework do Hormozi e a checagem cética dos números. Dos 18 vídeos do núcleo temático.

**📘 [GUIA.md](GUIA.md) — biblioteca complementar.** Low ticket e tráfego pago: método consolidado,
números de referência e divergências entre professores. São 131 vídeos herdados de um projeto
anterior — úteis porque ensinam a **adquirir** o cliente que o SaaS vai reter.

## Como usar

Manda os links do YouTube (aqui no chat com o Claude Code, ou adicionando direto em
[`references/youtube/urls.txt`](references/youtube/urls.txt)) e a skill `youtube-refs` cuida de:

1. Baixar a legenda/transcrição de cada vídeo (`yt-dlp`)
2. Transcrever localmente com Whisper os vídeos sem legenda
3. Salvar tudo em `references/youtube/{canal}/{título}.md`, com timestamps por trecho
4. Manter um índice (`references/youtube/index.json`) do que já foi processado

Depois é só perguntar - ex. "o que esse canal fala sobre X" - que a resposta vem citada com
`[timestamp]` e link do vídeo original.

Detalhes completos do pipeline: [`.claude/skills/youtube-refs/SKILL.md`](.claude/skills/youtube-refs/SKILL.md).

## Estrutura

```
references/youtube/
  urls.txt      # links brutos, um por linha
  index.json    # status de cada vídeo (pending / ok / no_subs / error)
  {canal}/{título}.md   # transcrição final
```
