#!/usr/bin/env python3
"""EX-RAY 서비스 소개 카드뉴스 (8장).

service-intro(랩미)에서 정돈한 레이아웃 골격을 그대로 가져와,
EX-RAY 브랜드(크림 라이트 + 핑크)로 리스킨한 버전.
- 라이트 크림 배경 + 미세 도트 텍스처.
- 카톡 말풍선 커버(전 애인과의 마지막 대화 컨셉).
- 본문 글씨 절제, 좌하단 단일 카운터 + 우하단 셰브론.

- 결합 HTML(service-intro.html) + 슬라이드별 PNG(png/) 둘 다 생성.
- PNG는 Chrome 헤드리스로 1080x1350(기본 2배=2160x2700) 캡처.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# --- 테마 (EX-RAY / 크림 라이트 + 핑크) --------------------------------------
BG = "#fff8ef"            # 따뜻한 크림
ACCENT = "#ff2e63"        # 브랜드 핑크
ANSWER_TEXT = "#ffffff"   # 답변 말풍선 글자(핑크 위 화이트)
BUBBLE_GRAY = "#ece9e0"   # 질문 말풍선 배경(배경과 동계)
INK = "#0d0d0d"           # 헤드라인/제목(잉크 블랙)
INK_RGB = "13,13,13"      # 본문·보조 글자 rgba 기준
PRETENDARD = ("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/"
              "dist/web/static/pretendard.css")

CSS = f"""*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Pretendard',sans-serif;}}
.slide{{width:1080px;height:1350px;color:{INK};position:relative;overflow:hidden;
  background-color:{BG};
  background-image:radial-gradient(rgba({INK_RGB},0.05) 1px, transparent 1.5px);
  background-size:30px 30px;}}
.slide h1,.slide h2,.slide p,.slide span{{word-break:keep-all;}}
.brand{{position:absolute;left:80px;top:72px;font-size:34px;font-weight:800;letter-spacing:-0.5px;}}
.brand span{{color:{ACCENT};}}
.counter{{position:absolute;left:80px;bottom:62px;font-size:27px;font-weight:600;
  line-height:1;letter-spacing:1px;color:rgba({INK_RGB},0.30);}}
.h{{position:absolute;left:80px;width:900px;font-weight:800;color:{INK};
  letter-spacing:-1px;line-height:1.22;}}
.body{{position:absolute;left:80px;width:900px;font-size:29px;line-height:1.78;
  color:rgba({INK_RGB},0.70);}}
.body b{{color:{INK};font-weight:700;}}
.label{{position:absolute;left:80px;font-size:30px;font-weight:600;color:{ACCENT};}}
.note{{position:absolute;left:80px;width:900px;font-size:29px;line-height:1.7;
  color:rgba({INK_RGB},0.55);}}
.cta{{position:absolute;left:80px;font-size:36px;font-weight:700;color:{ACCENT};}}"""

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


# ── 슬라이드 정의 (heading+body 카드) ─────────────────────────────────────────
def card(n, total, heading, body_html, *, hsize=40, htop=360,
         bfs=29, blh=1.78, btop=None, extra="", arrow=True, halign="left"):
    head, arr = brand(n, total, arrow)
    if btop is None:
        btop = htop + hsize + 56
    return (
        '<div class="slide">' + head + extra +
        f'<div class="h" style="top:{htop}px;font-size:{hsize}px;text-align:{halign};">{heading}</div>'
        f'<div class="body" style="top:{btop}px;font-size:{bfs}px;line-height:{blh};">{body_html}</div>'
        + arr + '</div>'
    )


def slides():
    total = 8
    out = []

    # 01 · 커버 — 전남친이 보낸 훈수 DM 말풍선 + 후킹 헤드라인
    head, arr = brand(1, total)
    out.append(
        '<div class="slide">' + head +
        '<div style="position:absolute;left:80px;top:300px;width:60px;height:60px;'
        f'border-radius:50%;background:rgba({INK_RGB},0.10);"></div>'
        f'<div class="qb" style="position:absolute;left:160px;top:300px;max-width:600px;background:{BUBBLE_GRAY};'
        f'color:rgba({INK_RGB},0.9);font-size:33px;line-height:1.45;padding:20px 28px;'
        'border-radius:30px 30px 30px 8px;">너가 정신적으로 성숙한 사람이 됐으면 해. 학교에서 보자</div>'
        f'<div class="ab" style="position:absolute;right:80px;top:548px;background:{ACCENT};color:{ANSWER_TEXT};'
        'font-size:33px;font-weight:600;padding:18px 30px;border-radius:30px 30px 8px 30px;">...지금 그걸 네가?</div>'
        '<div class="h" style="top:892px;font-size:62px;line-height:1.2;">어이가 없어서,<br>하나 만들었다.</div>'
        '<div class="label" style="top:1188px;">전남친 카톡 분석기 만든 썰 ›</div>'
        + arr + '</div>'
    )

    # 02 · 사실 나도 해보고 싶었다
    out.append(card(
        2, total,
        "전남친 구글폼, 사실 나도 하고 싶었어",
        "한창 유행했잖아. 솔직히 궁금했지. 내가 어떤 연애를 했는지, 걔는 날 어떻게 기억하는지. "
        "근데 나 지금 만나는 사람도 있고, 무엇보다 <b>걔가 날 차단해놨더라고</b> ㅋㅋ "
        "연락할 길도 없는데 굳이 싶어서 그냥 묻고 살았어. 진짜 1도 생각 안 하고 있었다.",
        halign="center",
    ))

    # 03 · 갑자기 연락이 옴
    out.append(card(
        3, total,
        "근데 갑자기, 연락이 왔다",
        "지가 먼저 차단해놓고, 군대 룰루랄라 가놓고선. "
        "어느 날 갑자기 디엠이 온 거야. 무슨 큰일이라도 났나 싶어서 열어봤지. "
        "<b>내용을 아주 조금만 공개하자면.</b>",
        halign="center",
    ))

    # 04 · 그 훈수 (펀치라인)
    out.append(card(
        4, total,
        "“정신적으로 성숙했으면 좋겠어”",
        "나더러 훈수를 두더라고? 학교에서 보잰다. "
        "와, 진짜 어이가 없어서 ㅋㅋㅋㅋ <b>누구 때문에 헤어졌는데.</b> "
        "정신적 성숙은 또 누가 할 말이야. 다른 사람도 아니고 네가??",
        halign="center",
    ))

    # 05 · 자기 의심
    out.append(card(
        5, total,
        "근데 한편, 내가 잘못한 걸까?",
        "사람 기억은 자기한테 유리하게 바뀐다잖아. "
        "싸울 때 내가 말이 심했던 적은 없었는지, 내가 놓친 건 없었는지. "
        "근데 친구한테 물어보면 당연히 내 편이고, "
        "걔 친구한테 물어보면 또 반대로 말하겠지 ㅋㅋ",
        halign="center",
    ))

    # 06 · 제3자가 카톡만 보고 판단하면? + 만든 계기
    out.append(card(
        6, total,
        "제3자가 카톡만 보고 판단하면?",
        "그게 처음으로 제일 궁금해졌어. <b>감정 다 빼고, 우리 대화만 보고 객관적으로.</b> "
        "나처럼 궁금한 사람 나만은 아닐 거 같았고, 마침 버킷리스트에 ‘앱 출시’도 있겠다. "
        "클로드 붙잡고 2주 만에 만들어버렸다 ㅋㅋ",
        halign="center",
    ))

    # 07 · 그게 EX-RAY
    out.append(card(
        7, total,
        "그게 바로 EX-RAY야",
        "카톡 통째로 올리면 AI가 몇천 줄을 다 읽고, "
        "‘여기서부터 식었네요’ ‘이 사람 이땐 마음이 남아 있었네요’ 하고 짚어줘. "
        "<b>8챕터, 약 7,000자.</b> 헤어진 진짜 이유부터 재회 가이드까지 한 권으로.",
        halign="center", bfs=28, blh=1.74,
    ))

    # 08 · 마감 — 화살표 없음
    head, _ = brand(8, total, arrow=False)
    out.append(
        '<div class="slide">' + head +
        '<div class="h" style="top:360px;font-size:60px;line-height:1.24;text-align:center;width:920px;">감정 말고,<br>'
        f'<span style="color:{ACCENT};">사실</span>이 궁금하면.</div>'
        '<div class="note" style="top:1060px;">전남친·전여친 카톡 한 번 올려봐. '
        '우리가 왜 헤어졌는지, EX-RAY가 끝까지 읽고 정리해줄게.</div>'
        '<div class="cta" style="top:1192px;">exray.kr</div>'
        '</div>'
    )
    return out


def build_html(slide_list):
    return (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
        '<title>EX-RAY · 서비스 소개</title>'
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
# 브라우저에서 글자를 클릭해 직접 고치고, 버튼으로 PNG를 내려받는다.
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

const SEL = '.h,.body,.brand,.counter,.label,.note,.cta,.qb,.ab';
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
  btn.onclick = () => shoot(btn.parentElement.querySelector('.slide'), `exray-intro-${{pad(i+1)}}.png`);
}});
document.getElementById('all').onclick = async () => {{
  const slides = [...document.querySelectorAll('.frame .slide')];
  for (let i = 0; i < slides.length; i++) {{
    await shoot(slides[i], `exray-intro-${{pad(i+1)}}.png`);
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
    bar = ('<div class="bar"><b>EX-RAY 카드뉴스 편집기</b>'
           '<span class="tip">글자를 클릭해서 바로 고치세요. 다 고치면 저장 버튼 ›</span>'
           '<span class="sp"></span>'
           '<label class="tip">보기 크기 <input id="zoom" type="range" min="0.25" max="1" step="0.05" value="0.5"></label>'
           '<button id="all">전체 8장 PNG 저장</button></div>')
    return (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>EX-RAY 카드뉴스 편집기</title>'
        '<style>' + font_face + CSS + EDITOR_CSS + '</style></head><body>'
        + bar + '<div class="frames">' + "".join(frames) + '</div>'
        + '<script type="module">' + EDITOR_JS + '</script></body></html>'
    )


def export_png(slide_list, scale=2, prefix="exray-intro"):
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
    with open(os.path.join(HERE, "service-intro.html"), "w", encoding="utf-8") as f:
        f.write(build_html(sl))
    print(f"HTML 생성: service-intro.html ({len(sl)}장)", file=sys.stderr)
    with open(os.path.join(HERE, "editor.html"), "w", encoding="utf-8") as f:
        f.write(build_editor(sl))
    print("편집기 생성: editor.html", file=sys.stderr)
    if "--png" in sys.argv:
        export_png(sl)
