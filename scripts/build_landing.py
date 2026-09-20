#!/usr/bin/env python3
"""Gera a página inicial (estilo linktree) com os 8 tópicos e progresso de leitura.

Uso: python3 scripts/build_landing.py [saida.html]
"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_guia import CSS, HEAD_ICONS, ROOT, TOPICS, TOPICS_META, TRACKING_JS  # noqa: E402


def fontes_curtas(stem, limit=3):
    md = (ROOT / "guias" / f"{stem}.md").read_text(encoding="utf-8")
    for line in md.split("\n"):
        if line.startswith("**Fontes:**"):
            nomes = [n.strip() for n in line.replace("**Fontes:**", "").split("·")]
            nomes = [n.split(" (")[0].strip() for n in nomes if n.strip()]
            extra = len(nomes) - limit
            shown = ", ".join(nomes[:limit])
            return shown + (f" +{extra}" if extra > 0 else "")
    return ""


LANDING_CSS = """
/* --- a lista de tópicos continua dentro do próprio hero (fundo "atmosphere"
   edge-to-edge da página) em vez de um painel recortado por cima --- */
.hero-controls{
  display:flex; align-items:center; justify-content:space-between; gap:14px;
  flex-wrap:wrap; margin:8px 0 28px;
}
.hero-label{
  font-family:var(--mono); font-size:10.5px; text-transform:uppercase;
  letter-spacing:.16em; color:rgba(248,250,252,.72);
}
.progress{
  display:flex; align-items:center; gap:11px;
  font-family:var(--mono); font-size:11px; color:rgba(248,250,252,.78);
}
.progress-bar{
  flex:1; width:150px; max-width:40vw; height:5px; border-radius:var(--radius-pill);
  background:rgba(248,250,252,.18); overflow:hidden;
}
.progress-fill{height:100%;background:#F8FAFC;border-radius:var(--radius-pill);transition:width var(--reveal) var(--ease)}

.filter-pills{
  display:inline-flex; gap:3px; padding:4px; border-radius:var(--radius-pill);
  background:var(--glass-clear); backdrop-filter:blur(var(--blur-clear));
  -webkit-backdrop-filter:blur(var(--blur-clear));
  border:1px solid rgba(255,255,255,.16);
}
.filter-pill{
  border:0; background:transparent; cursor:pointer; white-space:nowrap;
  font:600 12px var(--sans); color:rgba(248,250,252,.76);
  padding:7px 14px; border-radius:var(--radius-pill);
  transition:background var(--fast) var(--ease),color var(--fast) var(--ease);
}
.filter-pill:hover{color:#fff}
.filter-pill.is-active{background:rgba(248,250,252,.94);color:#1F2E3A}

.cardlist{
  list-style:none; margin:0; padding:0; counter-reset:card;
  display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:14px;
}
.group{margin-top:28px}
.group:first-child{margin-top:0}
.group[hidden]{display:none}
.group-title{
  display:flex;align-items:baseline;gap:10px;margin:0 0 12px;padding:0;border:0;
  font-family:var(--mono);font-size:11px;font-weight:500;text-transform:uppercase;
  letter-spacing:.16em;color:rgba(248,250,252,.6);
}
.group-count{letter-spacing:.04em;text-transform:none;opacity:.8}
#read-section{margin-top:40px;padding-top:20px;border-top:1px dashed var(--border)}
#read-section .group-title{color:var(--ink-faint)}

/* --- card de tópico: material "frosted" (28px blur · 72% tint), leitura em
   primeiro plano sobre o palco escuro --- */
.card{
  counter-increment:card; min-width:0;
  position:relative; display:flex; flex-direction:column; gap:10px;
  background:var(--glass-frosted);
  backdrop-filter:blur(var(--blur-frosted)); -webkit-backdrop-filter:blur(var(--blur-frosted));
  border:1px solid rgba(255,255,255,.18); border-radius:var(--radius-card);
  padding:18px 18px 16px; color:var(--ink);
  box-shadow:var(--glass-rim),var(--shadow-glass);
  transition:transform var(--fast) var(--ease),box-shadow var(--fast) var(--ease),opacity var(--fast) var(--ease);
}
.card:hover{transform:translateY(-3px)}
.card.is-lido{opacity:.55}
.card.is-lido .card-title{text-decoration:line-through;text-decoration-color:var(--ink-faint)}
.card-link{
  display:flex; flex-direction:column; gap:9px;
  text-decoration:none; color:inherit; min-width:0;
}
.card-emoji{
  display:flex; align-items:center; justify-content:center; flex:none;
  width:42px; height:42px; font-size:21px; border-radius:var(--radius-control);
  background:color-mix(in srgb, var(--ink) 8%, transparent);
}
.card-body{min-width:0}
.card-tag{
  display:block; font-family:var(--mono); font-size:10px; text-transform:uppercase;
  letter-spacing:.1em; color:var(--action); margin:0 0 6px;
}
.card-tag::before{content:counter(card,decimal-leading-zero) " / "}
.card-title{
  display:block;font-family:var(--sans);font-weight:700;font-size:16.5px;
  line-height:1.28;color:var(--ink);letter-spacing:-.01em;margin-bottom:2px;
}
.card-lede{display:block;font-size:13.5px;color:var(--ink-soft);line-height:1.5}
.card-meta{
  display:flex; align-items:center; justify-content:space-between; gap:10px;
  margin-top:8px; padding-top:10px;
  border-top:1px solid color-mix(in srgb, var(--ink) 12%, transparent);
}
.card-fontes{
  display:block; font-family:var(--mono); font-size:10px; color:var(--ink-faint);
  min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}
.card-check{
  flex:none;display:flex;align-items:center;gap:5px;
  font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;
  color:var(--ink-faint);cursor:pointer;
}
.card-check input{width:15px;height:15px;accent-color:var(--success);cursor:pointer}

/* cor fixa (não segue --action/--text-inverse): é um CTA sobre o fundo
   claro da página, não texto sobre o hero escuro — precisa do mesmo
   contraste nos dois temas. */
.hub-link{
  display:inline-flex; align-items:center; gap:8px; margin-top:8px;
  font-family:var(--sans); font-size:13px; font-weight:600; color:#F8FAFC;
  background:#344F65; padding:11px 20px; border-radius:var(--radius-pill);
  text-decoration:none; box-shadow:var(--shadow-soft);
  transition:background var(--fast) var(--ease),transform var(--fast) var(--ease);
}
.hub-link:hover{background:#263F54;transform:translateY(-1px)}

@media(max-width:600px){
  .hero-controls{gap:12px}
  .progress-bar{max-width:100%}
  .cardlist{grid-template-columns:1fr}
  .card{padding:16px 16px 14px}
}
"""


def main():
    cards_by_cat = {}
    for idx, (stem, _title, _emoji, _tag) in enumerate(TOPICS):
        meta = TOPICS_META[stem]
        # o card da home usa o título "completo" (o mesmo da própria página do
        # guia); o hub tudo.html usa o título curto — comportamento original.
        title, emoji, tag, lede = meta["title_full"], meta["emoji"], meta["tag"], meta["lede"]
        fontes = fontes_curtas(stem)
        categoria_attr = html.escape(meta["categoria"])
        cards_by_cat.setdefault(meta["categoria"], []).append(
            f'<li class="card" data-stem="{stem}" data-i="{idx}" data-cat="{categoria_attr}">'
            f'<a class="card-link" href="{stem}.html">'
            f'<span class="card-emoji">{emoji}</span>'
            f'<span class="card-body">'
            f'<span class="card-tag">{html.escape(tag)}</span>'
            f'<span class="card-title">{html.escape(title)}</span>'
            f'<span class="card-lede">{html.escape(lede)}</span>'
            f'</span></a>'
            f'<span class="card-meta">'
            f'<span class="card-fontes">Fontes: {html.escape(fontes)}</span>'
            f'<label class="card-check">'
            f'<input type="checkbox" data-stem="{stem}"><span>Já li</span>'
            f'</label></span></li>'
        )

    cats = list(cards_by_cat.keys())
    groups_html = "".join(
        f'<section class="group" data-cat="{html.escape(cat)}">'
        f'<h2 class="group-title">{html.escape(cat)} <span class="group-count"></span></h2>'
        f'<ul class="cardlist">{"".join(items)}</ul></section>'
        for cat, items in cards_by_cat.items()
    )
    filter_pills = '<button type="button" class="filter-pill is-active" data-filter="todos">Todos</button>' + "".join(
        f'<button type="button" class="filter-pill" data-filter="{html.escape(cat)}">{html.escape(cat)}</button>'
        for cat in cats
    )

    out = f"""<title>CORTEX</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
{HEAD_ICONS}
<style>{CSS}{LANDING_CSS}</style>
<div class="hero" id="topo">
<div class="hero-inner">
  <p class="eyebrow">Biblioteca de transcrições · Síntese operacional</p>
  <h1 class="brand"><img class="brandmark" src="cortex-icon.png" alt="">CORTEX</h1>
  <p class="lede">Escolha por onde começar. O que você já leu desce pra baixo da lista sozinho —
  fica só o que falta.</p>
  <div class="hero-controls">
    <span class="hero-label">{len(TOPICS)} tópicos · {len(cats)} categorias</span>
    <div class="progress">
      <span id="progress-label">0 de {len(TOPICS)} lidos</span>
      <span class="progress-bar"><span class="progress-fill" id="progress-fill" style="width:0%"></span></span>
    </div>
    <div class="filter-pills" id="filter-pills">{filter_pills}</div>
  </div>
  <div id="groups">{groups_html}</div>
</div>
</div>
<div class="wrap">
<main style="max-width:820px">
<section class="group" id="read-section" hidden>
  <h2 class="group-title">Já lidos <span class="group-count"></span></h2>
  <ul class="cardlist" id="read-list"></ul>
</section>
<a class="hub-link" href="tudo.html">Ver os {len(TOPICS)} tópicos numa página só →</a>
<footer>
  482 vídeos, 225 canais. Cada afirmação nos guias é rastreável ao vídeo e timestamp de origem em
  <code>references/youtube/</code>.<br>
  O progresso de leitura fica salvo só neste navegador (localStorage) — não é sincronizado entre
  dispositivos. Parte do <a href="https://github.com/analuisamoutinho/estudos">repositório
  CORTEX</a>.
</footer>
</main>
</div>
{TRACKING_JS}
<script>
document.addEventListener('DOMContentLoaded', function(){{
  var root = document.getElementById('groups');
  var readSection = document.getElementById('read-section');
  var readList = document.getElementById('read-list');
  var label = document.getElementById('progress-label');
  var fill = document.getElementById('progress-fill');
  var total = {len(TOPICS)};
  var cards = Array.prototype.slice.call(document.querySelectorAll('li.card'))
    .sort(function(a,b){{ return a.getAttribute('data-i') - b.getAttribute('data-i'); }});
  var groupList = {{}};
  Array.prototype.forEach.call(root.querySelectorAll('.group'), function(g){{
    groupList[g.getAttribute('data-cat')] = g;
  }});
  var activeFilter = 'todos';

  function renderOrder(){{
    var lidos = window.estudosLidos.get();
    var read = [];
    cards.forEach(function(li){{
      var stem = li.getAttribute('data-stem');
      var input = li.querySelector('input');
      if (lidos[stem]) {{
        read.push(li);
        li.classList.add('is-lido');
        input.checked = true;
      }} else {{
        var home = groupList[li.getAttribute('data-cat')];
        home.querySelector('.cardlist').appendChild(li);
        li.classList.remove('is-lido');
        input.checked = false;
      }}
    }});
    read.sort(function(a,b){{
      return lidos[a.getAttribute('data-stem')] - lidos[b.getAttribute('data-stem')];
    }});
    read.forEach(function(li){{ readList.appendChild(li); }});

    Object.keys(groupList).forEach(function(cat){{
      var g = groupList[cat];
      var n = g.querySelectorAll('li.card').length;
      var matches = activeFilter === 'todos' || activeFilter === cat;
      g.hidden = n === 0 || !matches;
      g.querySelector('.group-count').textContent = n;
    }});
    readSection.hidden = read.length === 0;
    readSection.querySelector('.group-count').textContent = read.length;
    label.textContent = read.length + ' de ' + total + ' lidos';
    fill.style.width = Math.round((read.length/total)*100) + '%';
  }}

  document.addEventListener('change', function(e){{
    if (e.target.matches('li.card input[type=checkbox]')){{
      var li = e.target.closest('li.card');
      window.estudosLidos.set(li.getAttribute('data-stem'), e.target.checked);
      renderOrder();
    }}
  }});

  var pills = document.getElementById('filter-pills');
  if (pills) {{
    pills.addEventListener('click', function(e){{
      var btn = e.target.closest('.filter-pill');
      if (!btn) return;
      activeFilter = btn.getAttribute('data-filter');
      Array.prototype.forEach.call(pills.querySelectorAll('.filter-pill'), function(b){{
        b.classList.toggle('is-active', b === btn);
      }});
      renderOrder();
    }});
  }}

  renderOrder();
}});
</script>
"""
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "index.html"
    dest.write_text(out, encoding="utf-8")
    print(f"{dest}  ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
