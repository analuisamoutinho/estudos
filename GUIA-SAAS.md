# Guia — Micro SaaS e Produto com IA

Síntese dos **18 vídeos** que formam o núcleo temático desta central de estudos: construir e vender
software/app com IA, sem programar.

**Canais:** Starter Story (3) · Cakto (2) · Caio Martins (2) · Thiago Boeira (2) · Alex Hormozi ·
Jaxon Poulton · João Mussoi · Bruno Gabarra · Eli Rigobeli · Kevin Rodrigues · Matheus PH ·
Junior Moreira · Rafa Voss

> Para o material de low ticket e tráfego pago (131 vídeos herdados do projeto anterior), veja
> [GUIA.md](GUIA.md). Ele é complementar: ensina a **adquirir** o cliente que o SaaS vai reter.

---

## A tese central

Todos esses vídeos existem por causa de um problema só: **o low ticket para de faturar no dia em que
você desliga o anúncio.** SaaS resolve isso trocando pico por recorrência.

| Modelo | Receita | Vantagem real | Custo real |
|---|---|---|---|
| Low ticket (R$5-67, pago uma vez) | pico, morre sem tráfego | valida rápido, dinheiro na hora | tráfego constante e caro |
| **SaaS assinatura (MRR)** | recorrente e composta | escala sem campanha nova toda semana | demora muito a decolar |
| Lifetime deal (LTD) | pico único grande | caixa imediato, "converte suposição em dinheiro" | mata a recorrência futura |
| Serviço de IA p/ empresas | recorrente, R$500-6.000/cliente | margem alta, zero produto | não escala sozinho |

**O melhor arranjo do corpus inteiro** é do Nícolas Moreira (que está na outra biblioteca): usar o
micro SaaS de **$7,90/mês como upsell** de um PDF low ticket de $9,90. O low ticket paga a aquisição,
o SaaS gera a recorrência. Nenhum dos 18 vídeos de SaaS resolve aquisição tão bem quanto isso.

---

## Parte 1 — Construir sem programar

Padrão repetido em todos: **prompt estruturado → ferramenta de vibe coding → deploy → checkout**.

### Stack

| Camada | Ferramenta | Nota |
|---|---|---|
| Build | **Lovable** (mais citado nos canais BR) ou **Claude Code** | Jaxon construiu o app inteiro no Claude Code depois de fracassar copiando código do ChatGPT pro Xcode |
| Build grátis | **OLAMA** local com GLM 4.6 | alternativa do Caio Martins ao Claude Code pago |
| Protótipo | **Google AI Studio** (aba Build) + Nano Banana | ⚠️ sem banco de dados e sem pagamento — só teste |
| Deploy | **Netlify** / **Vercel** | arrastar pasta → domínio grátis |
| Checkout | **Cakto** / Kiwify / **Stripe** | Cakto faz assinatura recorrente com Pix automático |
| Alternativas | V0, Base44, Hostinger Horizons | citadas de passagem |

### O caminho mais curto (Caio Martins)

1. Instalar o app desktop (Claude Code ou OLAMA), configurar o modelo
2. Prompt curto descrevendo o produto: *"Quero criar um microSaaS chamado Lilo, um assistente financeiro inteligente"*
3. Pegar o `index.html` gerado, salvar, abrir local pra conferir
4. Arrastar a pasta pro Netlify → deploy automático
5. Cadastrar na Cakto como **assinatura recorrente**, definir preço (R$9,90/mês), colar o link, publicar

### Liberar acesso automaticamente

O método do Nícolas (Replit + Hotmart), que é o mais limpo:
webhook da plataforma → `https://[dominio]/api/webhook/hotmart` → **login só pelo e-mail da compra**
(sem senha, sem CPF) → cancelamento/reembolso revoga o acesso sozinho pelo evento do webhook.

### Técnica de prompt: Role Based Prompt (Matheus PH)

Estruturar em XML com tags `<cargo>`, `<instruções>`, `<regras>`. Ele inclui uma cláusula fictícia de
recompensa/punição para forçar aderência do modelo — funciona, mas é o vídeo mais inflado do lote
(ver Parte 5).

### O contraponto que você precisa ouvir

O fundador do DataCrazy (R$1,59M de MRR, 2.822 clientes pagantes, 64 funcionários) chama vibe coding
de **cassino**:

> *"O cara que tá ali no cassino do Claude Code gastando crédito — quem tá ganhando é o Claude."*
> *"Software não é sobre o código. É sobre as pessoas, é pôr no mercado, fazer todo mundo usar."*

Ele diz ter torrado R$1.000 em algumas horas sem construir nada de valor. **Construir virou a parte
fácil e barata. O negócio inteiro está na Parte 3.**

---

## Parte 2 — O método do clone (Starter Story)

Samuel Rondo faz $35K/mês e **não inventa produto nenhum**. Ele copia o que já funciona.

### Os 4 filtros de validação

1. **Eu mesmo usaria** o produto
2. **Já tem tração comprovada** — não é aposta
3. **O concorrente NÃO gasta muito em tráfego pago** → prova que existe demanda orgânica real, não é
   um produto sustentado artificialmente por anúncio
4. **É simples o bastante** para eu manter sozinho

O filtro 3 é o mais inteligente e o menos óbvio. Inverte a lógica de quem minera oferta em
biblioteca de anúncios: aqui, muito anúncio é sinal **ruim**.

### Como verificar na prática

- **Prova de que paga:** procure fundadores publicando print de MRR/Stripe no Twitter (comunidades
  "build in public"/solopreneur). *"É a prova definitiva de que a ferramenta funciona e que as
  pessoas estão pagando."*
- **Origem do tráfego:** cheque o concorrente no **Ahrefs**. Se vem de ads → replicável rápido
  (basta ligar o anúncio). Se vem de SEO → lento, mas muito mais defensável.

**Caso real:** viu um concorrente automatizando vídeos faceless, confirmou no Ahrefs que 100% do
tráfego era Facebook Ads, construiu o clone (Story Short) em ~1 semana e replicou o crescimento.

### Sobre ética

Nenhum dos vídeos discute propriedade intelectual, marca ou plágio — tratam só como posicionamento
de mercado. O enquadramento deles é "modelar, não copiar": mesma categoria de produto, diferencial
próprio. Copiar código, nome, marca ou conteúdo é outra coisa e tem risco jurídico real.

---

## Parte 3 — Distribuição: o negócio inteiro

**Esta é a parte que os vídeos técnicos escondem e os cases reais revelam.** Matheus PH e Rafa Voss
não tocam no assunto. Construir o app é a parte fácil.

### ⚠️ O dado mais importante dos 18 vídeos

**Angus Chang faz $40K/mês com margem de 97,5%.** O que ele testou:

| Canal | Investimento | Resultado |
|---|---|---|
| Google Search Ads | 6 meses | **nunca foi lucrativo** — gastava $1.000, vendia $300 |
| Cold email | 3 meses | **1 venda** |
| Blog / Twitter | contínuo | efeito real quase nulo |
| **SEO passivo** | — | ao cortar os ads, seguia recebendo **2-3 cadastros orgânicos/dia** |

Ele cresceu consertando o produto via feedback de cliente e deixando o SEO compor. Evolução:
$6K → $14K → $27K → $40K/mês.

> *"Ignorem redes sociais. Acho que é perda de tempo. Só foquem no negócio, foquem no produto."*

Isso contradiz frontalmente o instinto de quem vem de low ticket (subir campanha). **Para SaaS, o
tráfego pago valida rápido mas raramente sustenta** — a economia é diferente porque você paga a
aquisição uma vez e recebe por meses.

### Os padrões que funcionaram

**Padrão americano — ads para validar, SEO para escalar** (stack de 4 passos do Samuel Rondo):
1. Sempre começa com ads (Google/Meta) para validar rápido
2. Com tração, entra SEO — *"quase grátis e composto"*
3. Canais faceless automatizados (YouTube/TikTok/Instagram) publicando UGC diário
4. Programa de afiliados — CPA fixo + viralidade, porque afiliado faz vídeo/artigo de graça

**Padrão brasileiro — orgânico + retargeting em cascata** (Junior Moreira, 575 assinantes / R$50K MRR):
1. Publica Reels normalmente
2. Impulsiona **só os que já performaram organicamente** (850K e 417K views)
3. Roda anúncio **exclusivamente para quem assistiu esses vídeos** — público pré-qualificado
4. YouTube Shorts (20-43K views) mandam lead direto pro WhatsApp, organizados em Kanban

**Viralização (Jaxon Poulton, $6K/mês):** tentou TikToks próprios sem sucesso e quase desistiu. Fez
um vídeo com personagem gerado por IA (não ele) que estourou: 30M views no Reels, 6-8M no TikTok,
custo ~$0,25 e 10 minutos. A descoberta que vale:

> **Pessoas compram por aspiração, não por prevenção** — venda "sua vida vai ficar assim", não "você vai evitar isso".

⚠️ Mas viralizar não se repete sob demanda. Ele é honesto sobre isso; o título do vídeo não é.

**Lançamento com lista (Umberto, $117K num dia):** ~1 mês de sequência de e-mails com storytelling
gradual, **nunca revelando o preço** antes do dia. Depois LTD com 3 tiers ($109 / $199 / $349 — os
dois baratos ancoram o caro) e vagas limitadas por 5-7 dias. Comunidade no Telegram com os primeiros
compradores. ⚠️ Ele já tinha marca física e lista construída desde 2020.

**Conteúdo faceless com IA (Cakto):** copiar um rosto do Instagram → pedir ao Gemini "outra pessoa"
(nunca o rosto real) → roteiro de notícia viral via Perplexity → narração Eleven Labs → CapCut com
legenda dinâmica → CTA pedindo comentário ("comenta skill") → link no direct. Captura por
engajamento, não link na bio.

---

## Parte 4 — Preço e monetização

| Faixa | Valor | Quem |
|---|---|---|
| Low ticket BR | R$5 - R$67 | Caio Martins define essa faixa |
| MicroSaaS simples | R$9,90 - R$19,90/mês | Caio Martins |
| SaaS de nicho | R$49 - R$50/mês | Eli Rigobeli (hipotético) |
| Serviço de IA B2B | R$1.000 - R$6.000/mês por cliente | Bruno Gabarra, João Mussoi |
| LTD | $109 / $199 / $349 | Umberto (Flogga) |
| Comissão de afiliado | 50-70% | Caio Martins, para influenciador <50k seguidores |

**Trial:** Lovable dá 5 mensagens/dia grátis. Centralizze (Junior Moreira) tem trial de 3 dias.

⚠️ **Churn é o buraco do corpus.** Nenhum dos 18 vídeos dá uma taxa numérica real. Caio Martins
reconhece genericamente ("tem a base de churn, as pessoas que desistem") e para aí. Junior Moreira
fala de retenção qualitativamente (lembrete de ativação 29 dias após assinar) sem número.

Para referência, os únicos dados de retenção do corpus vêm do Nícolas (outra biblioteca): **LTV de
~2,2 meses, retenção 61%, 78 pagantes ativos de 124 assinaturas totais** — ou seja, 46 cancelaram.
Se essa for a ordem de grandeza, é o número que decide se o negócio fecha.

---

## Parte 5 — Números: o que se sustenta e o que não

Checagem título contra o que é dito no corpo do vídeo.

### ✅ Bem documentados (histórico coerente, tela ao vivo)

| Case | Número | Verificação |
|---|---|---|
| **Angus Chang** — "$40K/month with this one website" | $40K/mês | histórico ano a ano coerente ($6K→$14K→$27K→$40K), margem 97,5% declarada. **O melhor dado do lote** |
| **DataCrazy** (Cakto) — "SaaS Milionário" | R$1,59M MRR | 2.822 clientes, R$8M no ano, 16 meses, 64 funcionários, tela mostrada |
| **Samuel Rondo** — "$35K/month" | $35K | soma de 3 produtos ($15K + $20K + $0,9K). Correto, mas o título esconde que são portes desiguais |
| **Bruno Gabarra** — "R$330/dia" | R$330/dia | matemática explícita e correta (2 clientes × R$5.000 ÷ 30). Mas é **projeção de precificação**, não case realizado |

### ⚠️ Enganosos por omissão

| Case | Problema |
|---|---|
| **Starter Story** — "$120K em 24 horas" | corpo diz $117K e é **pico único de LTD**. O MRR recorrente é $9-10K/mês — **12× menor**. Tecnicamente verdade, praticamente enganoso |
| **Jaxon Poulton** — "$6.000/mês" | é **projeção**: "$200/dia, então até este vídeo sair vou estar em $6K". Não fechado no momento |
| **Kevin Rodrigues** — "R$300 em 1 dia (do zero)" | valor real, mas "do zero" é falso: já tinha Instagram ativo, prompt validado e Photoshop |
| **Thiago Boeira** — "11 minutos, já validado" | a validação citada (265 vendas) é de **outro produto**, não do app construído no vídeo |
| **Cakto** — "vendi em 20min" | mostra conta com histórico de R$172.000, mas **não mostra a venda do produto criado ao vivo** |

### 🚨 Sem lastro

| Case | Título | Corpo |
|---|---|---|
| **Matheus PH** | "R$49K por mês no automático" | **zero menção a receita, preço ou venda**. É só tutorial de prompt. O mais flagrante do lote |
| **Thiago Boeira** | "Fiz R$382 mil em 30 dias" | **~R$78.000** ("2 a 5 mil/dia × 30"). Discrepância de ~5× |

### O conflito de interesse

Junior Moreira, Thiago Boeira, Caio Martins, Matheus PH e Rafa Voss são, no fundo, **funis para
vender curso/mentoria/comunidade própria**. O case é a isca. Dois participantes dizem isso na cara:

> *"É muito mais fácil vender um curso pra você criar SaaS do que você fazer dinheiro com isso."* — Eli Rigobeli
> *"E não, eu não fiz R$77.979,90 no último mês com esse SaaS. Pelo menos não da forma como alguns têm ensinado aqui no YouTube."* — Eli Rigobeli

---

## Parte 6 — Alex Hormozi: os primeiros R$100 mil

O vídeo mais conceitual e provavelmente o mais valioso dos 18. Não é sobre SaaS — é sobre sair do zero.

**O enquadramento:** o momento em que ele se sentiu mais rico não foram os $42 milhões em
distribuições, nem a saída de $46,2 milhões, nem os $106 milhões num fim de semana. Foi **juntar os
primeiros $100 mil**, porque acabou com a ansiedade de pagar o aluguel do mês seguinte.

### Os 6 passos

1. **Cortar todos os custos** — não comer fora, não comprar roupa, morar o mais barato possível (ele
   dividia quarto por $300-400/mês). Objetivo: gerar folga de caixa para reinvestir
2. **Poupar tempo** — as 4h antes e as 4h depois do trabalho. Fórmula **4-4-4**: 4h promovendo, 4h
   entregando, 4h construindo. Separe modo *maker* (agenda vazia = produtivo) de modo *manager*
   (blocos cheios = produtivo) e nunca misture no mesmo bloco — *"trocar de tarefa é o maior assassino da produtividade"*
3. **Escolher uma habilidade que já se paga** — não invente nada. Olhe o que um negócio já faz
   (anúncio, conteúdo, outreach, funil) e escolha uma dessas. Regra **1-1-1**: um produto, um avatar,
   um canal, até bater $1 milhão. Hack para achar no B2C: *"imprima sua fatura do cartão e veja onde você realmente gasta"*
4. **Aprender de verdade** — *"aprendizado é mesma condição, novo comportamento"*. Se você consome
   conteúdo e nada muda no seu comportamento, você não aprendeu. Não são 10.000 horas, são
   **10.000 iterações** (loops de feedback). Jeito mais rápido: contratar alguém muito bom, 1-a-1,
   mesmo mal podendo pagar
5. **Gastar nos lugares certos** — três baldes: ferramentas (CRM, landing page), ajuda de
   implementação (curso, tutoria), e tentativas (rodar os primeiros anúncios)
6. **Não aumentar o padrão de vida** — *"tudo menos comida e moradia é seu lucro"*. Ganhando ~$20K/mês
   na primeira academia, continuou dividindo quarto por $400

> *"Você nunca chega aos 100 mil na conta só aumentando a receita. Você também tem que impedir que seu padrão de vida tome de volta, para finalmente conseguir guardar."*
> *"O dia em que você para de gastar dinheiro aprendendo é o dia em que você decide que não quer ganhar mais."*
> *"Você quer ser rico, não parecer rico. Isso é sobre 100 mil no banco, não 100 mil em faturamento."*

---

## Parte 7 — IA como serviço (o caminho sem produto)

Modelo mais rápido para caixa: não construa SaaS, **venda IA implementada** para empresa que já tem
dinheiro.

### João Mussoi — Google Maps + GoHighLevel (o mais replicável)

- **Cliente-alvo:** empresa local com poucas avaliações no Google (<100), nota <4,8, sem site, mas
  estabelecida há anos. Foca primeiro em geografia, depois em nicho
- **Oferta:** "reativação de base" — agente de IA (GoHighLevel Conversation AI, canal WhatsApp) que
  varre os contatos parados do CRM do cliente e tenta reagendar
- **Preço:** R$500 a R$1.500 de implementação **ou** variável por lead reativado que compareceu
  (R$20-200 conforme o ticket do cliente). Regra: fixo quando o ciclo de venda é longo, variável
  quando o cliente cobra na hora
- **Prospecção (100% cold call, sem tráfego):**
  1. Google Maps: "nicho + cidade"
  2. Extensão **Instant Data Scraper** → lista de 100-200 empresas
  3. Abertura de curiosidade: *"estranho, aqui diz que vocês estão fechados por algum motivo"*
  4. Pitch: *"eu literalmente construí uma IA para sua empresa que pode agendar de 10 a 20 visitas nos próximos 7 dias"*
  5. Qualificação: *"tudo que precisamos é de uma base de 2.000 a 5.000 leads"*

> *"Vendas é um jogo de números. A diferença de quem teve resultado para quem não teve é dedicação, disciplina e persistência."*

### Bruno Gabarra — 3 modelos

1. Agente de WhatsApp para PME via Claude + N8N — R$1.000-2.000/mês, custo de API R$100-150/mês (margem alta)
2. Vibe coding sob encomenda para infoprodutor (calculadora, dashboard) — R$2.000 a R$20.000 por projeto
3. Funil completo (posicionamento + tráfego + agente) — R$3.000-6.000/mês

⚠️ Ele não explica como conseguir os primeiros clientes — pressupõe a rede que ele já tem (agência,
escola online, ferramenta própria faturando +R$1 milhão).

### Kevin Rodrigues — imagens de produto com IA

Vende imagem gerada para lojinhas de perfume/cosmético. ChatGPT (mapeia o produto) → Gemini (gera) →
Photoshop (finaliza). **A sacada da prospecção:** curtir e seguir lojas amadoras para o algoritmo do
Instagram passar a mostrar anúncios desse nicho no feed — aí ele aborda **quem já paga anúncio**,
porque já tem orçamento de marketing. Não aborda loja orgânica.

---

## Parte 8 — O que é realista para você

**Reproduzível do zero, sem audiência:**
- O processo técnico de construção (Claude Code / Lovable / AI Studio) — é genuinamente acessível
- Os 4 filtros de validação do Samuel Rondo
- O cold outreach do João Mussoi — depende de ligar em volume, não de audiência
- A técnica do Kevin Rodrigues (imagens de produto)
- O framework do Hormozi — é disciplina, não sorte

**Depende de sorte:** Jaxon (30M views) e Junior Moreira (850K views) dependeram de **um vídeo
viralizar**. Não se repete sob demanda.

**Depende de vantagem prévia invisível no vídeo:** Bruno Gabarra e Thiago Boeira já tinham agência e
anos de tráfego pago; Umberto já tinha lista desde 2020; DataCrazy tem 64 funcionários.

### O caminho que eu seguiria, na ordem

1. **Escolher um problema que alguém já paga para resolver** (Hormozi passo 3) — não invente
2. **Aplicar os 4 filtros do Samuel Rondo** ao concorrente — especialmente o filtro 3 (pouco ads = demanda orgânica real)
3. **Construir o MVP** em Lovable/Claude Code — dias, não meses
4. **Cobrar desde o primeiro usuário.** O DataCrazy e o Angus concordam: o produto se conserta com
   feedback de quem paga, não com mais código
5. **Distribuição antes de mais features** — escolha UM canal (regra 1-1-1) e vá até doer
6. **Medir churn desde o dia 1** — é o número que o corpus inteiro esconde e o que decide tudo

---

*Extraído da leitura integral de 18 transcrições em `references/youtube/`. Cada afirmação é
rastreável ao vídeo e timestamp de origem. Legendas automáticas — números e nomes de ferramentas
podem conter erros.*
