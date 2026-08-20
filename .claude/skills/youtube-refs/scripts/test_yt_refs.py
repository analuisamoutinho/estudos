#!/usr/bin/env python3
"""Self-check: python3 test_yt_refs.py"""
from types import SimpleNamespace

from yt_refs import last_error, pick_lang, slug, video_id, vtt_to_text

assert video_id("https://www.youtube.com/live/UpBR4InLuzU") == "UpBR4InLuzU"
assert video_id("https://www.youtube.com/watch?v=hXQSniTGhmw&list=PL7ty") == "hXQSniTGhmw"
assert video_id("https://youtu.be/-FvX81leJpc") == "-FvX81leJpc"
assert video_id("https://example.com/nope") is None

assert slug("Claude Code: 10x Your Workflow!") == "claude-code-10x-your-workflow"
assert slug("///") == "untitled"

# Truncation must land on a word boundary, never mid-word, never end in "-".
long_title = "Aula 13 - Como criar um produto na Kirvano e configurar no Typebot Curso Low Ticket Gratuito"
assert slug(long_title) == "aula-13---como-criar-um-produto-na-kirvano-e-configurar-no-typebot-curso-low-ticket"
assert len(slug(long_title)) <= 90

# Single word longer than the limit has no separator to cut back to: keep a
# hard cut rather than collapsing to "untitled", and never end in "-".
one_word_slug = slug("a" * 120)
assert len(one_word_slug) == 90, one_word_slug
assert one_word_slug == "a" * 90, one_word_slug
assert not one_word_slug.endswith("-"), one_word_slug

# YouTube auto-caption rolling window: each line re-emitted in the next cues.
VTT = """WEBVTT
Kind: captions
Language: en

00:00:01.000 --> 00:00:03.000 align:start position:0%
hello<00:00:01.500><c> there</c>

00:00:03.000 --> 00:00:05.000 align:start position:0%
hello there
this is<00:00:03.900><c> a test</c>

00:00:05.000 --> 00:00:07.000 align:start position:0%
this is a test

00:02:30.000 --> 00:02:33.000 align:start position:0%
&amp; later on
"""
out = vtt_to_text(VTT, chunk_secs=120)
assert out.startswith("[00:00:01] hello there this is a test"), out
assert "hello there hello there" not in out, "rolling duplicates not collapsed"
assert "\n\n[00:02:30] & later on" in out, out

# Original language wins over the preference list; one track only.
auto = {"pt-orig": [1], "pt": [1], "en": [1], "es": [1]}
assert pick_lang({"language": "pt", "automatic_captions": auto}, ["en", "pt"]) == ("pt-orig", "auto")
assert pick_lang({"automatic_captions": {"en": [1], "de": [1]}}, ["en"]) == ("en", "auto")
# Manual captions beat auto ones, even in a non-preferred language.
assert pick_lang({"subtitles": {"en": [1]}, "automatic_captions": auto}, ["pt"]) == ("en", "manual")
# Empty track lists are not captions.
assert pick_lang({"automatic_captions": {"en": []}}, ["en"]) == (None, None)
assert pick_lang({}, ["en"]) == (None, None)

# live_chat (chat-replay pseudo-track on live/premiere videos) is never real
# captions - must fall through to auto captions, not get picked as "manual".
assert pick_lang({"language": "pt", "subtitles": {"live_chat": [1]},
                   "automatic_captions": {"pt-orig": [1], "pt": [1]}},
                  ["en", "pt"]) == ("pt-orig", "auto")
assert pick_lang({"subtitles": {"live_chat": [1]}}, ["en"]) == (None, None)

# last_error: skip [download] progress lines, prefer ERROR/WARNING.
progress_only = SimpleNamespace(stderr="", stdout=(
    "[youtube] Extracting URL\n"
    "[download] Destination: x.live_chat.json\n"
    "[download]  50.0% of 4.43KiB\n"
    "[download] 100% of 4.43KiB in 00:00:01 at 2.52KiB/s\n"))
assert last_error(progress_only) == "[download] Destination: x.live_chat.json"

with_error = SimpleNamespace(stderr=(
    "[download]  50.0% of 4.43KiB\n"
    "ERROR: Sign in to confirm your age\n"), stdout="")
assert last_error(with_error) == "ERROR: Sign in to confirm your age"

print("ok")
