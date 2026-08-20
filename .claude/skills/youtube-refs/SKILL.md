---
name: youtube-refs
description: Build and extend the local YouTube transcript reference library under references/youtube/. Use this whenever the user drops YouTube links to "add to references", asks to transcribe or download subtitles for videos, wants to know which videos still need Whisper, or asks a study/research question that should be answered from the videos already collected ("what do these channels say about X", "find the part where they explain Y"). Also use it before hand-rolling any yt-dlp or mlx-whisper command against YouTube - the pipeline here already handles rate limits, language selection, and the index that tracks what has been fetched.
---

# YouTube reference library

Turns YouTube links into `references/youtube/{channel}/{video-title}.md` transcripts, tracked in a
single index so the collection can grow over months without re-downloading or losing track of gaps.

## Layout

```
references/youtube/
  urls.txt      # raw input, one link per line - append here, never edit entries in place
  index.json    # the database: one record per video id, keyed by id
  {channel}/{video-title}.md
```

`index.json` is the source of truth. Each record carries `status`, plus title/channel/duration/lang
and the `path` of the markdown once written:

| status | meaning | next step |
|---|---|---|
| `pending` | seeded, never fetched | `fetch` |
| `ok` | transcript written | nothing |
| `no_subs` | video genuinely has no captions | `whisper` |
| `error` | fetch failed (throttling, private, removed) | `fetch --retry-errors` |

The `no_subs` / `error` split matters: only `no_subs` means "YouTube has no captions for this".
Never let a throttled request get recorded as `no_subs`, or the video gets sent to Whisper (minutes
of GPU time) when a caption file was there all along.

## Workflow

```bash
S=.claude/skills/youtube-refs/scripts/yt_refs.py

# 1. add links (append to urls.txt first), then load them into the index
python3 $S seed

# 2. download captions - re-runnable, only touches pending records
python3 $S fetch --jobs 2

# 3. retry whatever failed, once YouTube's cooldown has passed
python3 $S fetch --retry-errors

# 4. transcribe locally the ones with no captions at all
python3 $S whisper

# 5. where things stand
python3 $S status
```

Every command is idempotent and saves the index after each video, so a batch that dies halfway
loses nothing - just run it again.

## Rate limiting

YouTube's caption endpoint (`timedtext`) throttles far more aggressively than metadata. Two rules
keep a large batch alive:

- **One caption track per video.** A glob like `--sub-langs "en.*,pt.*"` expands to every regional
  and auto-translated variant, so a single video makes ~5 caption requests and a batch of 20 videos
  earns a sticky 429 that lasts many minutes. The script reads the metadata first, picks exactly one
  language, and downloads only that.
- **Keep `--jobs` at 2 or below.** Higher concurrency triggers the same cooldown. It's not worth it:
  captions are small, and the batch is bounded by throttling, not bandwidth.

If a run does come back mostly `error` with 429s, the IP is in cooldown. Wait, then
`fetch --retry-errors` - don't escalate concurrency, and don't reach for `--cookies-from-browser`
by default, since hammering the caption endpoint with a signed-in session risks the account. That
flag exists for videos that genuinely require a login, not as a throttling workaround.

## Language choice

The original spoken language wins over the preference list, because YouTube's auto-translated tracks
are visibly worse than the original. `--langs en,pt` only breaks ties when the metadata doesn't say
what the original was. Manual (human) captions always beat auto ones. The chosen track is recorded
in each file's frontmatter as `lang` and `source`, so a later reader can judge how much to trust it.

One trap worth knowing on live streams and premieres: their `subtitles` table often contains only
`live_chat`, the chat-replay track. It looks like a manual caption track but is chat messages, and
yt-dlp writes it as `.live_chat.json` while ignoring `--sub-format`, so the run appears to succeed
and produces no transcript. The script excludes it and falls through to the real auto captions.

## Transcript format

Frontmatter holds the citable metadata; the body is the transcript in ~2-minute paragraphs, each
tagged with a timestamp so a claim can be traced back to the video:

```markdown
---
title: "..."
channel: "..."
url: "https://www.youtube.com/watch?v=..."
upload_date: "20260611"
duration: "00:28:22"
source: "yt-dlp auto captions"
lang: "pt-orig"
---

# ...

[00:00:00] first two minutes of speech...

[00:02:00] next chunk...
```

Auto captions arrive as a rolling window where each line repeats across two or three cues; the
script collapses those duplicates. Raw VTT is roughly 3x longer and unreadable, so don't store it.

## Answering questions from the library

These transcripts are speech, so they are long, informal, and have no headings - grepping for an
exact phrase usually fails. Search the index for the relevant channels/titles first, then read the
few files that plausibly cover the topic. When citing, use the timestamp and link the video, e.g.
`[00:14:30] in "<title>" (<url>)`, so the user can verify the claim in seconds.

Auto captions mangle names, numbers, and jargon. Treat a surprising figure as a transcription error
worth flagging rather than a fact, especially in non-English videos.

## Whisper pass

`whisper` downloads audio with yt-dlp, transcribes with `uvx mlx-whisper`, and writes the same
markdown shape. It's slow (roughly real-time/5 on Apple Silicon) and downloads full audio, so run it
only after `fetch` has taken everything it can, and expect a long unattended run. Override the model
with `--model` if the default (`mlx-community/whisper-large-v3-turbo`) is too heavy.

## Extending

`scripts/test_yt_refs.py` covers the parsing that isn't obvious - id extraction, VTT
de-duplication, language choice. Run `python3 test_yt_refs.py` from the scripts directory after
touching any of it; a silent regression there corrupts every transcript in the batch.
