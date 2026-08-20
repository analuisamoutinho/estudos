#!/usr/bin/env python3
"""Pull YouTube captions into references/youtube/{channel}/{video}.md, tracked in index.json.

  seed   urls.txt -> index.json (dedup by video id)
  fetch  yt-dlp captions -> markdown; marks entries needing whisper
  whisper  mlx-whisper local transcription for entries yt-dlp had no captions for
  status status counts
"""
import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ID_RE = re.compile(r"(?:v=|/live/|/shorts/|youtu\.be/)([A-Za-z0-9_-]{11})")
CUE_RE = re.compile(r"^((?:\d{2}:)?\d{2}:\d{2})\.\d{3}\s+-->")
TAG_RE = re.compile(r"<[^>]+>")
SKIP_PREFIX = ("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE", "REGION")
DB_LOCK = threading.Lock()


def video_id(url):
    m = ID_RE.search(url)
    return m.group(1) if m else None


def slug(text, limit=90):
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip()
    text = re.sub(r"[\s_]+", "-", text).strip("-").lower()
    if len(text) > limit:
        cut = text[:limit]
        boundary = cut.rfind("-")
        text = cut[:boundary] if boundary != -1 else cut
    return (text.rstrip("-") or "untitled")


def hms(ts):
    parts = [int(p) for p in ts.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def stamp(secs):
    return f"{secs // 3600:02d}:{secs % 3600 // 60:02d}:{secs % 60:02d}"


def vtt_to_text(raw, chunk_secs=120):
    """VTT -> timestamped paragraphs. Drops the rolling-window duplicate lines
    YouTube's auto captions emit (each line repeats in the next 2-3 cues)."""
    cues, cur, last = [], 0, None
    for line in raw.splitlines():
        m = CUE_RE.match(line.strip())
        if m:
            cur = hms(m.group(1))
            continue
        if not line.strip() or line.startswith(SKIP_PREFIX):
            continue
        text = html.unescape(TAG_RE.sub("", line)).replace(" ", " ").strip()
        if not text or text == last:
            continue
        last = text
        cues.append((cur, text))

    paras, buf, start = [], [], None
    for secs, text in cues:
        if start is not None and secs - start >= chunk_secs:
            paras.append(f"[{stamp(start)}] " + " ".join(buf))
            buf, start = [], None
        if start is None:
            start = secs
        buf.append(text)
    if buf:
        paras.append(f"[{stamp(start or 0)}] " + " ".join(buf))
    return "\n\n".join(paras)


def pick_lang(info, langs):
    """Exactly one caption track: the video's original language when known,
    else the first preferred one. Requesting `en.*,pt.*` instead pulls ~5 tracks
    per video and gets the caption endpoint to 429 within a handful of videos."""
    orig = info.get("language") or ""
    wanted = [f"{orig}-orig", orig] if orig else []
    wanted += [f"{l}-orig" for l in langs] + list(langs)
    seen, order = set(), []
    for w in wanted:
        if w and w not in seen:
            seen.add(w)
            order.append(w)

    for kind, table in (("manual", info.get("subtitles") or {}),
                        ("auto", info.get("automatic_captions") or {})):
        # live_chat is YouTube's chat-replay pseudo-track (live/premiere videos),
        # not spoken-word captions - yt-dlp writes it as .live_chat.json and
        # ignores --sub-format, so picking it here means "no .vtt ever appears".
        available = [k for k in table if table[k] and k != "live_chat"]
        for want in order:
            for have in available:
                if have == want or have.split("-")[0] == want:
                    return have, kind
        if kind == "manual" and available:
            return available[0], kind
    return None, None


def run(cmd, timeout=300):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def write_md(out_dir, entry, body, db):
    channel_dir = out_dir / slug(entry["channel"] or "unknown-channel", 60)
    channel_dir.mkdir(parents=True, exist_ok=True)
    name = slug(entry["title"])
    taken = {e.get("path") for e in db.values() if e["id"] != entry["id"]}
    path = channel_dir / f"{name}.md"
    if str(path) in taken:
        path = channel_dir / f"{name}-{entry['id']}.md"

    meta = {k: entry.get(k) for k in
            ("title", "channel", "channel_url", "id", "url", "upload_date",
             "duration", "source", "lang")}
    front = "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}"
                      for k, v in meta.items() if v not in (None, ""))
    path.write_text(f"---\n{front}\n---\n\n# {entry['title']}\n\n{body}\n", encoding="utf-8")
    return path


def yt(args, cookies, timeout=300):
    cmd = ["yt-dlp", "--no-warnings"] + (["--cookies-from-browser", cookies] if cookies else []) + args
    return run(cmd, timeout)


PROGRESS_RE = re.compile(r"^\[download]\s+[\d.]+%")


def last_error(res, default="unknown"):
    """Last meaningful yt-dlp output line - never a `[download] NN%` progress
    line, which is what a stalled/wrong download leaves behind on exit 0."""
    lines = [l.strip() for l in (res.stderr or res.stdout or "").strip().splitlines() if l.strip()]
    for l in reversed(lines):
        if "ERROR" in l or "WARNING" in l:
            return l[:300]
    for l in reversed(lines):
        if not PROGRESS_RE.match(l):
            return l[:300]
    return (lines[-1] if lines else default)[:300]


def fetch_one(entry, out_dir, db, langs, cookies, sleep=1, attempts=4):
    vid = entry["id"]
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        res = yt(["--skip-download", "--write-info-json", "-o", str(tmp / "%(id)s"),
                  entry["url"]], cookies)
        info_file = tmp / f"{vid}.info.json"
        if not info_file.exists():
            return {**entry, "status": "error", "error": last_error(res)}

        info = json.loads(info_file.read_text(encoding="utf-8"))
        secs = int(info.get("duration") or 0)
        entry = {**entry,
                 "title": info.get("title") or vid,
                 "channel": info.get("channel") or info.get("uploader") or "unknown-channel",
                 "channel_url": info.get("channel_url") or "",
                 "upload_date": info.get("upload_date") or "",
                 "duration": stamp(secs),
                 "duration_secs": secs}

        lang, kind = pick_lang(info, langs)
        if not lang:
            return {**entry, "status": "no_subs", "error": "", "note": "needs mlx-whisper"}

        err = "unknown"
        for attempt in range(attempts):
            res = yt(["--skip-download", "--write-subs", "--write-auto-subs",
                      "--sub-langs", lang, "--sub-format", "vtt",
                      "--sleep-requests", str(sleep),
                      "-o", str(tmp / "%(id)s"), entry["url"]], cookies)
            sub = next(iter(tmp.glob(f"{vid}.*.vtt")), None)
            if sub:
                break
            # 429 here means "throttled", never "no captions" - that distinction
            # decides whether the video gets handed to whisper.
            err = last_error(res)
            if attempt < attempts - 1:
                time.sleep(45 * (attempt + 1))
        else:
            return {**entry, "status": "error", "error": err}

        body = vtt_to_text(sub.read_text(encoding="utf-8"))
        if not body.strip():
            return {**entry, "status": "no_subs", "note": "empty caption file"}
        entry = {**entry, "lang": lang, "source": f"yt-dlp {kind} captions"}
        path = write_md(out_dir, entry, body, db)
        return {**entry, "status": "ok", "error": "",
                "path": str(path), "chars": len(body)}


def whisper_one(entry, out_dir, db, model, cookies):
    vid = entry["id"]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cmd = ["yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "mp3",
               "--no-warnings", "-o", str(tmp / "%(id)s.%(ext)s"), entry["url"]]
        if cookies:
            cmd[1:1] = ["--cookies-from-browser", cookies]
        res = run(cmd, timeout=3600)
        audio = next(iter(tmp.glob(f"{vid}.mp3")), None)
        if not audio:
            err = (res.stderr or "audio download failed").strip().splitlines()
            return {**entry, "status": "error", "error": err[-1][:300]}

        res = run(["uvx", "mlx-whisper", str(audio), "--model", model,
                   "--output-format", "vtt", "--output-dir", str(tmp)], timeout=7200)
        vtt = next(iter(tmp.glob("*.vtt")), None)
        if not vtt:
            err = (res.stderr or "mlx-whisper failed").strip().splitlines()
            return {**entry, "status": "error", "error": err[-1][:300]}

        body = vtt_to_text(vtt.read_text(encoding="utf-8"))
        entry = {**entry, "source": f"mlx-whisper ({model})"}
        path = write_md(out_dir, entry, body, db)
        return {**entry, "status": "ok", "error": "",
                "path": str(path), "chars": len(body)}


def load_db(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def save_db(path, db):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(db, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    tmp.replace(path)


def cmd_seed(args, db):
    added = 0
    for line in Path(args.urls).read_text().splitlines():
        url = line.strip()
        if not url or url.startswith("#"):
            continue
        vid = video_id(url)
        if not vid:
            print(f"! unparseable: {url}", file=sys.stderr)
            continue
        if vid not in db:
            db[vid] = {"id": vid, "url": f"https://www.youtube.com/watch?v={vid}",
                       "status": "pending", "title": "", "channel": ""}
            added += 1
    save_db(Path(args.db), db)
    print(f"seeded {added} new, {len(db)} total")


def cmd_run(args, db, worker, statuses):
    todo = [e for e in db.values() if e["status"] in statuses]
    if args.limit:
        todo = todo[:args.limit]
    if not todo:
        print("nothing to do")
        return
    out_dir = Path(args.out)
    done = [0]

    def work(entry):
        try:
            result = worker(entry)
        except Exception as exc:  # noqa: BLE001 - one bad video must not kill the batch
            result = {**entry, "status": "error", "error": f"{type(exc).__name__}: {exc}"[:300]}
        with DB_LOCK:
            db[entry["id"]] = result
            save_db(Path(args.db), db)
            done[0] += 1
            flag = {"ok": "+", "no_subs": "~", "error": "x"}.get(result["status"], "?")
            print(f"[{done[0]}/{len(todo)}] {flag} {result['status']:8} "
                  f"{(result.get('channel') or '?')[:28]:28} {(result.get('title') or entry['id'])[:60]}",
                  flush=True)

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        list(pool.map(work, todo))
    cmd_status(args, db)


def cmd_status(args, db):
    counts = {}
    for e in db.values():
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    print("  ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "empty")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["seed", "fetch", "whisper", "status"])
    p.add_argument("--db", default="references/youtube/index.json")
    p.add_argument("--urls", default="references/youtube/urls.txt")
    p.add_argument("--out", default="references/youtube")
    p.add_argument("--langs", default="en,pt", help="preferred caption languages")
    p.add_argument("--jobs", type=int, default=2)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--sleep", type=float, default=1, help="yt-dlp --sleep-requests")
    p.add_argument("--model", default="mlx-community/whisper-large-v3-turbo")
    p.add_argument("--cookies-from-browser", dest="cookies", default=None,
                   help="pass to yt-dlp if YouTube demands sign-in")
    p.add_argument("--retry-errors", action="store_true")
    args = p.parse_args()

    if not shutil.which("yt-dlp"):
        sys.exit("yt-dlp not found")
    db = load_db(Path(args.db))
    langs = [l.strip() for l in args.langs.split(",") if l.strip()]

    if args.command == "seed":
        cmd_seed(args, db)
    elif args.command == "status":
        cmd_status(args, db)
    elif args.command == "fetch":
        statuses = {"pending", "error"} if args.retry_errors else {"pending"}
        cmd_run(args, db, lambda e: fetch_one(e, Path(args.out), db, langs, args.cookies, args.sleep),
                statuses)
    else:
        statuses = {"no_subs", "error"} if args.retry_errors else {"no_subs"}
        cmd_run(args, db, lambda e: whisper_one(e, Path(args.out), db, args.model, args.cookies),
                statuses)


if __name__ == "__main__":
    main()
