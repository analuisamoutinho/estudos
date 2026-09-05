#!/usr/bin/env python3
"""Converte um único guia em guias/*.md numa página HTML standalone.

Uso: python3 scripts/build_single.py <stem> [saida.html]
Ex.: python3 scripts/build_single.py saas-produto /tmp/saas.html
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_guia import CSS, HEAD_ICONS, ROOT, TRACKING_JS, convert, slug  # noqa: E402

# stem -> (título, emoji, subtítulo, tagline curta para o header)
META = {
    "aquisicao-saas": (
        "Aquisição de Clientes para SaaS",
        "🧲",
        "os primeiros 100 assinantes",
        "Como conseguir assinantes para um SaaS — os canais que realmente trazem os primeiros "
        "clientes, garimpados por engajamento entre 143 vídeos.",
    ),
    "servicos-mil-dia": (
        "Serviços Digitais: a meta de R$1k/dia",
        "💰",
        "tráfego, IA, ebook e prospecção",
        "O que realmente é preciso para faturar R$1.000 por dia com serviço digital — as contas, os "
        "canais de prospecção e o que a matemática diz sobre a meta.",
    ),
    "upwork": (
        "Upwork e Freela Internacional",
        "🌎",
        "faturar em dólar",
        "Como pegar freela em dólar no Upwork e afins — perfil, proposta, precificação e o que os "
        "relatos honestos mostram sobre os primeiros meses.",
    ),
    "saas-produto": (
        "SaaS e Produto Digital",
        "💻",
        "recorrência com IA",
        "Construir e vender software com IA, sem programar — achar a ideia, montar o produto "
        "e a distribuição que os vídeos escondem.",
    ),
    "agencia-ia": (
        "Agência de IA e Automação",
        "🤖",
        "o caminho mais rápido para caixa",
        "Vender agentes de IA e automações para empresas — sem produto próprio, sem audiência, "
        "sem tráfego pago.",
    ),
    "low-ticket": (
        "Low Ticket e Tráfego Pago",
        "🎯",
        "adquirir cliente pagando",
        "Como adquirir cliente pagando por ele — 11 princípios de consenso e um método "
        "operacional em 8 fases.",
    ),
    "negocio-solo": (
        "Negócio Solo e Mentalidade",
        "🧠",
        "Hormozi e mentalidade",
        "Como sair do zero operando sozinho, sem se sabotar.",
    ),
    "copy-e-criativo": (
        "Copy, Criativo e Conteúdo",
        "✍️",
        "o que vende",
        "Escrever o que vende e produzir o que para o scroll.",
    ),
    "amar-a-deus-no-ordinario": (
        "Amar a Deus no Ordinário",
        "🕊️",
        "santidade na vida comum",
        "Buscar a Deus dentro do trabalho, da rotina, do cansaço e das obrigações banais — "
        "sem precisar de uma vida diferente da que você já tem.",
    ),
    "ecommerce": (
        "E-commerce e Dropshipping",
        "📦",
        "o experimento honesto",
        "O tópico menor da biblioteca, com o vídeo mais honesto de todos.",
    ),
    "ferramentas-de-ia": (
        "Ferramentas de IA na Prática",
        "🛠️",
        "Claude, Claude Code e N8N no real",
        "Como criadores realmente usam Claude, Claude Code e Gemini Omni — o fluxo de trabalho "
        "de verdade, com bug e retrabalho.",
    ),
    "numeros-e-ceticismo": (
        "Números e Ceticismo",
        "⚠️",
        "leia antes de tudo",
        "Auditoria de todos os resultados alegados na biblioteca — o número do título contra o "
        "que é dito dentro do vídeo.",
    ),
}


def main():
    if len(sys.argv) < 2:
        print("uso: build_single.py <stem> [saida.html]")
        sys.exit(1)
    stem = sys.argv[1]
    title, emoji, tag, lede = META.get(stem, (stem, "📄", "", ""))

    path = ROOT / "guias" / f"{stem}.md"
    md = path.read_text(encoding="utf-8")
    body_md = md.split("\n", 1)[1]
    body, subs = convert(body_md, stem, base_level=0)
    # Links para outros guias (ex.: [ecommerce.md]) viram #t-<stem> no hub multi-tópico,
    # âncora que não existe nesta página standalone — desfaz o link, mantém o texto.
    body = re.sub(r'<a href="#t-[^"]+">([^<]*)</a>', r"\1", body)

    nav = "".join(f'<a href="#{sid}">{html.escape(lbl)}</a>' for sid, lbl in subs)

    out = f"""<title>{html.escape(title)} · CORTEX</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
{HEAD_ICONS}
<style>{CSS}</style>
<div class="wrap">
<nav><p>Neste guia</p><a href="#topo"><b>Início</b></a>{nav}</nav>
<main>
<header id="topo">
  <p class="eyebrow">CORTEX · Guia individual</p>
  <h1>{emoji} {html.escape(title)}</h1>
  <p class="lede">{html.escape(lede)}</p>
  <div class="stats">
    <div class="stat"><b>{tag}</b><span>foco do guia</span></div>
  </div>
  <button type="button" id="lido-toggle" class="lido-toggle" data-stem="{stem}">
    <span class="lido-toggle-icon">✓</span><span class="lido-toggle-label">Marcar como lido</span>
  </button>
</header>
{body}
<footer>
  Extraído da leitura integral das transcrições em <code>references/youtube/</code>. Cada afirmação
  é rastreável ao vídeo e timestamp de origem.<br>
  Transcrições automáticas — números e nomes de ferramentas podem conter erros. Parte do
  <a href="https://github.com/analuisamoutinho/estudos">repositório CORTEX</a>.<br>
  <a href="index.html">← voltar para a lista de tópicos</a>
</footer>
</main>
</div>
{TRACKING_JS}
<script>
document.addEventListener('DOMContentLoaded', function(){{
  var btn = document.getElementById('lido-toggle');
  var stem = btn.getAttribute('data-stem');
  function render(){{
    var lidos = window.estudosLidos.get();
    var isLido = !!lidos[stem];
    btn.classList.toggle('is-lido', isLido);
    btn.querySelector('.lido-toggle-label').textContent = isLido ? 'Lido' : 'Marcar como lido';
  }}
  btn.addEventListener('click', function(){{
    var lidos = window.estudosLidos.get();
    window.estudosLidos.set(stem, !lidos[stem]);
    render();
  }});
  render();
}});
</script>
"""
    dest = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / f"{stem}.html"
    dest.write_text(out, encoding="utf-8")
    print(f"{dest}  ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
