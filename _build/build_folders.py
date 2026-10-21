"""Build the six short-address pages (/msf/<app>/index.html) from ../index.html.
index.html is the only source. Run from the repo root:  python3 _build/build_folders.py
Each copy gets its own static header (title, description, Open Graph) so link previews
in Messages / Gmail / WhatsApp show the right application. Nothing else changes."""
import html, os, re, sys

SITE = 'https://sazv-private-rebuild.github.io/msf/'
IMAGE = SITE + 'msf-logo-640.png'
APPS = [
    ('residential', 'Residential Mortgage Application', 'Purchase or refinance a home — secure application, about 6 minutes on your phone.'),
    ('commercial', 'Commercial Loan Application', 'Commercial property financing from $1M to $70M — secure application, about 8 minutes.'),
    ('construction', 'Construction Financing Application', 'Ground-up construction and development financing — secure application, about 8 minutes.'),
    ('private', 'Private / Fix & Flip Application', 'Bridge, fix-and-flip and rental financing for investors — secure application, about 7 minutes.'),
    ('multifamily', 'Multifamily Loan Application', 'Financing for apartment buildings with 5 or more units — secure application, about 8 minutes.'),
    ('dscr', 'DSCR Calculator', 'Instant DSCR, NOI and loan estimate for an income property. Nothing is saved or sent.'),
]

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
