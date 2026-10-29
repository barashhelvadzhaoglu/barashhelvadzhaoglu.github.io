#!/usr/bin/env python3
"""
translate_missing.py — barashhelvadzhaoglu.com eksik çevirileri Gemini ile tamamlar.
(LebenInsider'daki script'in bu siteye uyarlanmış hali.)

Mantık
- Bu sitede çeviriler AYNI DOSYA ADIYLA eşleşir: content/en/technology/x.md <-> content/de/technology/x.md.
  Bu yüzden anahtar = "<bölüm>/<dosya>.md" (ör. technology/cisco-sd-wan.md).
- Yalnızca architecture, technology ve posts bölümleri çevrilir (_index, about, contact, search hariç).
- Bir yazının eksik olduğu her dil için en iyi kaynaktan (önce EN, sonra TR, sonra DE) çeviri üretilir.
- Hedef dosya aynı bölüm ve aynı dosya adıyla yazılır, URL slug'ı değişmez (Hugo hreflang eşleşmesi korunur).
- Kaynaktaki aliases içinde HEDEF DİLE ait olanlar (ör. /tr/...) hedef dosyaya taşınır ve kaynaktan silinir.
  Hedefin kendi URL'sine eşit olan alias atılır. Diğer aliases kaynakta kalır.
- Site içi linkler, varsa hedef dildeki karşılığına çevrilir.
- Kategoriler, mevcut çevrilmiş yazılardan öğrenilen eşleşmeyle hedef dile çevrilir.
- Yeni çeviriler ileri tarihli yazılır: her dilde günde en fazla 1 yazı yayına girer.
  (deploy.yml her gece build alıyor, buildFuture kapalı.)
- Bitince yalnızca yeni/değişen dosyaları commit+push eder ve iMessage ile rapor atar.

Kullanım
  python3 script/translate_missing.py --dry-run     # ne yapılacağını göster
  python3 script/translate_missing.py --limit 5     # 5 çeviri yap
  python3 script/translate_missing.py --no-push     # commit et ama push etme
  python3 script/translate_missing.py --key technology/cisco-sd-wan.md

Atlanacak yazılar: script/translate_skip.txt (her satırda bir anahtar; * joker desteklenir)
Hemen yayınlanacaklar: script/translate_priority.txt (sıraya girmez, tarih = şimdi)
API anahtarları: .env içinde GEMINI_API_KEY_1, GEMINI_API_KEY_2 ...
  .env yoksa ~/lebeninsider/.env okunur.
"""

import argparse, fnmatch, json, os, re, subprocess, sys, time, unicodedata, urllib.request, urllib.error
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SKIP_FILE = ROOT / "script" / "translate_skip.txt"
PRIORITY_FILE = ROOT / "script" / "translate_priority.txt"
STATE_FILE = ROOT / "script" / "translate_state.json"
LOG_FILE = ROOT / "script" / "translate_missing.log"
ENV_FILES = [ROOT / ".env", ROOT.parent / "lebeninsider" / ".env"]

LANGS = ["en", "de", "tr"]
SOURCE_PRIORITY = ["en", "tr", "de"]
LANG_NAMES = {"en": "English", "de": "German", "tr": "Turkish"}
SECTIONS = ["architecture", "technology", "posts"]
SKIP_NAMES = {"_index.md", "index.md", "search.md"}

MODELS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-3-flash",
          "gemini-2.5-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-2.5-flash-lite"]
DELAY = 13            # ücretsiz katman ~5 istek/dk
MAX_SOURCE_BYTES = 120_000
MAX_FAILS = 3
IMESSAGE_TARGET = "baris.helvacioglu@outlook.com"
SITE = "barashhelvadzhaoglu.com"

GAP_DAYS = 1                 # her dilde günde en fazla 1 yeni yazı
PUBLISH_CLOCK = "00:30:00"   # gece 01:30 UTC build'inden önce olsun ki o gün yayına girsin


def log(msg):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ── Yardımcılar ──────────────────────────────────────────────────────────────

def nfc(s): return unicodedata.normalize("NFC", s)

def load_keys():
    keys = []
    for env in ENV_FILES:
        if not env.exists():
            continue
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY") and "=" in line:
                v = line.split("=", 1)[1].strip().strip('"').strip("'")
                keys += [k.strip() for k in v.split(",") if len(k.strip()) > 10 and k.strip() not in keys]
        if keys:
            break
    for i in range(1, 10):
        v = os.environ.get(f"GEMINI_API_KEY_{i}", "")
        if len(v) > 10 and v not in keys:
            keys.append(v)
    return keys

def split_fm(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    return text[4:end], text[end + 4:].lstrip("\n")

def fm_get(fm, field):
    m = re.search(rf'^{field}:\s*"?([^"\n]*)"?\s*$', fm or "", re.M)
    return m.group(1).strip() if m else None

def fm_aliases(fm):
    if not fm or not re.search(r"^aliases:", fm, re.M):
        return []
    block = re.search(r"^aliases:\s*\n((?:[ \t]+-.*\n?)*)", fm + "\n", re.M)
    if block:
        return re.findall(r'^\s*-\s*"?([^"\n]+?)"?\s*$', block.group(1), re.M)
    inline = re.search(r"^aliases:\s*\[(.*)\]\s*$", fm, re.M)
    if inline:
        return [a.strip().strip('"\'') for a in inline.group(1).split(",") if a.strip()]
    return []

def fm_strip_aliases(fm):
    fm = re.sub(r"^aliases:\s*\n(?:[ \t]+-.*\n?)*", "", fm + "\n", flags=re.M).rstrip("\n")
    return re.sub(r"^aliases:.*\n?", "", fm, flags=re.M).rstrip("\n")

def fm_set_aliases(fm, aliases):
    fm = fm_strip_aliases(fm)
    if aliases:
        fm += "\naliases:\n" + "\n".join(f'  - "{a}"' for a in aliases)
    return fm

def url_of(lang, key):
    section, name = key.split("/", 1)
    return f"/{lang}/{section}/{name[:-3]}/".lower()


# ── İçerik envanteri ─────────────────────────────────────────────────────────

LAST_DATE = {}

def scan():
    posts = {}   # key -> {lang: Path}
    for lang in LANGS:
        for section in SECTIONS:
            folder = CONTENT / lang / section
            if not folder.exists():
                continue
            for p in folder.glob("*.md"):
                if p.name in SKIP_NAMES:
                    continue
                text = p.read_text(encoding="utf-8", errors="replace")
                fm, _ = split_fm(text)
                d = fm_get(fm, "date")
                if d and re.match(r"\d{4}-\d{2}-\d{2}", d) and fm_get(fm, "draft") != "true":
                    dd = date.fromisoformat(d[:10])
                    if dd > LAST_DATE.get(lang, date.min):
                        LAST_DATE[lang] = dd
                posts.setdefault(f"{section}/{nfc(p.name)}", {})[lang] = p
    return posts

def learn_categories(posts):
    """Mevcut çevirilerden kategori satırı eşleşmesini öğren: (kaynak dil, hedef dil, satır) -> satır."""
    votes = defaultdict(Counter)
    for have in posts.values():
        lines = {}
        for lang, p in have.items():
            fm, _ = split_fm(p.read_text(encoding="utf-8", errors="replace"))
            m = re.search(r"^categories:.*$", fm or "", re.M)
            if m:
                lines[lang] = m.group(0)
        for a, la in lines.items():
            for b, lb in lines.items():
                if a != b:
                    votes[(a, b, la)][lb] += 1
    return {k: c.most_common(1)[0][0] for k, c in votes.items()}

def next_publish_date(lang):
    base = max(LAST_DATE.get(lang, date.today()), date.today())
    d = base + timedelta(days=GAP_DAYS)
    LAST_DATE[lang] = d
    return publish_stamp(d)

def publish_stamp(d):
    tz = datetime.now().astimezone().strftime("%z")
    return f"{d.isoformat()}T{PUBLISH_CLOCK}{tz[:3]}:{tz[3:]}"

def now_stamp():
    return datetime.now().astimezone().replace(microsecond=0).isoformat()

def load_list(path):
    if not path.exists():
        return []
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.strip().startswith("#")]

def matches(key, pats):
    return any(fnmatch.fnmatch(key, p) for p in pats)

def load_state():
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"fails": {}}

def save_state(st):
    STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Gemini ───────────────────────────────────────────────────────────────────

class QuotaExhausted(Exception):
    pass

class NetworkDown(Exception):
    pass

dead_models = set()
exhausted = set()

def gemini(prompt, keys):
    for model in MODELS:
        if model in dead_models:
            continue
        for ki, key in enumerate(keys):
            if (model, ki) in exhausted:
                continue
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                               "generationConfig": {"temperature": 0.2, "maxOutputTokens": 65536}}).encode()
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    data = json.loads(r.read())
                parts = data["candidates"][0]["content"]["parts"]
                text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
                if data["candidates"][0].get("finishReason") == "MAX_TOKENS":
                    raise ValueError("cikti kesildi (MAX_TOKENS)")
                time.sleep(DELAY)
                return text.strip(), model
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    log(f"   kota doldu: {model} key#{ki+1}")
                    exhausted.add((model, ki))
                elif e.code == 404:
                    dead_models.add(model)
                    break
                elif e.code == 503:
                    log(f"   {model} su an yogun, sonraki modele geciliyor")
                    break
                else:
                    log(f"   HTTP {e.code} {model} key#{ki+1}: {e.read()[:150]!r}")
                    time.sleep(DELAY)
            except urllib.error.URLError as e:
                raise NetworkDown(f"Gemini'ye baglanilamadi: {e.reason}")
            except Exception as e:
                log(f"   hata {model} key#{ki+1}: {str(e)[:150]}")
                time.sleep(DELAY)
    raise QuotaExhausted("tum model/anahtar kombinasyonlari tukendi")


STYLE = {
    "de": "Use the formal 'Sie'. Use standard German IT terminology; keep established English terms "
          "(Switch, Firewall, Load Balancer, Upgrade, Failover) where German engineers use them.",
    "tr": "Write natural, professional Turkish as Turkish network engineers write it. Keep established English "
          "terms (switch, firewall, load balancer, upgrade, failover, policy) where Turkish engineers use them.",
    "en": "Write clear, professional technical English.",
}

def build_prompt(src_lang, tgt_lang, text):
    return f"""You translate articles for {SITE}, the professional blog of a senior network security engineer
in Munich (enterprise networking, Cisco, Fortinet, Palo Alto, F5, Aruba, SD-WAN, security architecture).

Translate this Hugo Markdown file from {LANG_NAMES[src_lang]} to {LANG_NAMES[tgt_lang]}.

Rules:
- Output ONLY the Markdown file, starting with ---. No explanations, no code fences around the file.
- Keep the author's voice and technical depth. Do not add content, sections, FAQs or claims. Do not shorten.
- {STYLE[tgt_lang]}
- Front matter: translate only the values of title, seoTitle, description, summary, tags, keywords and cover alt.
  Keep every other field (date, draft, cover image, showToc, TocOpen, aliases, categories) exactly as-is.
- Never translate: CLI commands, configuration snippets, code blocks, file names, URLs, product and feature
  names (Catalyst SD-WAN, vManage, EdgeConnect, Prisma SD-WAN, FortiGate, BIG-IP, ISE ...), protocol names
  and acronyms (OSPF, BGP, TLOC, OMP, IPsec, VRF ...).
- Keep all Markdown formatting, tables, lists, headings levels, Hugo shortcodes like {{{{< figure ... >}}}} and image paths exactly.
- In links [text](url) translate the text, never change the url.

FILE:
{text}"""


# ── Bir çeviriyi üret ────────────────────────────────────────────────────────

def postprocess(out, src_text, key, src_lang, tgt_lang, posts, cat_map, pub_date):
    out = re.sub(r"^```[a-z]*\n|\n```\s*$", "", out.strip())
    if not out.startswith("---"):
        i = out.find("---")
        if i < 0:
            raise ValueError("front matter yok")
        out = out[i:]
    fm, body = split_fm(out)
    if fm is None:
        raise ValueError("front matter kapanmamis")
    sfm, sbody = split_fm(src_text)

    # zorunlu alanlar kaynaktan
    for field in ("draft", "date"):
        v = fm_get(sfm, field)
        if v is None:
            continue
        if field == "date" and pub_date:
            v = pub_date
        if re.search(rf"^{field}:", fm, re.M):
            fm = re.sub(rf"^{field}:.*$", f"{field}: {v}", fm, count=1, flags=re.M)
        else:
            fm += f"\n{field}: {v}"

    # kategoriler: öğrenilmiş eşleşme
    m = re.search(r"^categories:.*$", sfm or "", re.M)
    if m and (src_lang, tgt_lang, m.group(0)) in cat_map:
        new = cat_map[(src_lang, tgt_lang, m.group(0))]
        if re.search(r"^categories:.*$", fm, re.M):
            fm = re.sub(r"^categories:.*$", new, fm, count=1, flags=re.M)
        else:
            fm += "\n" + new

    # aliases: yalnızca hedef dile ait olanlar, hedefin kendi URL'si hariç
    own = url_of(tgt_lang, key)
    moved = [a for a in fm_aliases(sfm) if a.lower().startswith(f"/{tgt_lang}/") and a.lower() != own]
    fm = fm_set_aliases(fm, moved)

    if len(body) < 0.5 * len(sbody):
        raise ValueError(f"ceviri cok kisa ({len(body)} / {len(sbody)})")

    # site içi linkler
    def fix(m):
        pre, lang, section, name, post = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        k = f"{section}/{name}.md"
        if tgt_lang in posts.get(k, {}):
            return f"{pre}/{tgt_lang}/{section}/{name}/{post}"
        return m.group(0)
    body = re.sub(r"(\]\((?:https?://(?:www\.)?barashhelvadzhaoglu\.com)?)/(en|de|tr)/(architecture|technology|posts)/([^/)\s#?]+)/?([^)]*\))",
                  fix, body)
    return f"---\n{fm.strip()}\n---\n\n{body.strip()}\n"

def remove_aliases_from_source(src_path, tgt_lang, key):
    """Hedef dile taşınan aliases'ı kaynak dosyadan sil. Değiştiyse True."""
    text = src_path.read_text(encoding="utf-8")
    fm, body = split_fm(text)
    al = fm_aliases(fm)
    keep = [a for a in al if not a.lower().startswith(f"/{tgt_lang}/")]
    if keep == al:
        return False
    src_path.write_text(f"---\n{fm_set_aliases(fm, keep).strip()}\n---\n\n{body}", encoding="utf-8")
    return True


def run(args):
    keys = load_keys()
    if not keys and not args.dry_run:
        log("API anahtari bulunamadi (.env GEMINI_API_KEY_1...)"); sys.exit(1)
    posts = scan()
    cat_map = learn_categories(posts)
    skip = load_list(SKIP_FILE)
    prio = load_list(PRIORITY_FILE)
    state = load_state()

    jobs = []
    for key, have in posts.items():
        if args.key and key != args.key:
            continue
        if matches(key, skip) and not args.key:
            continue
        src_lang = next(l for l in SOURCE_PRIORITY if l in have)
        src = have[src_lang]
        if fm_get(split_fm(src.read_text(encoding="utf-8"))[0], "draft") == "true":
            continue
        if src.stat().st_size > MAX_SOURCE_BYTES:
            log(f"atlandi (kaynak cok buyuk {src.stat().st_size//1024}KB): {src}")
            continue
        for tl in LANGS:
            if tl in have or state["fails"].get(f"{key}:{tl}", 0) >= MAX_FAILS:
                continue
            urgent = matches(key, prio)
            jobs.append(((0 if urgent else 1, SOURCE_PRIORITY.index(src_lang), key), key, src_lang, src, tl))
    jobs.sort(key=lambda j: j[0])
    log(f"Eksik ceviri: {len(jobs)} | Bu calismada en fazla: {args.limit} | Anahtar: {len(keys)}")

    if args.dry_run:
        for _, key, sl, src, tl in jobs[:args.limit]:
            pub = now_stamp() if matches(key, prio) else next_publish_date(tl)
            print(f"  {key:55s} {sl}->{tl}  yayin: {pub[:16]}")
        return [], len(jobs)

    changed = []
    created = 0
    for _, key, sl, src, tl in jobs[:args.limit]:
        src_text = src.read_text(encoding="utf-8")
        log(f"-> {key}: {sl} -> {tl}")
        try:
            out, model = gemini(build_prompt(sl, tl, src_text), keys)
            pub = now_stamp() if matches(key, prio) else next_publish_date(tl)
            final = postprocess(out, src_text, key, sl, tl, posts, cat_map, pub)
            section, name = key.split("/", 1)
            dest = CONTENT / tl / section / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(final, encoding="utf-8")
            posts[key][tl] = dest
            changed.append(dest)
            created += 1
            if remove_aliases_from_source(src, tl, key):
                changed.append(src)
            log(f"   OK {dest.relative_to(ROOT)} ({model}) yayin: {pub[:10]}")
        except QuotaExhausted:
            log("   Gunluk kota bitti, duruluyor.")
            break
        except NetworkDown as e:
            log(f"   {e} - duruluyor.")
            break
        except Exception as e:
            state["fails"][f"{key}:{tl}"] = state["fails"].get(f"{key}:{tl}", 0) + 1
            log(f"   HATA {e}")
    save_state(state)
    return changed, created, len(jobs) - created


def git_publish(paths, created, push=True):
    if not paths:
        return "degisiklik yok"
    rel = sorted({str(p.relative_to(ROOT)) for p in paths})
    def g(*a):
        r = subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    ok, out = g("add", "--", *rel)
    if not ok: return f"git add hatasi: {out[:150]}"
    ok, out = g("commit", "-m", f"content: {created} otomatik ceviri", "--only", "--", *rel)
    if not ok: return f"git commit hatasi: {out[:150]}"
    if not push: return "commit edildi (push yok)"
    ok, out = g("push")
    return "push edildi" if ok else f"git push hatasi: {out[:150]}"


def imessage(text):
    safe = text.replace("\\", "\\\\").replace('"', '\\"')
    script = (f'tell application "Messages"\n set s to 1st service whose service type = iMessage\n'
              f' send "{safe}" to buddy "{IMESSAGE_TARGET}" of s\nend tell')
    subprocess.run(["osascript", "-e", script], capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--no-git", action="store_true")
    ap.add_argument("--no-notify", action="store_true")
    ap.add_argument("--key")
    args = ap.parse_args()
    os.chdir(ROOT)
    log("=" * 50 + " barashhelvadzhaoglu.com ceviri")
    if args.dry_run:
        run(args)
        return
    changed, created, remaining = run(args)
    git_msg = "git atlandi" if args.no_git else git_publish(changed, created, push=not args.no_push)
    log(f"Bitti: {created} yeni ceviri, {remaining} eksik kaldi - {git_msg}")
    if not args.no_notify and (created or remaining):
        lines = [f"🌍 barashhelvadzhaoglu.com Çeviri — {datetime.now():%d.%m.%Y}",
                 f"✅ {created} yeni çeviri · ⏳ {remaining} eksik kaldı", f"📦 {git_msg}"]
        lines += [f"• {p.relative_to(CONTENT)}" for p in changed[:10]]
        imessage("\n".join(lines))


if __name__ == "__main__":
    main()
