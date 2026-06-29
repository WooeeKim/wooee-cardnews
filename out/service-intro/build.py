#!/usr/bin/env python3
"""랩미 서비스 소개 카드뉴스 (8장).

엑스레이 앱의 '따뜻한 미니멀' 톤으로 재설계한 버전.
- 따뜻한 다크 배경 + 미세한 도트 텍스처(클로드식 평평한 검정 대신).
- 잉크 단계 위계(불투명도만으로 만든 위계 대신 톤을 단계적으로).
- 본문 글씨 축소(34→29), 헤드라인도 절제(96→62).
- "magazine" 워드마크, 제목 앞 세로 액센트 바(│) 제거 → 깔끔한 위계로 대체.
- 브랜드 에셋(하트)은 글로우를 죽이고 작게, 거들기만.

- 결합 HTML(service-intro.html) + 슬라이드별 PNG(png/) 둘 다 생성.
- PNG는 Chrome 헤드리스로 1080x1350(기본 2배=2160x2700) 캡처.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# --- 테마 (랩미-파티 / 따뜻한 민트 다크) ------------------------------------
BG = "#161512"            # 따뜻한 차콜(차가운 #0e0e10 대신)
ACCENT = "#5DCAA5"        # 브랜드 민트
ANSWER_TEXT = "#08231c"   # 답변 말풍선 글자(액센트 어두운 동계색)
BUBBLE_GRAY = "#26251f"   # 질문 말풍선 배경(배경과 동계)
INK = "#f4f2ec"           # 헤드라인/제목(따뜻한 화이트)
INK_RGB = "244,242,236"   # 본문·보조 글자 rgba 기준
PRETENDARD = ("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/"
              "dist/web/static/pretendard.css")

CSS = f"""*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Pretendard',sans-serif;}}
.slide{{width:1080px;height:1350px;color:{INK};position:relative;overflow:hidden;
  background-color:{BG};
  background-image:radial-gradient(rgba({INK_RGB},0.045) 1px, transparent 1.5px);
  background-size:30px 30px;}}
.slide h1,.slide h2,.slide p,.slide span{{word-break:keep-all;}}
.brand{{position:absolute;left:80px;top:72px;font-size:34px;font-weight:800;letter-spacing:-0.5px;}}
.brand span{{color:{ACCENT};}}
.counter{{position:absolute;left:80px;bottom:62px;font-size:27px;font-weight:600;
  line-height:1;letter-spacing:1px;color:rgba({INK_RGB},0.34);}}
.h{{position:absolute;left:80px;width:900px;font-weight:800;color:{INK};
  letter-spacing:-1px;line-height:1.22;}}
.body{{position:absolute;left:80px;width:900px;font-size:29px;line-height:1.78;
  color:rgba({INK_RGB},0.72);}}
.body b{{color:{INK};font-weight:700;}}
.label{{position:absolute;left:80px;font-size:30px;font-weight:600;color:{ACCENT};}}
.note{{position:absolute;left:80px;width:900px;font-size:29px;line-height:1.7;
  color:rgba({INK_RGB},0.55);}}
.cta{{position:absolute;left:80px;font-size:36px;font-weight:700;color:{ACCENT};}}
.heart{{position:absolute;pointer-events:none;}}
.smoke{{position:absolute;left:0;bottom:0;width:1080px;height:820px;object-fit:cover;
  object-position:bottom;opacity:0.18;
  -webkit-mask-image:linear-gradient(to top,#000 0%,transparent 90%);
  mask-image:linear-gradient(to top,#000 0%,transparent 90%);}}"""

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
    s = ('<div class="brand">Lab<span>Meet</span></div>'
         f'<div class="counter">{n:02d}</div>')
    return s, (ARROW if arrow else "")


# ── 슬라이드 정의 (heading+body 카드) ─────────────────────────────────────────
# │바·kicker 없이 제목→본문만으로 깔끔하게. 위치는 절제된 스케일에 맞춰 재배치.
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

    # 01 · 커버 — 채팅 말풍선 후킹 + 하트(글로우 죽이고 작게)
    head, arr = brand(1, total)
    out.append(
        '<div class="slide">' + head +
        '<img class="heart" src="assets/heart.png" style="right:84px;top:560px;width:268px;opacity:0.9;'
        'filter:drop-shadow(0 18px 44px rgba(93,202,165,0.18));">'
        # 말풍선
        '<div style="position:absolute;left:80px;top:300px;width:60px;height:60px;'
        'border-radius:50%;background:rgba(244,242,236,0.12);"></div>'
        f'<div class="qb" style="position:absolute;left:160px;top:300px;background:{BUBBLE_GRAY};'
        f'color:rgba({INK_RGB},0.9);font-size:33px;padding:18px 28px;'
        'border-radius:30px 30px 30px 8px;">대전이 왜 노잼이야?</div>'
        f'<div class="ab" style="position:absolute;right:80px;top:408px;background:{ACCENT};color:{ANSWER_TEXT};'
        'font-size:33px;font-weight:600;padding:18px 30px;border-radius:30px 30px 8px 30px;">랩미 있는데?</div>'
        # 헤드라인 (절제: 96→62)
        '<div class="h" style="top:892px;font-size:62px;line-height:1.2;">연구는 혼자,<br>저녁은 같이.</div>'
        '<div class="label" style="top:1188px;">랩미가 뭐 하는 곳이냐면 ›</div>'
        + arr + '</div>'
    )

    # 02 · 랩미가 뭐냐면
    out.append(card(
        2, total,
        "혹시 대학원생이에요?",
        "심심한데 바쁘기도 하잖아요. 그런 대학(원)생이랑 연구자들끼리 만나는 오프라인 파티예요. "
        "소개팅 해달라 부탁하기도 기 빨리고요. 결이 비슷한 사람들끼리, "
        "<b>랩미가 대신 모아드려요.</b> "
        "파티만 있는 건 아니고, 셀소랑 커뮤니티까지 랩미 안에서 이어져요.",
        halign="center",
    ))

    # 03 · 누가 와요
    out.append(card(
        3, total,
        "랩실 밖에선 다 처음 보는 사이",
        "카이스트, 충남대, 서울대. 각자 자리에서 열심히 사는 사람들이 와요. "
        "아무나 만나고 싶진 않은 사람, 연구만 하다 사람이 그리워진 사람. "
        "<b>결국 여기로 다 모여요.</b>",
    ))

    # 04 · 파티 — 연기 + 반전 후킹
    out.append(card(
        4, total,
        "기 안 빨리게, 알잘딱으로",
        "신청만 하면 자리는 저희가 채워둘게요. 내향인 편, 외향인 편으로 나눠서 열려요. "
        "신나는 레이빙도, 조용한 와인파티도 있어요. "
        "<b>누가 올지는 안 알려드려요.</b> "
        "현장에서 직접 확인하기.",
        extra='<img class="smoke" src="assets/smoke.webp">',
    ))

    # 05 · 호스피탤리티
    out.append(card(
        5, total,
        "즐기기만 하면 돼요",
        "무제한 논알콜 샴페인이랑 치즈 플레이트까지 준비해둘게요. "
        "어색하게 서 있을 틈 없게, 분위기는 저희가 만들어요. 나머지는 그냥 즐기시면 돼요.",
    ))

    # 06 · 앱 (셀소 + 커뮤니티)
    out.append(card(
        6, total,
        "파티 끝나도 랩미는 안 끝나요",
        "셀프소개팅 게시판 ‘셀소’에서 마음 가는 사람한테 먼저 말 걸어보고, "
        "커뮤니티에선 연구 자랑이든 코웍 제안이든 가볍게 밍글링부터. "
        "<b>굳이 파티에 안 와도</b> 랩미 안에서 이어져요.",
    ))

    # 07 · 신뢰 — 카이스트 운영진 + 작은 하트
    out.append(card(
        7, total,
        "만드는 사람도 결국 같은 솔로",
        "랩미는 <b>카이스트 사람들이 직접</b> 만들어가요. "
        "심심하고 바쁜 마음 누구보다 잘 아니까, 기 안 빨리게 자리 하나하나 신경 써요. "
        "운영진도 똑같이 랩실과 집만 반복하던 사람들이거든요.",
        extra='<img class="heart" src="assets/heart.png" style="right:104px;top:968px;width:156px;opacity:0.7;'
              'filter:drop-shadow(0 12px 28px rgba(93,202,165,0.14));">',
    ))

    # 08 · 마감 — 수미상관 + 하트, 화살표 없음
    head, _ = brand(8, total, arrow=False)
    out.append(
        '<div class="slide">' + head +
        '<img class="heart" src="assets/heart.png" style="right:92px;top:612px;width:244px;opacity:0.9;'
        'filter:drop-shadow(0 18px 44px rgba(93,202,165,0.18));">'
        '<div class="h" style="top:360px;font-size:58px;line-height:1.2;">연구는 혼자.<br>저녁은 같이.</div>'
        '<div class="note" style="top:1072px;">다음 파티 일정이랑 신청은 인스타에서 안내하고 있어요. '
        '궁금한 건 DM으로 편하게 물어보세요.</div>'
        '<div class="cta" style="top:1196px;">@labmeet.love</div>'
        '</div>'
    )
    return out


def build_html(slide_list):
    return (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
        '<title>랩미 · 서비스 소개</title>'
        f'<link rel="stylesheet" href="{PRETENDARD}">'
        '<style>' + CSS +
        'body{background:#f2f0e9;display:flex;flex-direction:column;align-items:center;'
        'gap:32px;padding:48px;}.slide{box-shadow:0 4px 24px rgba(0,0,0,0.15);}</style>'
        '</head><body>' + "".join(slide_list) + '</body></html>'
    )


PAGE = ('<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
        '<link rel="stylesheet" href="{font}"><style>{css}'
        'html,body{{margin:0;padding:0;background:transparent;display:block;}}'
        '.slide{{box-shadow:none!important;}}</style></head><body>{slide}</body></html>')


# ── 편집형 HTML ─────────────────────────────────────────────────────────────
# 브라우저에서 글자를 클릭해 직접 고치고, 버튼으로 PNG를 내려받는다.
# 에셋은 data URI로 인라인해서(파일 fetch 차단 회피) 어디서 열든 그대로 굽힌다.
def _data_uri(path, mime):
    import base64
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


EDITOR_CSS = """
body{background:#1b1b1d;margin:0;padding:40px 20px 120px;font-family:'Pretendard',sans-serif;}
.bar{position:fixed;left:0;top:0;right:0;z-index:50;display:flex;align-items:center;gap:16px;
  padding:14px 22px;background:rgba(20,20,22,0.92);backdrop-filter:blur(8px);
  border-bottom:1px solid #2c2c30;color:#eaeaea;font-size:14px;}
.bar b{color:#5DCAA5;}
.bar .sp{flex:1;}
.bar button{background:#5DCAA5;color:#08231c;border:0;border-radius:999px;
  padding:10px 18px;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit;}
.bar input[type=range]{accent-color:#5DCAA5;}
.tip{color:#9a9a9e;font-size:13px;}
.frames{display:flex;flex-direction:column;align-items:center;gap:28px;margin-top:64px;}
.frame{display:flex;flex-direction:column;align-items:center;gap:12px;}
.holder{width:calc(1080px * var(--z,0.5));height:calc(1350px * var(--z,0.5));}
.holder .slide{transform:scale(var(--z,0.5));transform-origin:top left;
  box-shadow:0 10px 40px rgba(0,0,0,0.5);border-radius:6px;}
.frame .dl{background:#26262a;color:#eaeaea;border:1px solid #3a3a40;border-radius:999px;
  padding:8px 16px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;}
[contenteditable]{outline:none;cursor:text;border-radius:4px;transition:box-shadow .12s;}
[contenteditable]:hover{box-shadow:0 0 0 2px rgba(93,202,165,0.35);}
[contenteditable]:focus{box-shadow:0 0 0 2px #5DCAA5;}
"""

EDITOR_JS = """
import h2c from 'https://cdn.jsdelivr.net/npm/html2canvas-pro@1.5.11/+esm';

// 글자를 직접 고칠 수 있게 contenteditable 부여 (이미지/위치는 건드리지 않는다)
const SEL = '.h,.body,.brand,.counter,.label,.note,.cta,.qb,.ab';
document.querySelectorAll('.slide').forEach(s => {
  s.querySelectorAll(SEL).forEach(el => { el.contentEditable = 'true'; el.spellcheck = false; });
});

// 화면에선 transform:scale 로 줄여 보여주지만, 캡처는 변형 없는 오프스크린 클론을
// 원본 1080x1350 으로 떠서 굽는다 (부모 transform 때문에 잘리는 문제 회피).
const sandbox = document.createElement('div');
sandbox.style.cssText = 'position:fixed;left:-100000px;top:0;width:1080px;height:0;overflow:visible;';
document.body.appendChild(sandbox);
const pad = n => String(n).padStart(2, '0');

async function shoot(slide, name) {
  await document.fonts.ready;
  const bg = getComputedStyle(slide).backgroundColor || '#161512';
  const clone = slide.cloneNode(true);
  clone.style.transform = 'none';
  clone.style.boxShadow = 'none';
  clone.style.borderRadius = '0';
  sandbox.innerHTML = '';
  sandbox.appendChild(clone);
  await new Promise(r => setTimeout(r, 20));
  const canvas = await h2c(clone, { scale: 2, width: 1080, height: 1350,
    backgroundColor: bg, useCORS: true, logging: false });
  sandbox.innerHTML = '';
  const blob = await new Promise(res => canvas.toBlob(res, 'image/png'));
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

document.querySelectorAll('.frame .dl').forEach((btn, i) => {
  btn.onclick = () => shoot(btn.parentElement.querySelector('.slide'), `labme-intro-${pad(i+1)}.png`);
});
document.getElementById('all').onclick = async () => {
  const slides = [...document.querySelectorAll('.frame .slide')];
  for (let i = 0; i < slides.length; i++) {
    await shoot(slides[i], `labme-intro-${pad(i+1)}.png`);
    await new Promise(r => setTimeout(r, 400));
  }
};
const z = document.getElementById('zoom');
const setZ = () => document.documentElement.style.setProperty('--z', z.value);
z.oninput = setZ; setZ();
"""


def build_editor(slide_list):
    heart = _data_uri(os.path.join(HERE, "assets", "heart.png"), "image/png")
    smoke = _data_uri(os.path.join(HERE, "assets", "smoke.webp"), "image/webp")
    # 폰트를 data URI @font-face 로 인라인 → html-to-image 캡처 시 네트워크 0,
    # 어디서 열든(오프라인 포함) Pretendard 그대로 굽힌다.
    font = _data_uri(os.path.join(HERE, "assets", "Pretendard.woff2"), "font/woff2")
    font_face = (f"@font-face{{font-family:'Pretendard';font-weight:45 920;"
                 f"font-style:normal;font-display:swap;src:url({font}) format('woff2');}}")
    frames = []
    for i, s in enumerate(slide_list, start=1):
        s = s.replace("assets/heart.png", heart).replace("assets/smoke.webp", smoke)
        frames.append(f'<div class="frame"><div class="holder">{s}</div>'
                      f'<button class="dl">{i:02d} · 이 장 PNG 저장</button></div>')
    bar = ('<div class="bar"><b>랩미 카드뉴스 편집기</b>'
           '<span class="tip">글자를 클릭해서 바로 고치세요. 다 고치면 저장 버튼 ›</span>'
           '<span class="sp"></span>'
           '<label class="tip">보기 크기 <input id="zoom" type="range" min="0.25" max="1" step="0.05" value="0.5"></label>'
           '<button id="all">전체 8장 PNG 저장</button></div>')
    return (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>랩미 카드뉴스 편집기</title>'
        '<style>' + font_face + CSS + EDITOR_CSS + '</style></head><body>'
        + bar + '<div class="frames">' + "".join(frames) + '</div>'
        + '<script type="module">' + EDITOR_JS + '</script></body></html>'
    )


def export_png(slide_list, scale=2, prefix="labme-intro"):
    chrome = chrome_path()
    if not chrome:
        sys.exit("Chrome 실행파일을 찾지 못했습니다.")
    outdir = os.path.join(HERE, "png")
    os.makedirs(outdir, exist_ok=True)
    # 에셋을 file:// 로 읽도록 임시 페이지를 작업 폴더(HERE)에 둔다.
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
