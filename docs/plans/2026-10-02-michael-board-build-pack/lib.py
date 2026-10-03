# Tiny layout library: one element list -> (a) Miro Canvas Composer SVG, (b) local HTML preview.
import html, re
from xml.sax.saxutils import escape

INK = '#1a1a1a'; BODY = '#595959'; LINE = '#b0b0b0'; EDGE = '#e7e7e7'; FAINT = '#f7f7f7'; WHITE = '#ffffff'
PURPLE_FAINT = '#f4f2fd'; PURPLE_MED = '#8f7fee'; RED_FAINT = '#fff0f0'; RED_LIGHT = '#ffc6c6'

# status -> (label, fill, stroke, textcolor)
STAT = {
    'LIVE':     ('LIVE', '#adf0c7', 'none', '#067429'),
    'MANUAL':   ('MANUAL', '#c6dcff', 'none', '#305bab'),
    'PARTIAL':  ('PARTIAL', '#fff6b6', 'none', '#af7e04'),
    'BUILT':    ('BUILT, NOT LIVE', '#f8d3af', 'none', '#9b4a08'),
    'PROPOSED': ('PROPOSED', '#dedaff', 'none', '#6631d7'),
    'DEFERRED': ('DEFERRED', '#e7e7e7', 'none', '#595959'),
    'UNKNOWN':  ('UNKNOWN', '#ffffff', '#ff6464', '#bd0a0a'),
    'GAP':      ('אין היום', '#ff6464', 'none', '#1a1a1a'),
}

_n = [0]
def nid(p='e'):
    _n[0] += 1
    return f'{p}{_n[0]}'

def rich(s):
    """escape everything, then restore the few tags a textArea accepts"""
    s = escape(s)
    for t in ('b', 'i', 'u'):
        s = s.replace(f'&lt;{t}&gt;', f'<{t}>').replace(f'&lt;/{t}&gt;', f'</{t}>')
    s = s.replace('&lt;br/&gt;', '<br/>')
    return s

class Frame:
    def __init__(self, title, x, y, w, h, fill=WHITE):
        self.id = nid('f'); self.title = title; self.x = x; self.y = y; self.w = w; self.h = h
        self.fill = fill; self.items = []

    # ---- elements (coordinates relative to frame) ----
    def rect(self, x, y, w, h, fill=WHITE, stroke=EDGE, rx=12, content=None, fs=33, fw='normal',
             color=INK, sw=2, rid=None):
        rid = rid or nid('r')
        self.items.append(dict(k='rect', id=rid, x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, rx=rx,
                               content=content, fs=fs, fw=fw, color=color, sw=sw))
        return rid

    def text(self, x, y, w, txt, fs=33, fw='normal', color=BODY, align='center', maxh=None):
        rid = nid('t')
        self.items.append(dict(k='text', id=rid, x=x, y=y, w=w, txt=txt, fs=fs, fw=fw, color=color,
                               align=align, maxh=maxh))
        return rid

    def sticky(self, x, y, txt, color='violet'):
        rid = nid('s')
        self.items.append(dict(k='sticky', id=rid, x=x, y=y, w=199, h=228, txt=txt, color=color))
        return rid

    def line(self, a, b, sa='right', sb='left', color=INK, sw=3):
        self.items.append(dict(k='line', id=nid('l'), a=a, b=b, sa=sa, sb=sb, color=color, sw=sw))

    def chip(self, x, y, status, w=None, h=44, fs=22, label=None):
        lab, fill, stroke, tc = STAT[status]
        lab = label or lab
        w = w or max(130, int(len(lab) * 15 + 44)) if status != 'GAP' else (w or 150)
        return self.rect(x, y, w, h, fill=fill, stroke=stroke, rx=22, content=lab, fs=fs, fw='bold', color=tc), w

    def chip_w(self, status):
        lab = STAT[status][0]
        return 150 if status == 'GAP' else max(130, int(len(lab) * 15 + 44))

    def table(self, x, y, title, cols, rows, scale=1):
        self.items.append(dict(k='table', id=nid('tb'), x=x, y=y, title=title, cols=cols, rows=rows, scale=scale))

    def divider(self, x1, y1, x2, y2, color=LINE):
        self.items.append(dict(k='div', id=nid('d'), x1=x1, y1=y1, x2=x2, y2=y2, color=color))


def q(s):  # attribute value
    return escape(s, {'"': '&quot;'})

def to_dsl(frames):
    out = ['<svg xmlns="http://www.w3.org/2000/svg">']
    for f in frames:
        out.append(f'<g id="{f.id}" transform="translate({f.x},{f.y})" data-frame="{q(f.title)}">')
        out.append(f'<rect data-type="frame" x="0" y="0" width="{f.w}" height="{f.h}" fill="{f.fill}" data-title="{q(f.title)}" />')
        # connectors first (z-order), then shapes
        for it in [i for i in f.items if i['k'] == 'line']:
            out.append(f'<line id="{it["id"]}" x1="0" y1="0" x2="1" y2="1" stroke="{it["color"]}" stroke-width="{it["sw"]}" '
                       f'data-arrow="end" data-shape="straight" data-start="{it["a"]}" data-end="{it["b"]}" '
                       f'data-start-side="{it["sa"]}" data-end-side="{it["sb"]}" />')
        for it in [i for i in f.items if i['k'] != 'line']:
            k = it['k']
            if k == 'rect':
                a = (f'<rect id="{it["id"]}" x="{it["x"]}" y="{it["y"]}" width="{it["w"]}" height="{it["h"]}" rx="{it["rx"]}" '
                     f'fill="{it["fill"]}" stroke="{it["stroke"]}" stroke-width="{it["sw"]}"')
                if it['content'] is not None:
                    a += (f' data-content="{q(it["content"])}" data-text-color="{it["color"]}" data-font-family="noto_sans" '
                          f'data-font-size="{it["fs"]}" data-font-weight="{"bold" if it["fw"]=="bold" else "normal"}"')
                out.append(a + ' />')
            elif k == 'text':
                h = ''
                out.append(f'<textArea id="{it["id"]}" x="{it["x"]}" y="{it["y"]}" width="{it["w"]}"{h} fill="{it["color"]}" '
                           f'font-family="noto_sans" font-size="{it["fs"]}" text-align="{it["align"]}" '
                           f'font-weight="{"bold" if it["fw"]=="bold" else "normal"}">{rich(it["txt"])}</textArea>')
            elif k == 'sticky':
                out.append(f'<rect id="{it["id"]}" data-type="sticky" x="{it["x"]}" y="{it["y"]}" width="199" height="228" '
                           f'data-color="{it["color"]}" data-content="{q(it["txt"])}" />')
            elif k == 'div':
                out.append(f'<line data-type="divider" x1="{it["x1"]}" y1="{it["y1"]}" x2="{it["x2"]}" y2="{it["y2"]}" stroke="{it["color"]}" stroke-width="2" />')
            elif k == 'table':
                th = ''.join(f'<th{c[1]}>{escape(c[0])}</th>' for c in it['cols'])
                tr = ''.join('<tr>' + ''.join(f'<td>{escape(v)}</td>' for v in r) + '</tr>' for r in it['rows'])
                out.append(f'<foreignObject id="{it["id"]}" x="{it["x"]}" y="{it["y"]}" width="1200" height="600" data-type="table" '
                           f'data-title="{q(it["title"])}" data-scale="{it["scale"]}"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></foreignObject>')
        out.append('</g>')
    out.append('</svg>')
    return '\n'.join(out)


STICKY = {'violet': '#e1d5f5', 'yellow': '#fff9b1'}

def to_html(frames, scale=1.0):
    css = """
body{margin:0;background:#c9c9c9;font-family:'Noto Sans','FreeSans','Liberation Sans','DejaVu Sans',sans-serif}
.fr{position:absolute;box-sizing:border-box;border:2px solid #b0b0b0}
.el{position:absolute;box-sizing:border-box;direction:rtl}
.rc{display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.35;overflow:visible}
.tx{line-height:1.35;white-space:normal}
.ttl{position:absolute;font-size:30px;color:#777;direction:ltr}
"""
    parts = [f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>']
    for f in frames:
        parts.append(f'<div class="fr" id="{f.id}" style="left:{f.x}px;top:{f.y}px;width:{f.w}px;height:{f.h}px;background:{f.fill}">')
        pos = {i['id']: i for i in f.items if 'x' in i and i['k'] in ('rect', 'sticky')}
        for it in f.items:
            k = it['k']
            if k == 'rect':
                st = (f'left:{it["x"]}px;top:{it["y"]}px;width:{it["w"]}px;height:{it["h"]}px;background:{it["fill"]};'
                      f'border:{0 if it["stroke"]=="none" else it["sw"]}px solid {it["stroke"] if it["stroke"]!="none" else "transparent"};'
                      f'border-radius:{it["rx"]}px;')
                if it['content'] is not None:
                    st += f'font-size:{it["fs"]}px;font-weight:{"700" if it["fw"]=="bold" else "400"};color:{it["color"]};padding:0 8px'
                    parts.append(f'<div class="el rc" data-chk="rect" style="{st}">{escape(it["content"])}</div>')
                else:
                    parts.append(f'<div class="el" style="{st}"></div>')
            elif k == 'text':
                st = (f'left:{it["x"]}px;top:{it["y"]}px;width:{it["w"]}px;font-size:{it["fs"]}px;color:{it["color"]};'
                      f'font-weight:{"700" if it["fw"]=="bold" else "400"};text-align:{it["align"]}')
                mh = it['maxh'] or 0
                parts.append(f'<div class="el tx" data-chk="text" data-maxh="{mh}" style="{st}">{rich(it["txt"])}</div>')
            elif k == 'sticky':
                parts.append(f'<div class="el rc" data-chk="rect" style="left:{it["x"]}px;top:{it["y"]}px;width:199px;height:228px;background:{STICKY.get(it["color"],"#e1d5f5")};font-size:26px;padding:12px;color:#1a1a1a">{escape(it["txt"])}</div>')
            elif k == 'line':
                a = pos[it['a']]; b = pos[it['b']]
                x1 = a['x'] + a['w']; y1 = a['y'] + a['h'] / 2; x2 = b['x']; y2 = b['y'] + b['h'] / 2
                parts.append(f'<svg class="el" style="left:0;top:0;width:{f.w}px;height:{f.h}px;pointer-events:none"><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{it["color"]}" stroke-width="{it["sw"]}"/><polygon points="{x2},{y2} {x2-14},{y2-8} {x2-14},{y2+8}" fill="{it["color"]}"/></svg>')
            elif k == 'div':
                parts.append(f'<div class="el" style="left:{it["x1"]}px;top:{it["y1"]}px;width:{it["x2"]-it["x1"] or 2}px;height:{it["y2"]-it["y1"] or 2}px;background:{it["color"]}"></div>')
            elif k == 'table':
                th = ''.join(f'<th style="border:1px solid #ccc;padding:8px;background:#f0f0f0">{escape(c[0])}</th>' for c in it['cols'])
                tr = ''.join('<tr>' + ''.join(f'<td style="border:1px solid #ddd;padding:8px">{escape(v)}</td>' for v in r) + '</tr>' for r in it['rows'])
                parts.append(f'<table class="el" style="left:{it["x"]}px;top:{it["y"]}px;font-size:22px;border-collapse:collapse;width:2200px;background:#fff"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>')
        parts.append('</div>')
    parts.append('</body></html>')
    return '\n'.join(parts)
