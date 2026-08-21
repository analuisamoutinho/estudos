# Ferramentas de IA na Prática

Como criadores estão realmente usando Claude, Claude Code, Gemini Omni e N8N — não a promessa de
marketing, o fluxo de trabalho real, com bug, retrabalho e custo. Este guia é transversal: alimenta
diretamente o "cavalo de troia" da Agência de IA, o pipeline de produto do Low Ticket e a produção de
criativos do Copy e Criativo.

**Fontes:** Descomplicando Sites · Klebson Queiroz · Tiago Lemos · Invente com IA · Matheus Santos (2) ·
MGTInc · Preguiça Artificial · Gabriel Adamuchi · Ratos de IA (2) · Mateus Dias · Sancler Miranda ·
Rafa Voss · Pedro Sobral · Victor Baggio · Karine Lago · Renato Asse (Open Squad) · Codecon · Oliur Online

---

## Parte 1 — Landing pages com Claude Design: o pipeline que 3 criadores ensinam igual

Três canais sem relação entre si (Descomplicando Sites, Klebson Queiroz, Tiago Lemos), filmando dias
depois do lançamento do Claude Design, convergem no **mesmo processo** — o sinal de reprodutibilidade
mais forte deste guia inteiro:

1. **Copy antes de qualquer design.** Nunca peça a página direto — gere a copy primeiro, numa skill
   dedicada de copywriting ou num agente separado que entrevista você (produto, público, objeção,
   diferencial, tom) e devolve um prompt estruturado seção por seção.
2. **Referência visual, não descrição.** Cole um print de uma página que você gosta (extensão **GoFullPage
   Screen Capture**) ou um snippet de componente do **21st.dev** — "use como inspiração, não faça igual".
3. **Gere no Claude Design**, respondendo às perguntas de direção (cor, tom, hero, urgência) — "decida
   por mim" acelera.
4. **O editor visual do Claude Design é bom só para ajuste pequeno.** Os três criadores relatam bug e
   lentidão no editor in-canvas recém-lançado; preferem iterar pelo chat para mudanças grandes.
5. **Exporte HTML e hospede fora.** Claude Design não publica sozinho — todos usam hospedagem
   tradicional (Hostinger, HostGator) ou Claude Code fazendo deploy via CLI na Vercel.

**Regras que fazem a diferença (citadas por mais de um vídeo):**
- Nunca botão de compra/menu de navegação na primeira dobra — distrai da conversão.
- Peça explicitamente **"adicionar gráficos e ilustrações"** — muda a página de "bloco de texto" para
  visual dinâmico.
- Nomeie arquivos de imagem localmente igual ao que o prompt referencia — o Claude troca sozinho.
- `index.html` sem sufixo numérico, numa pasta própria por página — convenção de servidor.

### Referência de custo/hospedagem

| Serviço | Preço | Fonte |
|---|---|---|
| Hostinger (hospedagem + domínio) | ~R$161/ano com cupom | Descomplicando Sites |
| HostGator Plano M (60 sites) | ~R$11/mês, plano 3 anos | Tiago Lemos |
| Verificação de performance | GTmetrix — 98% performance, 100% estrutura, um exemplo real | Tiago Lemos |

---

## Parte 2 — Vídeo sem editor: Claude Code + Gemini Omni/Krea

Três criadores (MGTInc, Gabriel Adamuchi, Ratos de IA) chegaram, de forma independente, ao mesmo
padrão: Claude Code lê o vídeo bruto, transcreve (família Whisper), gera prompt de cena por take, e
entrega a um hub de geração (Google Flow/Gemini Omni ou Krea MCP) para B-roll e efeitos — sem editor
humano.

**Passo a passo consolidado:**
1. Documente a identidade visual num `design.md` (paleta, tipografia, layout) — sem isso a IA "não
   consegue seguir de forma ideal" [MGTInc].
2. Corte o bruto em takes de ~10s (exigência do modelo de vídeo), com contexto de cada um (quem
   aparece, cenário, roupa/marca).
3. Gere prompt por take, envie ao Flow/Krea, itere pedindo mais elementos ou trocando cenário.
4. Sincronize áudio manualmente no CapCut — o áudio gerado pelo modelo de vídeo costuma sair com bug.
5. Depois de estabilizar, **transforme em skill reutilizável** — é o padrão que se repete em quase todo
   vídeo de skill deste guia: prompt bem ajustado → skill salva → nunca mais reexplicar.

**Custo real:** R$29-99/segundo de motion design tradicional vs. **~R$12/minuto** com o pipeline via
skill (MGTInc, "290x mais barato" — claim do próprio criador, não auditado externamente). Edição de
~30s levou 25-30 minutos [Gabriel Adamuchi]. Editor humano tradicional: 3-9 mil reais, 3-7 dias.

**Regra de ouro repetida em geração de imagem/vídeo:** nunca gere vídeo direto de um prompt cru —
gere **imagens de referência primeiro** (personagem, cenário) e alimente essas imagens ao modelo de
vídeo. Prompt puro sai visivelmente pior [Preguiça Artificial, Matheus Santos].

**Criar vídeo com pessoa pública/clonagem de voz:** requer MP3 da voz-alvo separado; funciona, mas é
zona cinzenta de imagem/consentimento não discutida nos vídeos — ver aviso de ética em
[copy-e-criativo.md](copy-e-criativo.md).

---

## Parte 3 — Skills: o mecanismo que se repete em todo o lote

**A ideia central, dita de formas diferentes por 7 vídeos:** transforme um prompt bem ajustado numa
**skill salva** (pasta com `skill.md` + scripts opcionais) em vez de reexplicar toda sessão. Skill
funciona em qualquer IA que suporte o formato — diferente de GPT customizado, que fica preso ao
ecossistema de origem [Sancler Miranda].

**Anatomia:** `skill.md` (nome, descrição, instruções — "um prompt maior") + `scripts/` + `reference/`
opcionais. Criadas pelo fluxo de chat ("criar com Claude") sincronizam entre dispositivos; pastas
arrastadas manualmente **não sincronizam** — detalhe que surpreende quem espera disponibilidade global.

**Claude agora se autotesta** contra exemplo antes de finalizar uma skill nova — pega e corrige o
próprio bug antes de entregar [Sancler Miranda].

**Skills podem chamar ferramenta externa** (ex.: Nano Banana dentro de uma skill de infográfico) e
combinar com **agendamento nativo** — `/schedule` uma skill para rodar toda sexta às 18h.

### Open Squad — esquadrões de agentes, não um agente só

Framework open-source (Renato Asse) para não-programadores montarem **times** de agentes
especializados (pesquisador → redator → designer → revisor → publicador) em vez de um agente que
faz tudo mal. Instala com `npx open squad init` em cima de Claude Code/Antigravity/Cursor/Codex.

No primeiro uso, pesquisa sozinho o site da sua empresa para pré-popular tom de voz/produto/público.
Criação de esquadrão é conversacional; um agente arquiteto nomeia os agentes com iniciais
combinando (padrão "Marvel": "Carlos Carrossel", "Diana Design"). Grava aprendizado entre execuções
num arquivo de memória persistente ("prefiro versão direta e chocante") que melhora runs futuros sem
reensinar.

> ⚠️ **Aviso de custo:** esquadrões consomem muito mais token que um prompt único — tanto na criação
> quanto na execução. Recomendação do próprio criador: usar modelo mais barato (Haiku/Sonnet, não
> Opus) e plano de assinatura maior para uso pesado.

---

## Parte 4 — MCP: dar "mãos" ao Claude

Padrão mecânico repetido em 5 vídeos: achar ou instalar um servidor MCP para a ferramenta-alvo, colar
URL/token nas configurações de conector do Claude, e o Claude ganha acesso de leitura/escrita naquela
ferramenta.

| Conector | O que faz | Custo/nota |
|---|---|---|
| **Apify** (leads) | scraping de perfis/leads qualificados por prompt em linguagem natural | ~100 leads por $0,28 no free tier (estimativa do próprio criador) |
| **Firecrawl** | navegador dedicado e isolado com login persistente — não expõe suas sessões normais | mais barato em crédito que a ferramenta nativa de "usar navegador" do Claude, que tira screenshot repetido |
| **Conta Azul** (comunidade, não oficial) | 32 ações de leitura + 23 de escrita | achado via mcpservers.org quando não existe conector oficial |
| **Meta Ads / Google Ads** | ver [agencia-ia.md](agencia-ia.md) Parte 5.5 | |

**Aviso ético repetido em mais de um vídeo:** dado de scraping não vira lista de spam — usar só em
canal comercial (WhatsApp Business, e-mail), nunca WhatsApp pessoal do lead [Matheus Santos].

**Servidores MCP não oficiais existem para o que falta.** Quando a Anthropic não tem conector
pronto para uma ferramenta brasileira, buscar "servidor MCP [nome]" ou usar mcpservers.org resolve —
demonstrado ao vivo com Conta Azul.

---

## Parte 5 — Claude Code: o que sustenta todo o resto

Curso completo de Mateus Dias é a referência mais densa do lote — os conceitos abaixo aparecem
implícitos, sem explicação, em quase todo outro vídeo de Claude Code deste guia:

- **`CLAUDE.md`** — "um contrato de trabalho": regras, convenções, contexto, limites de segurança.
  Persiste entre sessões (diferente do contexto solto, que reseta). `/init` gera automaticamente a
  partir da pasta do projeto.
- **`/clear` e `/compact`** — limpar contexto acima de ~50-60% de uso (hábito pessoal do autor: limpar
  a partir de 160k tokens mesmo com contexto de 1M disponível). *"Contexto cheio é igual mesa de
  trabalho cheia — piora o resultado."*
- **Subagentes são "mais burrinhos"** — delegar por camada (orquestrador forte → workers médios →
  tarefa simples no modelo mais barato), nunca confiar decisão complexa a um subagente.
- **Plan Mode** para tarefa de peso arquitetural; **"ultra think"** só para decisão de alto risco —
  queima token/tempo desnecessário em tarefa trivial.
- **7 rituais recomendados:** sempre começar em Plan Mode · manter CLAUDE.md atualizado · limpar
  contexto por tarefa nova · sempre revisar output · verificar por ferramenta externa/navegador · usar
  subagentes para trabalho paralelo · versionar em Git.
- **Nunca deixar decisão crítica sem supervisão** (financeiro, contratar/demitir) e **nunca colar
  senha/API key no terminal de chat**.

**Comparativo de custo real:** plano de $200/mês do Claude Code cobriria, via API pura, algo próximo
de $3.000/mês de uso equivalente segundo o criador — a assinatura sai "menos de um décimo" do custo
por token avulso.

### O contraponto cético do lote: sêniors vs. júniors com IA (Codecon)

Único vídeo do lote com comparação controlada, não case de sucesso do próprio criador: 3 sêniors
(sem IA) contra 3 júniors (com IA) construindo o mesmo dashboard em 3 horas.

**Resultado:** IA não tornou os júniors dramaticamente mais rápidos — o gargalo foi **saber perguntar**,
não capacidade do modelo (os próprios participantes admitem baixo uso diário de IA antes do desafio).
Código gerado por IA tinha função duplicada quase idêntica e endpoint morto não utilizado — sinal de
output não revisado indo para produção. Os sêniors, sem IA, entregaram via low-code (Metabase +
MongoDB) mais rápido que os júniors sobre-engenheiraram com stack customizada.

> Contrapeso necessário ao tom geral triunfante do resto deste guia: IA fecha parte da distância de
> experiência, não elimina o valor de julgamento de engenharia.

### O outro contraponto: plugin oficial da Anthropic também precisa de adaptação

O plugin "Claude for Small Business" (Anthropic) vem com 31 skills e conectores centrados em
ferramentas americanas (QuickBooks, PayPal, HubSpot) — inútil de cara para pequeno negócio brasileiro
[Victor Baggio]. Adaptação real: trocar HubSpot→CRM local, PayPal→processador local, QuickBooks→
**Conta Azul**, Slack→**WhatsApp**. No teste do autor, **23 das 31 skills precisaram ser reescritas e
8 removidas**. *"Automação exige reiteração, exige trabalho"* — não é plug-and-play, mesmo vindo
oficial da própria Anthropic.

---

## Parte 6 — N8N: a camada de automação complementar (não Claude-específica)

N8N não é ferramenta da Anthropic — é a camada de orquestração que conecta apps por gatilho→ação, com
ou sem IA no meio [Karine Lago]. Diferença chave para quem só usou o Claude/ChatGPT de consumidor: o
**nó de IA dentro do N8N não tem memória nem acesso web por padrão** — precisa adicionar nó de memória
separado, ou o agente "esquece" o que foi dito na mesma conversa.

**Custo de hospedagem:** N8N Cloud oficial ~R$150/mês; alternativa mais barata é VPS com N8N
auto-hospedado (Hostinger tem opção de 1 clique).

---

## Parte 7 — Fora do mecânico: IA como parceiro de pensar, não substituto

Contraponto explícito ao tom "automatize tudo" do resto do guia [Pedro Sobral]: o maior valor não é
automação de tarefa, é apoio à decisão — dite ideias soltas por voz (Whisper/ditado nativo) em vez de
prompt engenheirado, peça prós/contras de uma decisão real, peça para separar "o que é real" de "o que
é ansiedade" numa preocupação.

> *"Eu não uso IA para ela pensar por mim. Uso para me ajudar a pensar melhor."*

Risco nomeado explicitamente: terceirizar o pensamento e virar "o segundo cérebro da IA", em vez do
contrário — se não usar o próprio raciocínio, ele atrofia.

---

## O que levar daqui

1. **Landing page:** copy separada → referência visual → Claude Design → export HTML → hospedagem
   tradicional. Nunca confie no editor visual do Claude Design para mudança grande — ainda é instável.
2. **Vídeo sem editor:** imagem de referência antes de vídeo, sempre. Documente identidade visual num
   `design.md`. Vire skill assim que o fluxo estabilizar.
3. **Toda ferramenta que você refaz mais de uma vez vira skill.** É o padrão mais repetido do lote
   inteiro — e o que sobrevive a troca de modelo (o próprio Boris Cherny, criador do Claude Code,
   reforça isso).
4. **MCP = mãos.** Servidor comunitário (mcpservers.org) resolve quando não existe conector oficial
   para ferramenta brasileira.
5. **Não acredite que "conectou = funciona".** Plugin oficial da Anthropic para pequeno negócio
   precisou de 74% de reescrita para servir o mercado brasileiro. Adapte sempre.
6. **IA não substitui julgamento técnico** — o contraste sênior/júnior mostra isso melhor que qualquer
   outro vídeo da biblioteca.

---

*Extraído da leitura integral das transcrições em `references/youtube/`. Cada afirmação é rastreável
ao vídeo e timestamp. Legendas automáticas — nomes de ferramentas e números podem conter erros.*
