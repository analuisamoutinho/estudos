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
.progress{
  display:flex;align-items:center;gap:12px;margin:22px 0 6px;
  font-family:var(--mono);font-size:11.5px;color:var(--ink-faint);
}
.progress-bar{flex:1;max-width:220px;height:5px;border-radius:99px;background:var(--surface-2);overflow:hidden}
.progress-fill{height:100%;background:var(--accent);border-radius:99px;transition:width .25s ease}
.cardlist{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.group{margin-top:34px}
.group[hidden]{display:none}
.group-title{
  display:flex;align-items:baseline;gap:10px;margin:0 0 12px;padding:0;border:0;
  font-family:var(--mono);font-size:11px;font-weight:500;text-transform:uppercase;
  letter-spacing:.16em;color:var(--ink-faint);
}
.group-count{letter-spacing:.04em;text-transform:none;opacity:.8}
#read-section{padding-top:18px;border-top:1px dashed var(--rule)}
.card{
  display:flex;align-items:center;gap:14px;background:var(--surface);
  border:1.5px solid var(--rule);border-radius:12px;padding:16px 18px;
  transition:border-color .15s,opacity .2s;
}
.card:hover{border-color:var(--accent)}
.card.is-lido{opacity:.52}
.card.is-lido .card-title{text-decoration:line-through;text-decoration-color:var(--ink-faint)}
.card-link{
  flex:1;min-width:0;display:flex;align-items:flex-start;gap:14px;
  text-decoration:none;color:inherit;
}
.card-emoji{font-size:26px;line-height:1.3;flex:none}
.card-body{min-width:0}
.card-title{
  display:block;font-family:var(--sans);font-weight:700;font-size:16.5px;
  color:var(--ink);letter-spacing:-.01em;
}
.card-tag{
  display:block;font-family:var(--mono);font-size:10px;text-transform:uppercase;
  letter-spacing:.12em;color:var(--accent);margin:3px 0 6px;
}
.card-lede{display:block;font-size:14px;color:var(--ink-soft);line-height:1.5;max-width:56ch}
.card-fontes{display:block;font-family:var(--mono);font-size:10.5px;color:var(--ink-faint);margin-top:7px}
.card-check{
  flex:none;display:flex;flex-direction:column;align-items:center;gap:4px;
  font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.08em;
  color:var(--ink-faint);cursor:pointer;padding:4px 6px;
}
.card-check input{width:18px;height:18px;accent-color:var(--accent);cursor:pointer}
.hub-link{
  display:inline-block;margin-top:46px;font-family:var(--mono);font-size:12px;color:var(--ink-soft);
}
@media(max-width:600px){
  .card{flex-direction:column;align-items:stretch}
  .card-check{flex-direction:row;align-self:flex-end}
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
        cards_by_cat.setdefault(meta["categoria"], []).append(
            f'<li class="card" data-stem="{stem}" data-i="{idx}" data-cat="{html.escape(meta['categoria'])}">'
            f'<a class="card-link" href="{stem}.html">'
            f'<span class="card-emoji">{emoji}</span>'
            f'<span class="card-body">'
            f'<span class="card-title">{html.escape(title)}</span>'
            f'<span class="card-tag">{html.escape(tag)}</span>'
            f'<span class="card-lede">{html.escape(lede)}</span>'
            f'<span class="card-fontes">Fontes: {html.escape(fontes)}</span>'
            f'</span></a>'
            f'<label class="card-check">'
            f'<input type="checkbox" data-stem="{stem}"><span>Já li</span>'
            f'</label></li>'
        )

    groups_html = "".join(
        f'<section class="group" data-cat="{html.escape(cat)}">'
        f'<h2 class="group-title">{html.escape(cat)} <span class="group-count"></span></h2>'
        f'<ul class="cardlist">{"".join(items)}</ul></section>'
        for cat, items in cards_by_cat.items()
    )

    out = f"""<title>CORTEX</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
{HEAD_ICONS}
<style>{CSS}{LANDING_CSS}</style>
<div class="wrap">
<main style="max-width:760px">
<header>
  <p class="eyebrow">Biblioteca de transcrições · Síntese operacional</p>
  <h1 class="brand"><img class="brandmark" src="cortex-icon.png" alt="">CORTEX</h1>
  <p class="lede">Escolha por onde começar. O que você já leu desce pra baixo da lista sozinho —
  fica só o que falta.</p>
  <div class="progress">
    <span id="progress-label">0 de {len(TOPICS)} lidos</span>
    <span class="progress-bar"><span class="progress-fill" id="progress-fill" style="width:0%"></span></span>
  </div>
</header>
<div id="groups">{groups_html}</div>
<section class="group" id="read-section" hidden>
  <h2 class="group-title">Já lidos <span class="group-count"></span></h2>
  <ul class="cardlist" id="read-list"></ul>
</section>
<a class="hub-link" href="tudo.html">Ver os {len(TOPICS)} tópicos numa página só →</a>
<footer>
  435 vídeos, 197 canais. Cada afirmação nos guias é rastreável ao vídeo e timestamp de origem em
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
      g.hidden = n === 0;
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

  renderOrder();
}});
</script>
"""
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "index.html"
    dest.write_text(out, encoding="utf-8")
    print(f"{dest}  ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
