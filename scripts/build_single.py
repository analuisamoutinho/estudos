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
from build_guia import CSS, HEAD_ICONS, ROOT, TOPICS_META, TRACKING_JS, convert, parse_frontmatter  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print("uso: build_single.py <stem> [saida.html]")
        sys.exit(1)
    stem = sys.argv[1]
    meta = TOPICS_META.get(stem, {"title": stem, "title_full": stem, "emoji": "📄", "tag": "", "lede": ""})
    title, emoji, tag, lede = meta["title_full"], meta["emoji"], meta["tag"], meta["lede"]

    path = ROOT / "guias" / f"{stem}.md"
    _, body_md = parse_frontmatter(path.read_text(encoding="utf-8"))
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
