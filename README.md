# Central de Estudos

Repositório para transformar vídeos do YouTube em material de estudo organizado: transcrição
completa, com timestamps, indexada e pesquisável.

## 📚 [GUIA.md](GUIA.md) — comece por aqui

Índice mestre dos 233 vídeos, organizado por grandes tópicos:

| Tópico | O que cobre |
|---|---|
| 🤖 [Agência de IA](guias/agencia-ia.md) | vender agentes e automação — o caminho mais rápido para caixa |
| 🛠️ [Ferramentas de IA na Prática](guias/ferramentas-de-ia.md) | como criadores realmente usam Claude, Claude Code e N8N |
| 💻 [SaaS e Produto Digital](guias/saas-produto.md) | construir e vender software com IA, sem programar |
| 🎯 [Low Ticket e Tráfego Pago](guias/low-ticket.md) | adquirir cliente pagando por ele |
| 🧠 [Negócio Solo e Mentalidade](guias/negocio-solo.md) | Hormozi, método CLOUD, sair do zero |
| ✍️ [Copy, Criativo e Conteúdo](guias/copy-e-criativo.md) | escrever o que vende, produzir o que segura o scroll |
| 📦 [E-commerce e Dropshipping](guias/ecommerce.md) | o experimento mais honesto da biblioteca |
| ⚠️ [Números e Ceticismo](guias/numeros-e-ceticismo.md) | auditoria de todos os resultados alegados |

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
