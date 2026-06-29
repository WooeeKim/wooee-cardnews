#!/usr/bin/env python3
"""EX-RAY 리포트 미리보기 카드뉴스 (8장) — 정적 / 광고용 / 기능 나열형.

스토리(exray-intro)와 달리 '리포트가 어떻게 생겼는지'를 목업 UI로 보여준다.
- 목차, 카톡 원문 인용 근거, 관계 7단계 타임라인, 정량 지표 바,
  재회 가능성 게이지, 다음 연애 가이드 카드.
- 크림 라이트 + 핑크 브랜드 토큰은 exray-intro와 공유.
- 결합 HTML + 슬라이드별 PNG + 편집기 HTML 생성.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# --- 테마 (EX-RAY / 크림 라이트 + 핑크) --------------------------------------
BG = "#fff8ef"
ACCENT = "#ff2e63"
ANSWER_TEXT = "#ffffff"
INK = "#0d0d0d"
INK_RGB = "13,13,13"
PRETENDARD = ("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/"
              "dist/web/static/pretendard.css")

CSS = f"""*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Pretendard',sans-serif;}}
.slide{{width:1080px;height:1350px;color:{INK};position:relative;overflow:hidden;
  background-color:{BG};
  background-image:radial-gradient(rgba({INK_RGB},0.05) 1px, transparent 1.5px);
  background-size:30px 30px;}}
.slide h1,.slide h2,.slide p,.slide span,.slide div{{word-break:keep-all;}}
.brand{{position:absolute;left:80px;top:72px;font-size:34px;font-weight:800;letter-spacing:-0.5px;}}
.brand span{{color:{ACCENT};}}
.counter{{position:absolute;left:80px;bottom:62px;font-size:27px;font-weight:600;
  line-height:1;letter-spacing:1px;color:rgba({INK_RGB},0.30);}}
.kicker{{position:absolute;left:80px;font-size:25px;font-weight:800;letter-spacing:2px;
  color:{ACCENT};}}
.h{{position:absolute;left:80px;width:920px;font-weight:800;color:{INK};
  letter-spacing:-1px;line-height:1.22;}}
.note{{position:absolute;left:80px;width:920px;font-size:29px;line-height:1.7;
  color:rgba({INK_RGB},0.55);}}
.cta{{position:absolute;left:80px;font-size:36px;font-weight:700;color:{ACCENT};}}
/* 리포트 패널(흰 카드) */
.panel{{position:absolute;left:80px;width:920px;background:#fff;
  border:1px solid rgba({INK_RGB},0.08);border-radius:30px;
  box-shadow:0 16px 38px rgba(0,0,0,0.06);padding:46px 48px;}}
.plab{{font-size:23px;font-weight:800;letter-spacing:1px;color:rgba({INK_RGB},0.4);
  margin-bottom:24px;}}
/* 목차 */
.toc-row{{display:flex;align-items:center;gap:28px;padding:21px 0;
  border-bottom:1px solid rgba({INK_RGB},0.07);}}
.toc-row.last{{border-bottom:0;padding-bottom:0;}}
.toc-row.first{{padding-top:0;}}
.toc-num{{font-size:25px;font-weight:800;color:{ACCENT};width:42px;flex:none;}}
.toc-title{{font-size:31px;font-weight:600;color:{INK};}}
/* 인용 */
.quote{{font-size:33px;line-height:1.5;color:{INK};font-weight:600;}}
.quote-meta{{font-size:24px;color:rgba({INK_RGB},0.4);margin-top:18px;}}
.verdict{{font-size:30px;line-height:1.55;color:rgba({INK_RGB},0.75);}}
.verdict b{{color:{ACCENT};font-weight:800;}}
/* 정량 지표 바 */
.stat{{margin-bottom:30px;}}
.stat.last{{margin-bottom:0;}}
.stat-top{{display:flex;justify-content:space-between;align-items:baseline;
  font-size:28px;margin-bottom:13px;}}
.stat-label{{color:rgba({INK_RGB},0.6);font-weight:600;}}
.stat-val{{color:{INK};font-weight:800;}}
.bar{{height:18px;border-radius:999px;background:rgba({INK_RGB},0.08);overflow:hidden;}}
.bar > i{{display:block;height:100%;border-radius:999px;background:{ACCENT};}}
/* 타임라인 */
.tl-wrap{{position:relative;margin-top:66px;}}
.tl-line{{position:absolute;top:13px;left:7%;right:7%;height:3px;
  background:rgba({INK_RGB},0.13);}}
.tl{{display:flex;position:relative;}}
.tl-cell{{flex:1;display:flex;flex-direction:column;align-items:center;gap:20px;}}
.tl-dot{{width:28px;height:28px;border-radius:50%;background:rgba({INK_RGB},0.18);
  border:5px solid #fff;box-shadow:0 0 0 2px rgba({INK_RGB},0.10);}}
.tl-dot.on{{background:{ACCENT};box-shadow:0 0 0 3px {ACCENT}44;width:34px;height:34px;
  margin-top:-3px;}}
.tl-lab{{font-size:23px;color:rgba({INK_RGB},0.5);font-weight:600;}}
.tl-lab.on{{color:{ACCENT};font-weight:800;}}
.tl-call{{position:absolute;font-size:24px;font-weight:700;color:{ACCENT};}}
/* 게이지 */
.gnum{{font-size:150px;font-weight:800;color:{ACCENT};line-height:0.9;
  letter-spacing:-5px;}}
.gnum span{{font-size:64px;letter-spacing:-2px;}}
.gsub{{font-size:30px;font-weight:700;color:rgba({INK_RGB},0.5);margin-top:8px;}}
/* 가이드 액션 */
.act{{display:flex;gap:26px;align-items:flex-start;padding:22px 0;
  border-bottom:1px solid rgba({INK_RGB},0.07);}}
.act.last{{border-bottom:0;padding-bottom:0;}}
.act.first{{padding-top:0;}}
.act-n{{width:50px;height:50px;flex:none;border-radius:50%;background:{ACCENT};
  color:#fff;font-size:26px;font-weight:800;display:flex;align-items:center;
  justify-content:center;}}
.act-t{{font-size:30px;line-height:1.45;color:{INK};font-weight:500;padding-top:6px;}}
.act-t b{{font-weight:800;}}
/* 칩(커버) */
.pill{{display:inline-block;background:#fff;border:1px solid rgba({INK_RGB},0.1);
  border-radius:999px;padding:15px 28px;font-size:27px;font-weight:700;
  color:rgba({INK_RGB},0.7);margin:0 12px 14px 0;}}
.pill b{{color:{ACCENT};}}"""

ARROW = (f'<div class="arrow" style="position:absolute;right:84px;bottom:62px;'
         f'font-size:27px;font-weight:600;line-height:1;color:{ACCENT};">&gt;</div>')


def chrome_path(explicit=None):
    cands = ([explicit] if explicit else []) + [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chrome"):
        cands.append(shutil.which(n))
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


def brand(n, total, arrow=True):
    s = ('<div class="brand">EX-<span>RAY</span></div>'
         f'<div class="counter">{n:02d}</div>')
    return s, (ARROW if arrow else "")


def head_block(kicker, heading, *, ktop=288, htop=326, hsize=46):
    """챕터 키커 + 제목."""
    return (f'<div class="kicker" style="top:{ktop}px;">{kicker}</div>'
            f'<div class="h" style="top:{htop}px;font-size:{hsize}px;">{heading}</div>')


# ── 슬라이드 ──────────────────────────────────────────────────────────────────
def slides():
    total = 8
    out = []

    # 01 · 커버 — 리포트 미리보기 후킹
    head, arr = brand(1, total)
    pills = ('<div style="position:absolute;left:80px;top:980px;width:920px;">'
             '<span class="pill"><b>8</b>챕터</span>'
             '<span class="pill">약 <b>7,000</b>자</span>'
             '<span class="pill">실제 카톡 <b>원문 근거</b></span></div>')
    out.append(
        '<div class="slide">' + head +
        '<div class="kicker" style="top:360px;">REPORT PREVIEW</div>'
        '<div class="h" style="top:404px;font-size:62px;line-height:1.22;">'
        '카톡 한 번 올리면,<br>이런 리포트가 나와요.</div>'
        '<div class="note" style="top:678px;width:860px;">전 연인과의 대화를 통째로 읽고, '
        '헤어진 진짜 이유부터 재회 가이드까지. 다음 장에서 실제 양식 그대로 보여줄게요.</div>'
        + pills + arr + '</div>'
    )

    # 02 · 목차 (8챕터 구성)
    toc_items = [
        "관계 한눈에 요약", "헤어진 진짜 이유", "관계 7단계 타임라인",
        "대화 정량 분석", "상대의 속마음", "재회 가능성 진단",
        "나의 연애 캐릭터", "다음 연애 가이드",
    ]
    rows = ""
    for i, t in enumerate(toc_items, 1):
        cls = "toc-row" + (" first" if i == 1 else "") + (" last" if i == len(toc_items) else "")
        rows += (f'<div class="{cls}"><span class="toc-num">{i:02d}</span>'
                 f'<span class="toc-title">{t}</span></div>')
    head, arr = brand(2, total)
    out.append(
        '<div class="slide">' + head +
        head_block("CONTENTS", "8개 챕터로,<br>관계 전체를 한 권에.", htop=326, hsize=46) +
        f'<div class="panel" style="top:540px;">{rows}</div>'
        + arr + '</div>'
    )

    # 03 · 헤어진 진짜 이유 — 인용 근거
    head, arr = brand(3, total)
    quote_panel = (
        '<div class="plab">근거가 된 카톡 원문</div>'
        '<div class="quote">“바쁜 건 알겠는데, 나 오늘 좀 힘들다고 말했잖아.”</div>'
        '<div class="quote-meta">2025.03.14 · 상대 → 나</div>'
        '<div style="height:30px;"></div>'
        '<div class="verdict">결정적인 균열은 ‘다툼’이 아니라 <b>반복된 무응답</b>이었어요. '
        '같은 패턴이 11번 나타났고, 그때마다 대화가 끊겼습니다.</div>'
    )
    out.append(
        '<div class="slide">' + head +
        head_block("CHAPTER 02 · 헤어진 진짜 이유", "추측이 아니라,<br>원문으로 짚어줘요.", htop=326, hsize=46) +
        f'<div class="panel" style="top:548px;">{quote_panel}</div>'
        + arr + '</div>'
    )

    # 04 · 관계 7단계 타임라인
    phases = ["썸", "초기", "황금기", "권태", "갈등", "소강", "이별"]
    active = 3  # 권태
    cells = ""
    for i, p in enumerate(phases):
        on = " on" if i == active else ""
        cells += (f'<div class="tl-cell"><span class="tl-dot{on}"></span>'
                  f'<span class="tl-lab{on}">{p}</span></div>')
    tl_panel = (
        '<div class="plab">관계 페이즈</div>'
        '<div class="tl-wrap"><div class="tl-line"></div>'
        f'<div class="tl">{cells}</div>'
        '<div class="tl-call" style="top:-50px;left:50%;transform:translateX(-50%);">'
        '여기서부터 식기 시작 ↓</div></div>'
        '<div style="height:42px;"></div>'
        '<div class="verdict">황금기는 <b>2025.01~02</b>. '
        '3월 들어 답장 텀이 길어지면서 권태기로 접어들었어요.</div>'
    )
    head, arr = brand(4, total)
    out.append(
        '<div class="slide">' + head +
        head_block("CHAPTER 03 · 관계 타임라인", "어디서부터 식었는지,<br>한 줄로 보여요.", htop=326, hsize=46) +
        f'<div class="panel" style="top:548px;padding-top:54px;">{tl_panel}</div>'
        + arr + '</div>'
    )

    # 05 · 대화 정량 분석 — 지표 바
    stats = [
        ("평균 답장 속도", "나 12분 vs 상대 3.4시간", 22),
        ("먼저 연락한 비율", "나 78% : 상대 22%", 78),
        ("애칭 사용 빈도", "3월부터 87% 감소", 13),
        ("후반 2개월 갈등", "14회", 64),
    ]
    srows = ""
    for i, (lab, val, pct) in enumerate(stats):
        cls = "stat" + (" last" if i == len(stats) - 1 else "")
        srows += (f'<div class="{cls}"><div class="stat-top">'
                  f'<span class="stat-label">{lab}</span>'
                  f'<span class="stat-val">{val}</span></div>'
                  f'<div class="bar"><i style="width:{pct}%;"></i></div></div>')
    head, arr = brand(5, total)
    out.append(
        '<div class="slide">' + head +
        head_block("CHAPTER 04 · 정량 분석", "느낌이 아니라,<br>숫자로 정리돼요.", htop=326, hsize=46) +
        f'<div class="panel" style="top:548px;">{srows}</div>'
        + arr + '</div>'
    )

    # 06 · 재회 가능성 게이지
    head, arr = brand(6, total)
    gauge_panel = (
        '<div class="plab">재회 가능성</div>'
        '<div style="display:flex;align-items:flex-end;gap:24px;">'
        '<div class="gnum">37<span>%</span></div>'
        '<div class="gsub" style="padding-bottom:18px;">낮지만,<br>0은 아님</div></div>'
        '<div style="height:30px;"></div>'
        '<div class="bar" style="height:22px;"><i style="width:37%;"></i></div>'
        '<div style="height:34px;"></div>'
        '<div class="verdict">마지막 3주간 <b>먼저 연락한 쪽은 상대</b>였어요. '
        '말투는 식었지만, 끊지 못하는 신호가 남아 있습니다.</div>'
    )
    out.append(
        '<div class="slide">' + head +
        head_block("CHAPTER 05 · 상대의 속마음", "재회 가능성도,<br>%로 추정해줘요.", htop=326, hsize=46) +
        f'<div class="panel" style="top:548px;">{gauge_panel}</div>'
        + arr + '</div>'
    )

    # 07 · 다음 연애 가이드
    acts = [
        "<b>먼저 표현하기.</b> 서운함을 삼키다 한 번에 터뜨리는 패턴이 반복됐어요.",
        "<b>답장 텀 신경 쓰기.</b> 바쁠 땐 ‘이따 답할게’ 한마디면 충분했어요.",
        "<b>기대치 먼저 맞추기.</b> 연락 빈도에 대한 생각이 서로 달랐어요.",
    ]
    arows = ""
    for i, a in enumerate(acts, 1):
        cls = "act" + (" first" if i == 1 else "") + (" last" if i == len(acts) else "")
        arows += (f'<div class="{cls}"><span class="act-n">{i}</span>'
                  f'<span class="act-t">{a}</span></div>')
    head, arr = brand(7, total)
    out.append(
        '<div class="slide">' + head +
        head_block("CHAPTER 08 · 다음 연애 가이드", "다음 연애에서,<br>바꿀 것 3가지.", htop=326, hsize=46) +
        f'<div class="panel" style="top:548px;">{arows}</div>'
        + arr + '</div>'
    )

    # 08 · 마감 CTA — 화살표 없음
    head, _ = brand(8, total, arrow=False)
    out.append(
        '<div class="slide">' + head +
        '<div class="h" style="top:360px;font-size:60px;line-height:1.24;text-align:center;width:920px;">'
        f'이 모든 게,<br><span style="color:{ACCENT};">카톡 하나</span>로.</div>'
        '<div class="note" style="top:1060px;">전남친·전여친 카톡 한 번 올려봐. '
        'EX-RAY가 끝까지 읽고 8챕터 리포트로 정리해줄게.</div>'
        '<div class="cta" style="top:1192px;">exray.kr</div>'
        '</div>'
    )
    return out


def build_html(slide_list):
    return (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
        '<title>EX-RAY · 리포트 미리보기</title>'
        f'<link rel="stylesheet" href="{PRETENDARD}">'
        '<style>' + CSS +
        'body{background:#e9e6dd;display:flex;flex-direction:column;align-items:center;'
        'gap:32px;padding:48px;}.slide{box-shadow:0 4px 24px rgba(0,0,0,0.12);}</style>'
        '</head><body>' + "".join(slide_list) + '</body></html>'
    )


PAGE = ('<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
        '<link rel="stylesheet" href="{font}"><style>{css}'
        'html,body{{margin:0;padding:0;background:transparent;display:block;}}'
        '.slide{{box-shadow:none!important;}}</style></head><body>{slide}</body></html>')


# ── 편집형 HTML ─────────────────────────────────────────────────────────────
def _data_uri(path, mime):
    import base64
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


EDITOR_CSS = f"""
body{{background:#1b1b1d;margin:0;padding:40px 20px 120px;font-family:'Pretendard',sans-serif;}}
.bar{{position:fixed;left:0;top:0;right:0;z-index:50;display:flex;align-items:center;gap:16px;
  padding:14px 22px;background:rgba(20,20,22,0.92);backdrop-filter:blur(8px);
  border-bottom:1px solid #2c2c30;color:#eaeaea;font-size:14px;}}
.bar b{{color:{ACCENT};}}
.bar .sp{{flex:1;}}
.bar button{{background:{ACCENT};color:#fff;border:0;border-radius:999px;
  padding:10px 18px;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit;}}
.bar input[type=range]{{accent-color:{ACCENT};}}
.tip{{color:#9a9a9e;font-size:13px;}}
.frames{{display:flex;flex-direction:column;align-items:center;gap:28px;margin-top:64px;}}
.frame{{display:flex;flex-direction:column;align-items:center;gap:12px;}}
.holder{{width:calc(1080px * var(--z,0.5));height:calc(1350px * var(--z,0.5));}}
.holder .slide{{transform:scale(var(--z,0.5));transform-origin:top left;
  box-shadow:0 10px 40px rgba(0,0,0,0.5);border-radius:6px;}}
.frame .dl{{background:#26262a;color:#eaeaea;border:1px solid #3a3a40;border-radius:999px;
  padding:8px 16px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;}}
[contenteditable]{{outline:none;cursor:text;border-radius:4px;transition:box-shadow .12s;}}
[contenteditable]:hover{{box-shadow:0 0 0 2px {ACCENT}55;}}
[contenteditable]:focus{{box-shadow:0 0 0 2px {ACCENT};}}
"""

EDITOR_JS = f"""
import h2c from 'https://cdn.jsdelivr.net/npm/html2canvas-pro@1.5.11/+esm';

const SEL = '.h,.note,.cta,.kicker,.plab,.toc-title,.quote,.quote-meta,.verdict,'
  + '.stat-label,.stat-val,.tl-lab,.tl-call,.gsub,.act-t,.pill';
document.querySelectorAll('.slide').forEach(s => {{
  s.querySelectorAll(SEL).forEach(el => {{ el.contentEditable = 'true'; el.spellcheck = false; }});
}});

const sandbox = document.createElement('div');
sandbox.style.cssText = 'position:fixed;left:-100000px;top:0;width:1080px;height:0;overflow:visible;';
document.body.appendChild(sandbox);
const pad = n => String(n).padStart(2, '0');

async function shoot(slide, name) {{
  await document.fonts.ready;
  const bg = getComputedStyle(slide).backgroundColor || '{BG}';
  const clone = slide.cloneNode(true);
  clone.style.transform = 'none';
  clone.style.boxShadow = 'none';
  clone.style.borderRadius = '0';
  sandbox.innerHTML = '';
  sandbox.appendChild(clone);
  await new Promise(r => setTimeout(r, 20));
  const canvas = await h2c(clone, {{ scale: 2, width: 1080, height: 1350,
    backgroundColor: bg, useCORS: true, logging: false }});
  sandbox.innerHTML = '';
  const blob = await new Promise(res => canvas.toBlob(res, 'image/png'));
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}}

document.querySelectorAll('.frame .dl').forEach((btn, i) => {{
  btn.onclick = () => shoot(btn.parentElement.querySelector('.slide'), `exray-report-${{pad(i+1)}}.png`);
}});
document.getElementById('all').onclick = async () => {{
  const slides = [...document.querySelectorAll('.frame .slide')];
  for (let i = 0; i < slides.length; i++) {{
    await shoot(slides[i], `exray-report-${{pad(i+1)}}.png`);
    await new Promise(r => setTimeout(r, 400));
  }}
}};
const z = document.getElementById('zoom');
const setZ = () => document.documentElement.style.setProperty('--z', z.value);
z.oninput = setZ; setZ();
"""


def build_editor(slide_list):
    font = _data_uri(os.path.join(HERE, "assets", "Pretendard.woff2"), "font/woff2")
    font_face = (f"@font-face{{font-family:'Pretendard';font-weight:45 920;"
                 f"font-style:normal;font-display:swap;src:url({font}) format('woff2');}}")
    frames = []
    for i, s in enumerate(slide_list, start=1):
        frames.append(f'<div class="frame"><div class="holder">{s}</div>'
                      f'<button class="dl">{i:02d} · 이 장 PNG 저장</button></div>')
    bar = ('<div class="bar"><b>EX-RAY 리포트 미리보기 편집기</b>'
           '<span class="tip">글자를 클릭해서 바로 고치세요. 다 고치면 저장 버튼 ›</span>'
           '<span class="sp"></span>'
           '<label class="tip">보기 크기 <input id="zoom" type="range" min="0.25" max="1" step="0.05" value="0.5"></label>'
           '<button id="all">전체 8장 PNG 저장</button></div>')
    return (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>EX-RAY 리포트 미리보기 편집기</title>'
        '<style>' + font_face + CSS + EDITOR_CSS + '</style></head><body>'
        + bar + '<div class="frames">' + "".join(frames) + '</div>'
        + '<script type="module">' + EDITOR_JS + '</script></body></html>'
    )


def export_png(slide_list, scale=2, prefix="exray-report"):
    chrome = chrome_path()
    if not chrome:
        sys.exit("Chrome 실행파일을 찾지 못했습니다.")
    outdir = os.path.join(HERE, "png")
    os.makedirs(outdir, exist_ok=True)
    made = []
    for i, slide_html in enumerate(slide_list, start=1):
        page = PAGE.format(font=PRETENDARD, css=CSS, slide=slide_html)
        html_path = os.path.join(HERE, f".tmp-slide-{i:02d}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page)
        out = os.path.join(outdir, f"{prefix}-{i:02d}.png")
        cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--no-sandbox", f"--force-device-scale-factor={scale}",
               "--window-size=1080,1350", "--default-background-color=00000000",
               "--virtual-time-budget=5000", f"--screenshot={out}",
               "file://" + html_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        os.remove(html_path)
        if not os.path.exists(out):
            sys.stderr.write(res.stderr[-800:] + "\n")
            sys.exit(f"슬라이드 {i} 캡처 실패")
        made.append(out)
    print(f"PNG {len(made)}장 → {outdir} ({1080*scale}x{1350*scale})", file=sys.stderr)


if __name__ == "__main__":
    sl = slides()
    with open(os.path.join(HERE, "report-preview.html"), "w", encoding="utf-8") as f:
        f.write(build_html(sl))
    print(f"HTML 생성: report-preview.html ({len(sl)}장)", file=sys.stderr)
    with open(os.path.join(HERE, "editor.html"), "w", encoding="utf-8") as f:
        f.write(build_editor(sl))
    print("편집기 생성: editor.html", file=sys.stderr)
    if "--png" in sys.argv:
        export_png(sl)
