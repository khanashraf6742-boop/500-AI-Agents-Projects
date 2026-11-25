"""Tiny SVG helpers for flowcharts/timelines. All text comes from the source guide."""
from html import escape
import textwrap

def wrap(text, width):
    return textwrap.wrap(text, width) or ['']

_N = [0]
_ID = ['ar0']

def svg_open(w, h, title):
    _N[0] += 1
    _ID[0] = f'ar{_N[0]}'
    return (f'<div class="svgwrap"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}" '
            f'xmlns="http://www.w3.org/2000/svg" style="min-width:{min(w,640)}px">'
            f'<defs><marker id="{_ID[0]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0 0L10 5L0 10z" class="arrowhead"/></marker></defs>'
            f'<title>{escape(title)}</title>')

def svg_close():
    return '</svg></div>'

def box(x, y, w, h, text, kind='n', size=14, chars=None, bold_first=False):
    """kind: n=neutral, s=start/end, d=decision(diamond), g=good(green), r=red/warn, a=amber, b=blue"""
    chars = chars or max(8, int(w / (size * 0.56)))
    lines = []
    for para in text.split('\n'):
        lines += wrap(para, chars)
    lh = size * 1.25
    ty = y + h / 2 - (len(lines) - 1) * lh / 2 + size * 0.35
    out = []
    if kind == 'd':
        cy = y + h / 2
        k_ = min(26, w / 8)
        out.append(f'<polygon points="{x+k_},{y} {x+w-k_},{y} {x+w},{cy} {x+w-k_},{y+h} {x+k_},{y+h} {x},{cy}" class="nd d"/>')
    else:
        rx = h / 2 if kind == 's' else 8
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="nd {kind}"/>')
    for i, ln in enumerate(lines):
        wt = ' font-weight="700"' if (bold_first and i == 0) else ''
        out.append(f'<text x="{x+w/2}" y="{ty+i*lh:.1f}" text-anchor="middle" font-size="{size}"{wt}>{escape(ln)}</text>')
    return ''.join(out)

def arrow(x1, y1, x2, y2, label='', dx=6, dy=-6, size=12):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="ln" marker-end="url(#{_ID[0]})"/>'
    if label:
        s += f'<text x="{(x1+x2)/2+dx}" y="{(y1+y2)/2+dy}" font-size="{size}" class="lbl">{escape(label)}</text>'
    return s

def poly(points, label='', lx=0, ly=0, size=12):
    pts = ' '.join(f'{x},{y}' for x, y in points)
    s = f'<polyline points="{pts}" fill="none" class="ln" marker-end="url(#{_ID[0]})"/>'
    if label:
        s += f'<text x="{lx}" y="{ly}" font-size="{size}" class="lbl">{escape(label)}</text>'
    return s

def text(x, y, t, size=14, anchor='middle', cls='', bold=False):
    wt = ' font-weight="700"' if bold else ''
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" class="{cls}"{wt}>{escape(t)}</text>'

def vflow(steps, title, w=760, bw=520, bh=58, gap=34, size=14, labels=None):
    """Simple vertical flowchart. steps: list of (text, kind). labels: optional list of edge labels."""
    h = len(steps) * (bh + gap) - gap + 20
    x = (w - bw) / 2
    o = [svg_open(w, h, title)]
    ar = []
    y = 10
    for i, (t, k) in enumerate(steps):
        o.append(box(x, y, bw, bh, t, k, size))
        if i < len(steps) - 1:
            lab = labels[i] if labels and i < len(labels) else ''
            ar.append(arrow(w / 2, y + bh, w / 2, y + bh + gap, lab, dx=10, dy=4))
        y += bh + gap
    o += ar
    o.append(svg_close())
    return ''.join(o)

def hbar(items, title, unit='Rs.', w=760, row=40, maxv=None, color='b', label_w=210, fmt=None):
    """Horizontal bar chart. items: list of (label, value, display)."""
    maxv = maxv or max(v for _, v, _ in items)
    h = len(items) * row + 20
    bw = w - label_w - 300
    o = [svg_open(w, h, title)]
    for i, (lab, v, disp) in enumerate(items):
        y = 10 + i * row
        o.append(text(label_w - 10, y + row / 2 + 4, lab, 14, 'end'))
        o.append(f'<rect x="{label_w}" y="{y+6}" width="{bw*v/maxv:.1f}" height="{row-14}" rx="5" class="bar {color}"/>')
        o.append(text(label_w + bw * v / maxv + 8, y + row / 2 + 4, disp, 14, 'start', bold=True))
    o.append(svg_close())
    return ''.join(o)

def _lines(t, w, size, pad=0):
    chars = max(8, int((w - pad) / (size * 0.56)))
    n = 0
    for para in t.split('\n'):
        n += len(wrap(para, chars))
    return n

def _need(t, w, size, minh, pad=0):
    return max(minh, _lines(t, w, size, pad) * size * 1.25 + 26)

def spine(nodes, title, w=920, sw=330, side_w=400, bh=56, gap=36, size=14, last_kind='g'):
    """Decision spine. nodes: list of dicts {t, k, side:(text,kind,label) or None, down_label}
    Main spine runs down the left; side outcome boxes branch right."""
    sx = 20
    rows = []
    for n in nodes:
        k = n.get('k', 'n')
        hn = _need(n['t'], sw, size, bh, 60 if k == 'd' else 0)
        hs = _need(n['side'][0], side_w, size - 1, bh) if n.get('side') else 0
        rows.append((hn, hs, max(hn, hs)))
    h = sum(r[2] for r in rows) + gap * (len(nodes) - 1) + 24
    o = [svg_open(w, h, title)]
    ar = []
    y = 12
    for i, n in enumerate(nodes):
        k = n.get('k', 'n')
        hn, hs, hh = rows[i]
        o.append(box(sx, y + (hh - hn) / 2, sw, hn, n['t'], k, size))
        cy = y + hh / 2
        if n.get('side'):
            st, sk, lab = n['side']
            ar.append(arrow(sx + sw, cy, sx + sw + 70, cy, lab, dx=-4, dy=-6))
            o.append(box(sx + sw + 70, y + (hh - hs) / 2, side_w, hs, st, sk, size - 1))
        if i < len(nodes) - 1:
            ar.append(arrow(sx + sw / 2, y + (hh + hn) / 2, sx + sw / 2, y + hh + gap, n.get('down_label', ''), dx=8, dy=4))
        y += hh + gap
    o += ar
    o.append(svg_close())
    return ''.join(o)
