---
title: "Páginas de Vendas de Low Ticket"
emoji: "🧾"
tag: "estrutura, checkout e métricas"
lede: "O que os vídeos da biblioteca mostram sobre páginas de vendas de low ticket que convertem: estrutura, o debate entre página, checkout com banner, VSL e quiz, números de funil e os riscos de copiar o que funciona."
title_full: "Páginas de Vendas de Low Ticket de Alta Conversão"
categoria: "Negócios"
order: 81
---

Estudo sobre páginas de vendas para produtos de ticket baixo (de R$ 9,90 a cerca de R$ 99, ou US$ 6,90 a US$ 9,90 no
mercado "global"), com base nas transcrições da biblioteca. Complementa o guia [Low Ticket e Tráfego Pago](low-ticket.md),
que tem o método de ponta a ponta; aqui o foco é só **a página, o checkout e a medição**.

> **Leia isto antes.**
> 1. **"Alta conversão" não foi provada por nenhum vídeo.** Nenhum mostra teste A/B de elementos da página. O que existe são
>    páginas de criadores que dizem vender, números de funil de dois produtos (Cássio Hart) e opiniões que se contradizem.
> 2. **Quase todo criador vende curso, template, ferramenta ou comunidade**, e várias das ferramentas recomendadas têm link de
>    indicação. Faturamento citado é alegação do vendedor.
> 3. **Só o que está marcado "lido" foi lido na íntegra.** Dos vídeos longos usei trechos (marcados "trechos"). Há 20 vídeos novos
>    buscados no YouTube sobre o tema que **ainda não baixaram** (verificação anti-robô); estão listados no fim, com link.
> 4. **Legendas automáticas:** números e nomes podem estar errados. Onde a legenda truncou algo, eu digo.

---

## Resumo

1. A estrutura mais citada, **no mesmo molde em vários criadores**: headline com o que é e para quem, subheadline com um **número**
   ("50 aulas", "200 dinâmicas"), mockup do produto, o que vem dentro, bônus numerados, prova social, garantia de 7 dias, ancoragem de
   preço, FAQ e botão final. Veja a Parte 2.
2. **Clareza e especificidade** são o critério que Nícolas Moreira e Allan Torquato usam para separar página boa de ruim: o visitante
   precisa entender **o que recebe, em que quantidade e se é para ele** sem rolar. O produto é "visual" (mockup, capa, prints).
3. **Os criadores discordam em três pontos centrais**: página de vendas × tráfego direto para um checkout com banner; botão na primeira
   dobra; e VSL. Não há dado nos vídeos para decidir. Veja a Parte 3.
4. O número que mais mudou o raciocínio dos vídeos é o **funil por etapa**. Cássio Hart mostra dois produtos de mesmo ticket (R$ 97), um
   com **18,6%** e outro com **7,9%** das visitas indo ao checkout, e o checkout convertendo **33,7%** e **45,1%**. Conserte a etapa pior.
5. **Velocidade e celular**: Cássio fala que mais de 90% do tráfego dele vem do celular; Caio Martins pede *connect rate* acima de 80%.
   Dois produtos do Cássio tiveram 81,8% e 71,3%.
6. O dinheiro de low ticket está **no checkout e na esteira** (order bump, upsell, recuperação), não só na página. Veja a Parte 5.
7. **IA para montar a página** é consenso (Replit, Claude, Lovable, Hostinger), com ressalvas de Silvio Roberto: fundo claro, nada de
   botão de compra na primeira dobra, pixel e token no prompt, hospedar no domínio próprio.
8. **Riscos que os vídeos tratam como detalhe**: depoimentos gerados por IA sem pessoa real, urgência e preço "de" fictícios,
   copiar página e VSL de concorrente. Veja a Parte 7.

---

## Parte 1 — Como medir "converte" (antes de julgar uma página)

### As etapas do funil e o número de cada uma

Cássio Hart, em **"Como lucrar com Low Ticket em 2026"** (1:25:42, [vídeo](https://www.youtube.com/watch?v=VBSDTUldSEE)), trechos:
*"nem todo mundo que vê clica, nem todo mundo que clica espera carregar, nem todo mundo que chega na página avança pro checkout, nem todo
mundo que tá no checkout compra"* [00:32:18]. Ele mostra os números de dois produtos de **R$ 97**:

| Etapa | Produto 1 | Produto 2 |
|---|---|---|
| Investimento | R$ 5.900 | R$ 9.600 |
| Cliques no anúncio | 3.118 | 5.116 |
| Esperaram a página carregar | 2.552 | 3.648 |
| Foram ao checkout | 475 | 288 |
| Compras | 160 | 130 |
| **Connect rate** (carregou ÷ cliques) | **81,8%** | **71,3%** |
| **Página → checkout** (checkout ÷ carregou) | **18,6%** | **7,9%** |
| **Checkout → compra** | **33,7%** | **45,1%** |

As porcentagens da linha de baixo são contas minhas sobre os números que ele mostra; ele cita "18%", "33%", "7,89" e "45%" [00:38:20-00:40:22].
Somando os dois produtos, ele diz ter investido R$ 15.541 e faturado R$ 43.300 [00:36:20] (cerca de 2,8 vezes).

O que ele conclui, e vale como regra de leitura:
- **O custo por compra não é só problema de criativo.** Se a página converte pouco, "não adianta testar milhares de criativos"
  [00:36:20].
- Segundo ele, os dois produtos tinham o mesmo ticket (R$ 97) e custo por clique parecido (cerca de R$ 1,80 a R$ 1,90), e a página deu retornos
  bem diferentes: no produto 2, 92% de quem chegou à página saiu sem ir ao checkout.
- *"Se eu dobro a taxa de conversão da página, de 7 para 15%, o retorno aumenta"* com as mesmas campanhas [00:40:22]. É aritmética, não resultado de teste.
- **Trocar o checkout derrubou o resultado** numa oferta dele, mesmo achando que o novo era melhor: *"só vou saber colocando tráfego"* [00:40:22].
- Um gateway de pagamento que mostrava aviso de "possível golpe" fez um cliente desistir, e ele atribui queda de conversão a isso [00:54:28].

### Metas citadas

| Métrica | Valor citado | Fonte |
|---|---|---|
| Connect rate | acima de 80% | Caio Martins [00:34:14] |
| Conversão de checkout | 30% ou mais; abaixo de 19% indica problema de confiança | guia [Low Ticket](low-ticket.md) (síntese de outros vídeos) |
| Mobile | "mais de 90% do tráfego" | Cássio Hart, checkout com IA [00:04:02] |
| Associar a conta do Instagram ao anúncio | "aumenta uns 30 a 40% de conversão" | Caio Martins [00:32:14] (alegação, sem dado) |

---

## Parte 2 — Anatomia da página (o molde que se repete)

### O critério: tangível, clara, específica, mensurável

*Lido:* **Nícolas Moreira — "A Página de Vendas que Me Gerou R$ 111.657 Com Low Ticket Global"** (21:21,
[vídeo](https://www.youtube.com/watch?v=Euu4CmTQx50)), lido até 00:14:03. Os quatro critérios dele [00:02:00-00:04:00]:

1. **Tangível**: a pessoa "sente" o produto (mockup que parece um e-book folheável no celular).
2. **Clara**: entende o que a oferta promete ao entrar.
3. **Específica**: fala direto com a persona, sem "mecanismo único" inventado.
4. **Mensurável**: dá quantidade (quantas aulas, quantos modelos).

E a premissa: em low ticket *"a pessoa já reconhece o problema, você só vem com a solução"* [00:04:00].

### A sequência de seções (síntese de três páginas)

A tabela cruza a página do Nícolas (pack de 50 aulas de canto), as duas páginas "validadas" que ele analisa em **"Seu Low Ticket Não
Vende?"** (26:16, [vídeo](https://www.youtube.com/watch?v=mYiFs95ddRA)) e a página do Allan Torquato (**"Analisei as páginas dos low
ticket LATAM"**, 11:49, [vídeo](https://www.youtube.com/watch?v=cZmFHdXjIWo)).

| # | Seção | O que fazem | Onde |
|---|---|---|---|
| 1 | Barra de urgência | "Desconto aplicado só hoje" | Nícolas [00:04:00] |
| 2 | **Headline** | Diz o que é e para quem: "Pack de aulas prontas para professores de canto"; "200 dinâmicas cristãs interativas"; "150 atividades musicais" | Nícolas, mYiFs [00:06:04] |
| 3 | **Subheadline** | Traz **número** e uso imediato: "50 aulas estruturadas, prontas para imprimir e aplicar hoje mesmo" | Nícolas [00:06:01] |
| 4 | **Mockup** | Imagem do produto, em mais de um ângulo ao longo da página; um vídeo curto ("mini VSL") é a alternativa | Nícolas [00:06:01], mYiFs [00:08:04] |
| 5 | Botão | Rola para a seção da oferta (ver divergência na Parte 3) | Nícolas [00:06:01] |
| 6 | Estrutura do material | Nível básico ao avançado, método claro, adaptável a idades | Nícolas [00:06:01] |
| 7 | O que você recebe | Lista dos módulos ou temas | Nícolas [00:06:01], mYiFs [00:08:04] |
| 8 | **Bônus numerados** | "Bônus 1 a 5", cada um com valor riscado e "hoje grátis"; Allan soma e diz que passam de US$ 49 | Nícolas [00:08:02], Allan [00:08:03] |
| 9 | "Este pack é para você" | Lista de subnichos (principiantes, experientes, autônomos, escolas) | Nícolas [00:08:02] |
| 10 | Prova social | Depoimentos; ele recomenda deixá-los **acima da oferta** | Nícolas [00:10:02], mYiFs [00:04:02] |
| 11 | Recapitulação da oferta | Repete tudo o que recebe, com outro ângulo de mockup | Nícolas [00:10:02] |
| 12 | **Quebra de objeções** | Garantia de 7 dias, acesso vitalício, atualizações grátis | Nícolas [00:10:02-00:12:02] |
| 13 | **Ancoragem de preço** | Preço "de" riscado e preço atual; "pague em sua moeda local" para venda em dólar | Nícolas [00:12:02] |
| 14 | FAQ | Perguntas frequentes, "obrigação ter" | Nícolas [00:12:02], Allan [00:10:03] |
| 15 | Botão final | Um único CTA | Nícolas [00:12:02] |

Ponto que aparece nos três: **o preço vem tarde**, depois de tratar objeções (Silvio Roberto também recomenda "valor só no final" [00:04:02]).

### Número em tudo

Nícolas repete: *"sempre coloco 50 aulas prontas para professores, 50 protocolos para médicos"* [mYiFs 00:06:04]; coloca numeração nos bônus e
no que a pessoa recebe [mYiFs 00:10:04]. Na página "validada" que analisa, a headline já traz **"mais de 200"** e a subheadline lista os usos.
O produto "genérico" que ele critica (planos para professores sem número, mockup genérico, dois planos de mesmo preço) é o contra-exemplo.

### O que aparece na página ruim

Nícolas e Allan descrevem, com quase as mesmas palavras:

- Criativo vago que não diz o que é; o criativo é *"80/20 da operação"* [mYiFs 00:02:00].
- Página **sem mockup** ou com imagem genérica; headline fraca; **sem bônus no início**; prova social **embaixo**; **sem garantia**.
- **Dois planos de mesmo preço** sem lógica de upgrade [mYiFs 00:04:02].
- **Sem order bump** no checkout e **sem avaliação** no marketplace (sinal de que não vende) [mYiFs 00:06:04].
- **Anunciar direto no checkout cru** sem nenhuma página, e hospedar no domínio do marketplace [Allan 00:00:00-00:02:01].
- Mockup de capa errada, imagem com baixa qualidade, página pesada [Allan 00:06:03-00:08:03].

---

## Parte 3 — Onde os criadores discordam

### 3.1 Página de vendas × tráfego direto para checkout com banner

| Posição | Quem | Argumento |
|---|---|---|
| **Sempre tenha página** | Allan Torquato | *"Ah, posso fazer só no checkout? Não faça… não vai"* [00:02:01]. Ilustra: 100 cliques, 40 chegam ao checkout, "perdeu R$ 120 se pagou R$ 2 no clique" [00:10:03]. É uma ilustração dele, não dado medido |
| **Anúncio → checkout com banner que parece landing** | Cássio Hart | *"A melhor maneira e mais fácil de tu começar a rodar, principalmente um produto low ticket"* [Checkout com IA, 00:02:01]. No checkout, um banner longo, **mobile-first**, gerado no ChatGPT, com order bumps, e recuperação de venda (Pix gerado sem pagar, abandono, cartão recusado) [00:00:00, 00:04:02] |
| **Anúncio → página → checkout** | Henrique Oliveira, Caio Martins, Nícolas | Página de vendas de R$ 9,90 com checkout de dois order bumps e dois upsells [Henrique, 00:02:01]; Caio define tráfego direto como subir o anúncio para uma página de vendas e depois ao checkout [00:26:12] |

Cássio justifica o checkout com banner por **custo e velocidade de teste**: quiz e VSL exigem ferramenta e edição, e ele diz que alterar a
"lead" de uma VSL para testar conversão dá muito trabalho [Funil R$ 419 mil, 00:14:06]. Em outro vídeo (**"Como fiz 289 vendas de um Low Ticket de
R$ 27"**, 39:58, [vídeo](https://www.youtube.com/watch?v=posOHrCnEBs), trechos), o checkout com banner é a estrutura da agência dele [00:06:02].

Nenhum dos dois mostra teste lado a lado com o mesmo produto. A diferença pode vir do produto, do ticket e do público; nenhum vídeo isola isso.
Repare que o próprio Cássio mostra, no vídeo do funil de R$ 419 mil, produtos que passam por página e, no mesmo vídeo, descreve o checkout
com banner como a estrutura da agência dele [00:14:06].

### 3.2 Botão na primeira dobra

- **Silvio Roberto:** não pôr botão na primeira dobra, que ele chama de erro mais comum. O botão que leva ao checkout faz a pessoa chegar fria; relata
  mentorados com muito *initiate checkout* e baixa conversão por isso [00:02:01-00:04:02].
- **Nícolas e Allan:** a página deles tem **botão logo depois do mockup**, mas o botão **rola até a seção da oferta**, não abre o checkout
  [Nícolas 00:06:01, Allan 00:08:03]. Nícolas até diz que em muitas páginas **não** põe esse botão, "faço a pessoa ler" [mYiFs 00:08:04].

Isso pode não ser contradição: Silvio critica botão que leva ao checkout; os outros usam âncora para a oferta. É leitura minha; confira ao testar.

### 3.3 VSL, mini VSL, quiz e fluxo no Typebot

- **Nícolas** analisa páginas "escaladas" com **mini VSL** (vídeo curto) e diz que dá para **trocar por mockup** [mYiFs 00:08:04, 00:14:06].
- **Cássio** evita VSL e quiz por custo e dificuldade de editar [00:14:06]; **Rafa Souza** (curso de 7 h, trechos) testa página, VSL, quiz e fluxo
  no Typebot, e diz que o que mais vende no caso dele é o **fluxo Typebot**, com produtos de R$ 19 a R$ 99 [05:20:38-05:22:39].
- O guia [Low Ticket](low-ticket.md) já registra que Silvio Roberto desaconselha VSL em low ticket; os vídeos novos de **Matheus Bressan**
  (página × VSL × quiz) estão na lista pendente.

### 3.4 Urgência e escassez

Na própria fonte principal há contradição: a página do Nícolas tem **barra de "desconto só hoje"** [00:04:00], e ele recomenda esse gatilho
como um que "converte bem". Na outra análise, diz *"eu não rodo com esse gatilho de escassez"* [mYiFs 00:08:04]. Pode ser um tipo diferente de gatilho (a legenda não deixa claro). Veja a Parte 7 sobre urgência falsa.

### 3.5 Fundo claro × escuro

Só Silvio Roberto trata do tema: *"site escuro converte menos que site claro"*, e pede fundo claro no prompt [00:02:01]. Sem dado.

---

## Parte 4 — Montar a página com IA (processo, não prompt único)

| Passo | Fonte | O que fazem |
|---|---|---|
| Ponto de partida | Silvio [00:00:00] | Começar de uma página existente ("modelagem"), mas ele avisa que o termo "virou sinônimo de plágio" e pede que o resultado seja aprimorado, não cópia |
| Ferramenta | Nícolas [00:02:00] | Replit (também Lovable, Bolt); ele oferece o template e um agente de copy, a quem pedir por Direct no Instagram |
| Prompt: público | Silvio [00:02:01] | Copy para **público frio**, com dados demográficos ("mulheres de 40 a 50 anos"); quanto mais detalhe, melhor |
| Prompt: layout | Silvio [00:02:01-00:04:02] | Responsivo; **fundo claro**; paleta do nicho; estilo visual; **sem botão de compra na primeira dobra**; preço só no fim, com parcelamento; link do botão já informado |
| Prompt: rastreio | Silvio [00:04:02-00:06:05] | Informar **ID do pixel e token** (conjunto de dados, API de conversões) já no primeiro prompt; links das imagens hospedadas |
| Mockup | Allan [00:04:02-00:06:03] | No ChatGPT, mandar a imagem e pedir o **prompt** que recria o mockup; usar a imagem original do criativo na página |
| Hospedagem | Allan [00:02:01], Silvio [00:08:07-00:10:07] | Domínio e hospedagem próprios (Allan indica a Hostinger, com cupom de parceria); **não deixar a página só no Lovable ou no Claude**, porque quem espiona ofertas procura páginas ali [Silvio]. Silvio cola o HTML num bloco do Elementor no WordPress |
| Checkout | Cássio [00:02:01-00:06:02] | Prompt no ChatGPT para gerar um **banner de checkout mobile**; comprimir a imagem antes de subir |

⚠️ Allan e Silvio **indicam ferramentas com link de parceria ou vendem curso** no mesmo vídeo; a Hostinger e a ferramenta de espionagem de anúncios (Radar) são
citadas com cupom ou link. Silvio pede também **evitar palavras que bloqueiam** o anúncio no título da página, como "emagreça" [00:10:07].

---

## Parte 5 — Checkout e esteira: onde o ticket sobe

| Fonte | Desenho citado | Observação |
|---|---|---|
| Henrique Oliveira, **"Fiz 150 vendas usando o NOVO Funil"** (16:01, [vídeo](https://www.youtube.com/watch?v=BNOlFQInty4), trechos) | Página de R$ 9,90 → checkout com **2 order bumps (R$ 9,90 e R$ 19,90)** → 2 upsells de R$ 9,90 [00:02:01]. Antes: checkout com no máximo 1 bump e página de obrigado [00:00:00] | Painel (VK Matrix) para ver front, bumps e upsells [00:12:04] |
| Cássio Hart, 289 vendas de R$ 27 | Bumps de R$ 97, R$ 47, R$ 47 e R$ 27 [00:06:02]; **comprando todos, o ticket vai a R$ 245** [00:18:06] | R$ 245 é o **máximo se todos forem comprados**, não a média |
| Allan Torquato | Produto de R$ 14,90 com 5 bumps chega a R$ 221 se todos forem comprados [00:06:03-00:08:03] | idem |
| Caio Martins (39:15, [vídeo](https://www.youtube.com/watch?v=1TY_nKIObJA), trechos) | 30 bumps de R$ 19,90 = R$ 600; 10 upsells de R$ 67; *"quem não tem order bump não tem negócio"* [00:08:04, 00:22:09] | Dados ilustrativos de aula |
| Nícolas Moreira | Duas ofertas analisadas: uma de R$ 37 com 4 order bumps [mYiFs 00:10:04-00:12:05]; outra com checkout da Hotmart com banner, timer e bumps [00:16:08] | Ele usa a **presença do bump** como sinal de oferta validada |

**Recuperação de venda** (Cássio): quem gerou Pix e não pagou, abandonou o carrinho ou teve cartão recusado recebe sequência de mensagens
por automação [Checkout com IA 00:00:00; 289 vendas 00:20:07]. Ele argumenta que quem chegou ao checkout já fez o trabalho caro (anúncio e
página) e não receber oferta nenhuma é desperdício [00:22:07].

**Pop-up antes do checkout** (Caio): ao clicar em comprar, aparece um formulário (nome, e-mail, telefone) que captura o lead antes do
checkout, para remarketing [00:34:14-00:36:14].

---

## Parte 6 — Como achar páginas validadas para estudar

Os sinais que os vídeos usam, em ordem de confiança:

1. **Muitas variações de criativo** para a mesma oferta e **muito tempo ativa** na Biblioteca de Anúncios. Nícolas diz que a oferta que ele escolheu
   tem várias variações e "bastante tempo ativa" [Nícolas 00:12:02]; Guilherme Asvi cita uma oferta com **410 anúncios ativos** levando à mesma
   página [Asvi 00:12:01]. (A Biblioteca não mostra gasto; veja a Parte 2 do guia [Captar Clientes de Marketing nos EUA](captar-clientes-marketing-eua.md) sobre os limites.)
2. **Order bump no checkout**: a lógica de que quem criou order bump validou a oferta [mYiFs 00:10:04-00:12:05]. É um argumento, não prova.
3. **Avaliações no marketplace**: ofertas sem nenhuma avaliação provavelmente não vendem; uma com 6 avaliações "vendeu" [mYiFs 00:06:04, 00:16:08].
4. **Cópia do domínio** para achar outras páginas anunciando a mesma oferta, back redirect, upsell e testes de VSL [Asvi 00:10:01-00:14:01].

⚠️ A mesma "modelagem" que os vídeos ensinam inclui **baixar a VSL e copiar a página do concorrente** [Asvi 00:18:01-00:20:01]. Veja a Parte 7.

---

## Parte 7 — Riscos que os vídeos tratam como detalhe

> Isto **não é aconselhamento jurídico**. Confirme com advogado antes de operar.

| Prática ensinada | Por que é risco | Quem |
|---|---|---|
| **Depoimentos "gerados artificialmente, sem foto"** | Prova social inventada pode configurar publicidade enganosa (no Brasil, o Código de Defesa do Consumidor trata de publicidade enganosa; nos EUA, a FTC tem regra contra avaliações e depoimentos falsos). Pode também derrubar conta e processadora | Nícolas [00:10:02] |
| **Urgência e escassez falsas** ("só hoje", contador que reinicia) | Também enganoso; plataformas e processadoras reagem | Nícolas [00:04:00] |
| **Preço "de" fictício** ("de US$ 79,40 por US$ 9,90") | O preço "de" precisa ter sido praticado de fato | Nícolas [00:12:02] |
| **Copiar página e VSL do concorrente** | Direito autoral; o próprio Silvio diz que "modelagem virou sinônimo de plágio" | Asvi, Silvio |
| **Garantia de 7 dias** | No Brasil, compra online já tem 7 dias de arrependimento por lei; a garantia tem de ser cumprida, e o reembolso aparece na sua taxa | Nícolas, Allan |
| **Promessas em nichos sensíveis** (saúde, emagrecimento) | Bloqueio de anúncio e de conta; Silvio manda evitar certas palavras no título da página | Silvio [00:10:07] |
| **"Esconder" a página de espionagem** | Ele orienta tirar a oferta validada do Lovable e hospedar no próprio domínio | Silvio [00:08:07] |

**Interesse do vendedor:** Nícolas vende templates, agente de copy e acesso por Direct; Allan vende o treinamento de R$ 9,90 e indica
Hostinger e Radar com cupom; Silvio vende curso de tráfego e grupo; Cássio fala "aqui na agência" (é dono de agência de tráfego). Faturamentos: Nícolas "R$ 111.657", Cássio "R$ 419.131",
Allan "6 anos vivendo de low ticket". Nenhum é auditado.

---

## Parte 8 — Checklist de uma página de low ticket

**Antes de publicar**
- [ ] Headline diz **o que é e para quem**, com um número ("50 aulas", "200 dinâmicas")
- [ ] Subheadline com **uso imediato** e **quantidade**
- [ ] **Mockup** claro do produto (e outro ângulo mais abaixo)
- [ ] "O que você recebe" listado; **bônus numerados**
- [ ] Prova social **real** (depoimento com pessoa, print de avaliação ou resultado de verdade)
- [ ] **Garantia** de 7 dias, acesso e atualizações descritos
- [ ] Preço **só depois** das objeções; preço "de" que existiu de verdade
- [ ] **FAQ** e **um CTA** final
- [ ] Carrega rápido no celular; connect rate acima de 80% depois de rodar
- [ ] Fundo claro, texto legível no celular, imagens comprimidas
- [ ] Pixel e token (API de conversões) instalados **e testados**
- [ ] Hospedagem em domínio próprio

**Depois de rodar (leia a etapa pior)**
- [ ] Connect rate baixo: página pesada, ajustar velocidade
- [ ] Página → checkout baixo (Cássio: 7,9% × 18,6%): reescrever **headline, mockup e oferta**
- [ ] Checkout → compra baixo: confiança, meios de pagamento, aviso de golpe do gateway, order bump mal escrito
- [ ] Muitos *initiate checkout* e poucas compras: botão na primeira dobra, preço, confiança (Silvio)
- [ ] **Mude uma coisa por vez** e compare no mesmo período

---

## Lacunas de evidência

- **Nenhum teste A/B de elementos de página** nos vídeos lidos (headline, mockup, botão, VSL).
- **Taxa de conversão por tipo de página** (página × checkout com banner × VSL × quiz) não aparece; só os dois produtos do Cássio.
- **Reembolso e chargeback** não são medidos nos vídeos de página.
- **Mercado global:** Nícolas diz vender para vários países, mas nenhum vídeo mostra a conversão por país.
- As **páginas** citadas não foram abertas aqui; descrevi o que cada criador diz delas.

---

## Índice

**Lidos (completos ou quase):**

| Vídeo | Canal | Duração | Link |
|---|---|---|---|
| A Página de Vendas que Me Gerou R$ 111.657 (até 00:14:03) | Nícolas Moreira | 21:21 | [YouTube](https://www.youtube.com/watch?v=Euu4CmTQx50) |
| Seu Low Ticket Não Vende? (3 erros; quase todo) | Nícolas Moreira | 26:16 | [YouTube](https://www.youtube.com/watch?v=mYiFs95ddRA) |
| Analisei as páginas dos low ticket LATAM | Allan Torquato | 11:49 | [YouTube](https://www.youtube.com/watch?v=cZmFHdXjIWo) |
| Criar ou Modelar Página de Vendas com IA | Silvio Roberto | 11:58 | [YouTube](https://www.youtube.com/watch?v=X0k9IxNEXHo) |

**Trechos (vídeos longos, só as partes sobre página, checkout e métricas):**

| Vídeo | Canal | Duração | Link |
|---|---|---|---|
| Como lucrar com Low Ticket em 2026: funil simples (R$ 419 mil) | Cássio Hart | 1:25:42 | [YouTube](https://www.youtube.com/watch?v=VBSDTUldSEE) |
| Como fiz 289 vendas de um Low Ticket de R$ 27 | Cássio Hart | 39:58 | [YouTube](https://www.youtube.com/watch?v=posOHrCnEBs) |
| Checkout para Low Ticket com IA | Cássio Hart | 10:16 | [YouTube](https://www.youtube.com/watch?v=FW1pf3l1mrU) |
| Fiz 150 vendas usando o novo funil | Henrique Oliveira | 16:01 | [YouTube](https://www.youtube.com/watch?v=BNOlFQInty4) |
| Criando um Low Ticket e vendendo com tráfego direto | Caio Martins | 39:15 | [YouTube](https://www.youtube.com/watch?v=1TY_nKIObJA) |
| Low Ticket: curso completo | Rafa Souza | 7:11:17 | [YouTube](https://www.youtube.com/watch?v=hPgS4RJcHQg) |
| Como encontrar uma oferta escalada, clonar e vender | Guilherme Asvi | 31:37 | [YouTube](https://www.youtube.com/watch?v=x9kljw6KCAI) |

**Buscados no YouTube sobre este tema e ainda não baixados** (verificação anti-robô do YouTube; tentar de novo mais tarde):

| Vídeo | Canal | Views | Link |
|---|---|---|---|
| Sales Page, VSL or Quiz? Which is better? | Matheus Bressan | 17,8 mil | [YouTube](https://www.youtube.com/watch?v=5nQ4876pUPo) |
| Quiz + VSL, melhor estratégia para low ticket | Matheus Bressan | 15 mil | [YouTube](https://www.youtube.com/watch?v=2DjQ-HEE92k) |
| Too many initiate checkouts and zero sales | Matheus Bressan | 14,3 mil | [YouTube](https://www.youtube.com/watch?v=JKXUngYj0SM) |
| Elementos necessários para uma página de alta conversão | Tiago Tessmann | 167,6 mil | [YouTube](https://www.youtube.com/watch?v=XdouTIM7SGE) |
| Como criar páginas de vendas de alta conversão para low ticket | Fernando Oliveira | 13 mil | [YouTube](https://www.youtube.com/watch?v=oTAHd7jU89k) |
| How I create low-ticket sales pages in practice | Heitor Nogueira | 12,2 mil | [YouTube](https://www.youtube.com/watch?v=cbrno-n1vpU) |
| Low Ticket em 2026: copie minha página validada | 1kevones | 18,2 mil | [YouTube](https://www.youtube.com/watch?v=dl_xy0M4DJs) |
| Como clonar, modelar ou criar página de vendas para low ticket | Guilherme Emanoel | 44,2 mil | [YouTube](https://www.youtube.com/watch?v=wgJgpyjBpG4) |
| How to create a high-converting low ticket checkout | Magnus Folletto | 9,4 mil | [YouTube](https://www.youtube.com/watch?v=RTyrocHt2wI) |
| Melhor estrutura de página de venda low ticket | Thiago Almeida | 3,2 mil | [YouTube](https://www.youtube.com/watch?v=57cVWghGfsk) |
| Página de Vendas Low Ticket: estrutura simples que converte | Eidi Diego | 2,7 mil | [YouTube](https://www.youtube.com/watch?v=Fob7Sbhy4gA) |
| Como criar a página de vendas perfeita em 2025 para low ticket | Allan Torquato | 3,8 mil | [YouTube](https://www.youtube.com/watch?v=msnqegqDjzI) |
| Understand everything about sales pages | Ícaro de Carvalho | 10,9 mil | [YouTube](https://www.youtube.com/watch?v=-A7ed8-EzWo) |
| 5 hacks to crack your order bump | Matheus Bressan | 6 mil | [YouTube](https://www.youtube.com/watch?v=7pUF4DPfpwQ) |
| Como aumentar o ROI do low ticket: upsell e downsell | Guilherme Emanoel | 7,5 mil | [YouTube](https://www.youtube.com/watch?v=rBdJWps3DqM) |
| I Studied 1000 Landing Pages, Here's What Works in 2026 | ThrillX | 76,8 mil | [YouTube](https://www.youtube.com/watch?v=PcwuZJNJny4) |
| Alex Hormozi's Landing Page Strategy for 2026 | ThrillX | 106,8 mil | [YouTube](https://www.youtube.com/watch?v=zA0B-VwOPn4) |
| 3 Landing Page Tests To Skyrocket Conversions | Alex Hormozi | 152,9 mil | [YouTube](https://www.youtube.com/watch?v=9Dc2UQbQNTo) |
| The Ultimate Step-By-Step Landing Page Guide | Sabri Suby | 324,7 mil | [YouTube](https://www.youtube.com/watch?v=zpTsCrOvGao) |
| How To Write a Sales Page | Alex Cattoni | 42,8 mil | [YouTube](https://www.youtube.com/watch?v=vho8y4WM1Lk) |

*Fontes: transcrições em `references/youtube/` (legendas automáticas do YouTube). Cada trecho é rastreável ao vídeo e ao timestamp.*
