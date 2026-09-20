#!/usr/bin/env python3
"""Converte GUIA.md + guias/*.md numa página HTML publicável.

Uso: python3 scripts/build_guia.py [saida.html]

Conversor escrito à mão para não adicionar dependência ao repo — cobre exatamente
o subconjunto de markdown que os guias usam.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_frontmatter(text):
    """Lê um bloco `---\nkey: valor\n---` no início do arquivo.

    Sem dependência de PyYAML: cobre só o que os guias usam (uma linha por
    campo, valor opcionalmente entre aspas). Retorna (metadados, resto_do_texto).
    """
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] == '"':
            val = val[1:-1]
        meta[key.strip()] = val
    body = text[end + 4:].lstrip("\n")
    return meta, body


def _load_topics():
    """Cada guias/*.md carrega seu próprio título/emoji/tag/lede/order no
    frontmatter. Isto é a fonte única de verdade da lista de tópicos —
    adicionar ou remover um tópico é só criar ou apagar o arquivo .md, sem
    tocar em código. Ordenado pelo campo `order` (menor primeiro)."""
    entries = []
    for path in sorted((ROOT / "guias").glob("*.md")):
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not meta.get("title"):
            continue
        entries.append({
            "stem": path.stem,
            "title": meta.get("title", path.stem),
            # título alternativo, mais longo, só para o <h1>/<title> da própria
            # página do guia — cai no "title" quando não definido
            "title_full": meta.get("title_full") or meta.get("title", path.stem),
            "emoji": meta.get("emoji", "📄"),
            "tag": meta.get("tag", ""),
            "categoria": meta.get("categoria") or "Outros",
            "lede": meta.get("lede", ""),
            "order": int(meta["order"]) if str(meta.get("order", "")).strip().lstrip("-").isdigit() else 999,
        })
    entries.sort(key=lambda e: e["order"])
    return entries


_TOPICS_LIST = _load_topics()
TOPICS_META = {e["stem"]: e for e in _TOPICS_LIST}
# Mantido no formato de tupla (stem, title, emoji, tag) por compatibilidade
# com o restante do código.
TOPICS = [(e["stem"], e["title"], e["emoji"], e["tag"]) for e in _TOPICS_LIST]


def inline(text):
    out = []
    for i, chunk in enumerate(re.split(r"(`[^`]+`)", text)):
        if i % 2:
            out.append(f"<code>{html.escape(chunk[1:-1])}</code>")
            continue
        c = html.escape(chunk)
        c = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: _link(m), c)
        c = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", c)
        c = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", c)
        out.append(c)
    return "".join(out)


def _link(m):
    """Links entre guias viram âncoras internas; o resto fica como está."""
    label, href = m.group(1), m.group(2)
    stem = re.sub(r"^(guias/)?", "", href).replace(".md", "").split("#")[0]
    if stem in dict((t[0], t) for t in TOPICS):
        return f'<a href="#t-{stem}">{label}</a>'
    if href.endswith(".md") or href.startswith("references/"):
        return label  # caminho de repo: não é clicável na web
    return f'<a href="{href}">{label}</a>'


def slug(prefix, text):
    s = re.sub(r"[^\w\s-]", "", re.sub(r"<[^>]+>", "", text)).strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    return f"{prefix}-{s}"


def render_table(rows):
    def cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]

    head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
    out = ['<div class="scroll"><table><thead><tr>']
    out += [f"<th>{inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def render_list(items):
    checklist = any(re.match(r"\[[ x]\]\s", t) for _, t in items)
    ul_open = '<ul class="check">' if checklist else "<ul>"
    out = [ul_open]
    depth = 0
    for ind, text in items:
        want = 1 if ind >= 2 else 0
        while depth < want:
            out.append("<ul>")
            depth += 1
        while depth > want:
            out.append("</ul>")
            depth -= 1
        m = re.match(r"\[([ x])\]\s+(.*)", text)
        out.append(
            f"<li><span></span>{inline(m.group(2))}</li>" if m else f"<li>{inline(text)}</li>"
        )
    out.append("</ul>" * (depth + 1))
    return "".join(out)


def convert(md, prefix, base_level=0):
    """base_level desloca os títulos (h1 do guia vira h2 da página)."""
    lines = md.split("\n")
    body, subs = [], []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            body.append(
                f'<div class="scroll"><pre><code>{html.escape(chr(10).join(block))}</code></pre></div>'
            )
            continue

        if re.fullmatch(r"-{3,}", stripped):
            body.append("<hr>")
            i += 1
            continue

        m = re.match(r"(#{1,4})\s+(.*)", stripped)
        if m:
            lvl, text = min(len(m.group(1)) + base_level, 6), m.group(2)
            sid = slug(prefix, text)
            if lvl == 3:
                label = text.split(" — ")[0].strip()
                subs.append((sid, label))
            body.append(f'<h{lvl} id="{sid}">{inline(text)}</h{lvl}>')
            i += 1
            continue

        if stripped.startswith(">"):
            quotes = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quotes.append(lines[i].strip().lstrip(">").strip())
                i += 1
            if len(quotes) > 1 and not quotes[1].startswith("*"):
                quotes = [" ".join(quotes)]
            inner = "".join(f"<p>{inline(q)}</p>" for q in quotes if q)
            body.append(f"<blockquote>{inner}</blockquote>")
            continue

        if stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            body.append(render_table(rows))
            continue

        if re.match(r"[-*\d]\.?\s", stripped) and re.match(r"[-*]\s|\d+\.\s", stripped):
            ordered = bool(re.match(r"\d+\.\s", stripped))
            items = []
            while i < len(lines):
                cur = lines[i]
                if re.match(r"\s*([-*]\s|\d+\.\s)", cur):
                    ind = len(cur) - len(cur.lstrip())
                    items.append((ind, re.sub(r"^\s*([-*]|\d+\.)\s+", "", cur).strip()))
                    i += 1
                elif cur.strip() and not re.match(r"\s*[|>#`]", cur) and items:
                    ind, prev = items[-1]
                    items[-1] = (ind, prev + " " + cur.strip())
                    i += 1
                else:
                    break
            rendered = render_list(items)
            if ordered:
                rendered = rendered.replace("<ul>", "<ol>").replace("</ul>", "</ol>")
            body.append(rendered)
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not re.match(
            r"\s*([-*]\s|\d+\.\s|[|>#]|```|-{3,}$)", lines[i]
        ):
            para.append(lines[i].strip())
            i += 1
        if not para:
            # Linha que nenhum bloco reconheceu (ex.: "#Titulo" sem espaço).
            # Sem isto o laço não avança e o build trava.
            para.append(stripped)
            i += 1
        body.append(f"<p>{inline(' '.join(para))}</p>")

    return "".join(body), subs


CSS = """
:root{
  --bg:#EDF1F4; --surface:#F8FAFC; --surface-raised:#FFFFFF; --surface-muted:#E2E9EF;
  --ink:#243746; --ink-soft:#546777; --ink-faint:#7E90A0; --text-inverse:#F8FAFC;
  --border:#CCD6DE; --border-control:#8294A3;
  --action:#344F65; --action-hover:#263F54; --focus:#396E98;
  --success:#28644F; --success-bg:#E5F0EA;
  --warning:#805B1D; --warning-bg:#F4EDDF;
  --danger:#A63D4B; --danger-bg:#F8E9EB;
  --info:#345F83; --info-bg:#E3ECF4;
  --glass-clear:rgba(255,255,255,.10); --glass-frosted:rgba(248,250,252,.72); --glass-liquid:rgba(255,255,255,.16);
  --blur-clear:12px; --blur-frosted:28px; --blur-liquid:24px;
  --glass-rim:inset 0 1px 0 rgba(255,255,255,.65),inset 1px 0 0 rgba(255,255,255,.16);
  --atmosphere:radial-gradient(ellipse at 85% 0%,#9EAFBB 0%,transparent 58%),linear-gradient(125deg,#294355 0%,#526C80 54%,#8A9FAE 100%);
  --sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --mono:'SFMono-Regular',Consolas,'Liberation Mono',monospace;
  --radius-sm:.5rem; --radius-control:.875rem; --radius-card:1.75rem; --radius-stage:2rem; --radius-pill:999px;
  --shadow-soft:0 8px 30px rgba(36,55,70,.05);
  --shadow-raised:0 24px 64px rgba(25,44,60,.14);
  --shadow-glass:0 16px 40px rgba(17,34,49,.15);
  --ease:cubic-bezier(.22,1,.36,1);
  --press:120ms; --fast:180ms; --reveal:280ms;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#131A21; --surface:#1A222B; --surface-raised:#202A34; --surface-muted:#25303B;
    --ink:#E9EFF4; --ink-soft:#AAB9C6; --ink-faint:#758795;
    --border:#2C3945; --border-control:#4B5C6C;
    --action:#89ABC6; --action-hover:#A6C3DA; --focus:#6FA9D6;
    --success:#63C09E; --success-bg:#132621;
    --warning:#DDB169; --warning-bg:#2A2313;
    --danger:#E38F9A; --danger-bg:#2B181B;
    --info:#8FB6D8; --info-bg:#15222E;
    --glass-frosted:rgba(26,34,43,.72); --glass-clear:rgba(255,255,255,.06); --glass-liquid:rgba(255,255,255,.08);
    --glass-rim:inset 0 1px 0 rgba(255,255,255,.10),inset 1px 0 0 rgba(255,255,255,.05);
  }
}
:root[data-theme="dark"]{
  --bg:#131A21; --surface:#1A222B; --surface-raised:#202A34; --surface-muted:#25303B;
  --ink:#E9EFF4; --ink-soft:#AAB9C6; --ink-faint:#758795;
  --border:#2C3945; --border-control:#4B5C6C;
  --action:#89ABC6; --action-hover:#A6C3DA; --focus:#6FA9D6;
  --success:#63C09E; --success-bg:#132621;
  --warning:#DDB169; --warning-bg:#2A2313;
  --danger:#E38F9A; --danger-bg:#2B181B;
  --info:#8FB6D8; --info-bg:#15222E;
  --glass-frosted:rgba(26,34,43,.72); --glass-clear:rgba(255,255,255,.06); --glass-liquid:rgba(255,255,255,.08);
  --glass-rim:inset 0 1px 0 rgba(255,255,255,.10),inset 1px 0 0 rgba(255,255,255,.05);
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:var(--sans); font-size:16px; line-height:1.62;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1240px;margin:0 auto;padding:0 20px;display:flex;gap:48px;align-items:flex-start}
main{flex:1;min-width:0;max-width:72ch;padding:44px 0 110px}

nav{
  position:sticky; top:0; width:224px; flex:none;
  padding:56px 0 40px; font-family:var(--mono); font-size:11px;
  max-height:100vh; overflow-y:auto;
}
nav p{
  margin:0 0 12px; text-transform:uppercase; letter-spacing:.14em;
  color:var(--ink-faint); font-size:9.5px;
}
nav a{
  display:block; padding:6px 0 6px 11px; border-left:2px solid var(--border);
  color:var(--ink-soft); text-decoration:none; line-height:1.35;
  transition:border-color var(--fast) var(--ease),color var(--fast) var(--ease);
}
nav a:hover{border-left-color:var(--action);color:var(--action)}
nav a b{display:block;font-weight:600;color:var(--ink);letter-spacing:.01em}
nav a span{display:block;color:var(--ink-faint);font-size:9.5px;margin-top:1px}
nav .sub{padding-left:22px;border-left-color:transparent;font-size:10px}
nav .sub:hover{border-left-color:var(--border)}
@media(max-width:960px){nav{display:none}.wrap{gap:0}main{max-width:none;padding-top:32px}}

h1,h2,h3,h4,h5{font-family:var(--sans);text-wrap:balance;line-height:1.18;letter-spacing:-.02em}
h1{font-size:clamp(28px,5vw,42px);font-weight:750;margin:0 0 6px}
h2{
  font-size:clamp(22px,3.4vw,29px); font-weight:750; margin:0 0 8px;
  padding-top:24px;
}
h3{font-size:19px;font-weight:700;margin:44px 0 14px;padding-top:18px;border-top:1px solid var(--border)}
h4{font-size:16px;font-weight:680;margin:28px 0 10px}
h5{font-size:14px;font-weight:680;margin:22px 0 8px;color:var(--ink-soft)}

.topic{margin:76px 0 0;padding-top:28px;border-top:2px solid var(--border-control)}
.topic .kicker{
  font-family:var(--mono);font-size:10px;text-transform:uppercase;
  letter-spacing:.17em;color:var(--action);margin:0 0 10px;
}

p{margin:0 0 17px}
a{color:var(--action);text-decoration-thickness:1px;text-underline-offset:2px}
strong{font-weight:640}
hr{border:0;height:1px;background:var(--border);margin:38px 0}

ul,ol{margin:0 0 18px;padding-left:22px}
li{margin-bottom:7px}
li::marker{color:var(--ink-faint)}
ul ul,ol ol,ul ol,ol ul{margin:7px 0 0}
ul.check{list-style:none;padding-left:0}
ul.check li{position:relative;padding-left:29px}
ul.check li span{
  position:absolute;left:0;top:.36em;width:15px;height:15px;
  border:1.5px solid var(--ink-faint);border-radius:4px;
}

blockquote{
  margin:22px 0;padding:15px 20px;background:var(--surface);
  border-left:3px solid var(--action);border-radius:0 var(--radius-sm) var(--radius-sm) 0;
}
blockquote p{margin:0 0 9px;font-size:16px;color:var(--ink-soft)}
blockquote p:last-child{margin:0}
blockquote em{color:var(--ink);font-style:italic}

.scroll{overflow-x:auto;margin:24px 0;-webkit-overflow-scrolling:touch}
table{
  border-collapse:collapse;width:100%;font-family:var(--sans);
  font-size:13.5px;line-height:1.5;font-variant-numeric:tabular-nums;
}
th{
  text-align:left;font-family:var(--mono);font-size:10px;font-weight:600;
  text-transform:uppercase;letter-spacing:.1em;color:var(--ink-faint);
  padding:0 14px 9px 0;border-bottom:1.5px solid var(--border-control);white-space:nowrap;
}
td{padding:11px 14px 11px 0;border-bottom:1px solid var(--border);vertical-align:top}
tr:last-child td{border-bottom:0}
td:first-child{color:var(--ink);font-weight:550}
table code{font-size:12px}

code{
  font-family:var(--mono);font-size:.86em;background:var(--surface-muted);
  padding:.14em .38em;border-radius:var(--radius-sm)
}
pre{
  margin:0;background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius-sm);padding:17px 19px;overflow-x:auto;
}
pre code{background:none;padding:0;font-size:12.5px;line-height:1.72;color:var(--ink-soft)}

header{padding:56px 0 8px;border-bottom:2px solid var(--border-control)}
.eyebrow{
  font-family:var(--mono);font-size:10.5px;text-transform:uppercase;
  letter-spacing:.19em;color:var(--action);margin:0 0 15px;
}
.lede{font-size:18px;color:var(--ink-soft);margin:16px 0 26px;max-width:60ch}
.stats{display:flex;flex-wrap:wrap;margin:0 0 28px;border-top:1px solid var(--border)}
.stat{padding:14px 28px 14px 0;margin-right:28px;border-right:1px solid var(--border)}
.stat:last-child{border-right:0;margin-right:0}
.stat b{
  display:block;font-family:var(--sans);font-size:24px;font-weight:730;
  letter-spacing:-.02em;font-variant-numeric:tabular-nums;line-height:1.1;
}
.stat span{
  display:block;font-family:var(--mono);font-size:9.5px;text-transform:uppercase;
  letter-spacing:.13em;color:var(--ink-faint);margin-top:4px;
}
footer{
  margin-top:64px;padding-top:22px;border-top:1px solid var(--border);
  font-family:var(--mono);font-size:11px;color:var(--ink-faint);line-height:1.7;
}
:focus-visible{outline:2px solid var(--focus);outline-offset:3px}
@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}

/* --- progresso de leitura (compartilhado: landing + guia individual) --- */
.lido-toggle{
  display:inline-flex;align-items:center;gap:8px;margin:18px 0 0;padding:9px 16px 9px 12px;
  font-family:var(--sans);font-size:13px;font-weight:600;color:var(--ink-soft);
  background:var(--surface);border:1.5px solid var(--border);border-radius:var(--radius-pill);cursor:pointer;
  transition:border-color var(--fast) var(--ease),color var(--fast) var(--ease),background var(--fast) var(--ease);
}
.lido-toggle:hover{border-color:var(--action);color:var(--ink)}
.lido-toggle .lido-toggle-icon{
  display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;
  border-radius:50%;border:1.5px solid var(--ink-faint);font-size:11px;line-height:1;
  color:transparent;transition:all var(--fast) var(--ease);
}
.lido-toggle.is-lido{background:var(--success-bg);border-color:var(--success);color:var(--success)}
.lido-toggle.is-lido .lido-toggle-icon{
  background:var(--success);border-color:var(--success);color:var(--surface);
}

/* --- marca --- */
h1.brand{display:flex;align-items:center;gap:14px;letter-spacing:.015em}
.brandmark{
  width:50px;height:50px;flex:none;border-radius:var(--radius-control);
  box-shadow:var(--shadow-soft);
}
@media(max-width:600px){.brandmark{width:40px;height:40px;border-radius:var(--radius-sm)}}
"""

# Favicon + apple-touch-icon; caminhos relativos ao próprio HTML (tudo mora em docs/).
# Inter é a font-sans do design system Cortex (tokens.json); Google Fonts evita
# empacotar o arquivo da fonte no repo.
HEAD_ICONS = """<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="cortex-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">"""

TRACKING_JS = """<script>
(function(){
  var LS_KEY = 'estudos-lidos-v1';
  function getLidos(){ try{ return JSON.parse(localStorage.getItem(LS_KEY)||'{}'); }catch(e){ return {}; } }
  function setLido(stem,val){
    var l=getLidos();
    if(val){ l[stem]=Date.now(); } else { delete l[stem]; }
    localStorage.setItem(LS_KEY, JSON.stringify(l));
    return l;
  }
  window.estudosLidos = {get:getLidos, set:setLido};
})();
</script>"""


def main():
    hub = (ROOT / "GUIA.md").read_text(encoding="utf-8")
    # O hub vira o sumário: fica só o bloco "Por onde começar" em diante.
    tail = hub.split("## Por onde começar", 1)[1]
    intro, _ = convert("## Por onde começar" + tail, "hub", base_level=0)

    sections, nav = [], []
    for stem, title, emoji, tag in TOPICS:
        text = (ROOT / "guias" / f"{stem}.md").read_text(encoding="utf-8")
        _, md = parse_frontmatter(text)
        body, subs = convert(md, stem, base_level=1)
        sections.append(
            f'<section class="topic" id="t-{stem}">'
            f'<p class="kicker">{emoji} {html.escape(tag)}</p>'
            f'<h2>{html.escape(title)}</h2>{body}</section>'
        )
        nav.append(
            f'<a href="#t-{stem}"><b>{html.escape(title)}</b>'
            f'<span>{html.escape(tag)}</span></a>'
            + "".join(f'<a class="sub" href="#{sid}">{html.escape(lbl)}</a>' for sid, lbl in subs[:7])
        )

    out = f"""<title>CORTEX</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
{HEAD_ICONS}
<style>{CSS}</style>
<div class="wrap">
<nav><p>Tópicos</p><a href="#topo"><b>Por onde começar</b></a>{"".join(nav)}</nav>
<main>
<header id="topo">
  <p class="eyebrow">Biblioteca de transcrições · Síntese operacional</p>
  <h1 class="brand"><img class="brandmark" src="cortex-icon.png" alt="">CORTEX</h1>
  <p class="lede">Agência de IA, ferramentas de IA, SaaS, low ticket, negócio solo, copy e
  e-commerce, Google Meu Negócio e a santidade na vida ordinária — destilados da leitura integral de 477
  transcrições de YouTube.</p>
  <div class="stats">
    <div class="stat"><b>477</b><span>vídeos lidos</span></div>
    <div class="stat"><b>223</b><span>canais</span></div>
    <div class="stat"><b>{len(TOPICS)}</b><span>grandes tópicos</span></div>
    <div class="stat"><b>7</b><span>números sem lastro</span></div>
  </div>
</header>
{intro}
{"".join(sections)}
<footer>
  Gerado de <code>GUIA.md</code> + <code>guias/*.md</code>. Cada afirmação é rastreável ao vídeo
  e timestamp em <code>references/youtube/</code>.<br>
  Transcrições automáticas — números e nomes de ferramentas podem conter erros.<br>
  <a href="index.html">← voltar para a lista de tópicos</a>
</footer>
</main>
</div>
"""
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "GUIA.html"
    dest.write_text(out, encoding="utf-8")
    print(f"{dest}  ({len(out):,} bytes, {len(TOPICS)} tópicos)")


if __name__ == "__main__":
    main()
