import os, re

BASE = '/ojo-site/assets/'

# Domínios CDN para localizar
CDN = [
    'images.squarespace-cdn.com',
    'static1.squarespace.com',
    'static2.squarespace.com',
    'assets.squarespace.com',
    'definitions.sqspcdn.com',
    'use.typekit.net',
    'p.typekit.net',
    'file.squarespace-cdn.com',
]

def fix_html(content):
    # Corrigir protocol-relative URLs (//cdn.../...)
    for cdn in CDN:
        content = re.sub(
            r'(["\'(\s])\/\/' + re.escape(cdn) + r'([^"\')\s>]*)',
            lambda m: m.group(1) + BASE + cdn + m.group(2).split('?')[0],
            content
        )
    # Corrigir URLs absolutas https:// ainda apontando para CDN
    for cdn in CDN:
        content = re.sub(
            r'(["\'(\s])https?:\/\/' + re.escape(cdn) + r'([^"\')\s>]*)',
            lambda m: m.group(1) + BASE + cdn + m.group(2).split('?')[0],
            content
        )
    # Corrigir URLs corrompidas (CDN com /ojo-site/assets/ no meio)
    for cdn in CDN:
        content = content.replace(
            'https://' + cdn + '/' + BASE.strip('/') + '/',
            BASE + cdn + '/'
        )
    return content

count = 0
for root, dirs, files in os.walk('.'):
    # Pular a pasta assets
    dirs[:] = [d for d in dirs if d != 'assets']
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                original = fh.read()
            fixed = fix_html(original)
            if fixed != original:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(fixed)
                count += 1

print(f'{count} arquivos corrigidos.')