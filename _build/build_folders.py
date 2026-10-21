"""Build the six short-address pages (/msf/<app>/index.html) from ../index.html.
index.html is the only source. Run from the repo root:  python3 _build/build_folders.py
Each copy gets its own static header (title, description, Open Graph) so link previews
in Messages / Gmail / WhatsApp show the right application. Nothing else changes."""
import html, os, re, sys

SITE = 'https://sazv-private-rebuild.github.io/msf/'
IMAGE = SITE + 'msf-logo-640.png'
APPS = [
    ('residential', 'Residential Application, Mortgages', 'Purchase or refinance a home — secure application, about 6 minutes on your phone.'),
    ('commercial', 'Commercial $1M-$70M — Commercial Buildings, Multifamily, Mixed Use, Retail, Office, Industrial, Nursing Homes', 'Commercial and multifamily financing from $1M to $70M — secure application, about 8 minutes.'),
    ('construction', 'Ground-Up Construction and Development Financing', 'Ground-up construction and development financing — secure application, about 8 minutes.'),
    ('private', 'Private Lending, Hard Money, Fix and Flips', 'Private, hard money and fix-and-flip loans for investors, with DSCR calculator — about 7 minutes.'),
    ('dscr', 'DSCR Calculator', 'Instant DSCR, NOI and loan estimate for an income property. Nothing is saved or sent.'),
    ('programs', 'All Programs', 'Every My Source Finance application in one place, plus the DSCR calculator.'),
]
REDIRECTS = [('multifamily', 'commercial')]  # Multifamily is part of Commercial

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
for key, title, desc in APPS:
    full = title + ' — My Source Finance'
    e = lambda v: html.escape(v, quote=True)
    head = ('<meta charset="utf-8">\n<base href="../">\n'
            '<meta name="msf-app" content="%s">\n' % key +
            '<meta property="og:type" content="website">\n'
            '<meta property="og:site_name" content="My Source Finance">\n'
            '<meta property="og:title" content="%s">\n' % e(full) +
            '<meta property="og:description" content="%s">\n' % e(desc) +
            '<meta property="og:url" content="%s%s/">\n' % (SITE, key) +
            '<meta property="og:image" content="%s">\n' % IMAGE +
            '<meta property="og:image:width" content="640">\n<meta property="og:image:height" content="325">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="twitter:title" content="%s">\n' % e(full) +
            '<meta name="twitter:description" content="%s">\n' % e(desc))
    out = src
    for old, new in [('<meta charset="utf-8">\n', head),
                     ('<title>My Source Finance — Loan Applications</title>', '<title>%s</title>' % e(full)),
                     ]:
        if out.count(old) != 1: sys.exit('build failed: %r' % old)
        out = out.replace(old, new)
    out, n = re.subn(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % e(desc), out)
    if n != 1: sys.exit('build failed: description')
    os.makedirs(os.path.join(root, key), exist_ok=True)
    open(os.path.join(root, key, 'index.html'), 'w', encoding='utf-8').write(out)
    print('built', key + '/')
for old, new in REDIRECTS:
    t = [x for x in APPS if x[0] == new][0]
    page = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
            '<title>%s — My Source Finance</title>' % html.escape(t[1]) +
            '<meta property="og:site_name" content="My Source Finance"><meta property="og:title" content="%s — My Source Finance">' % html.escape(t[1], quote=True) +
            '<meta property="og:description" content="%s"><meta property="og:image" content="%s"><meta property="og:url" content="%s%s/">' % (html.escape(t[2], quote=True), IMAGE, SITE, new) +
            '<meta http-equiv="refresh" content="0; url=../%s/"><script>location.replace("../%s/" + location.search)</script></head>' % (new, new) +
            '<body><p><a href="../%s/">Open the application</a></p></body></html>' % new)
    os.makedirs(os.path.join(root, old), exist_ok=True)
    open(os.path.join(root, old, 'index.html'), 'w', encoding='utf-8').write(page)
    print('redirect', old + '/ ->', new + '/')
