"""Sinh docs/index.html (English) và docs/<lang>/index.html từ tools/lang/index.template.html + tools/lang/<lang>.json.
Chạy: python3 tools/build_site.py   (chạy lại sau khi sửa bản mẫu, chuỗi dịch hoặc thêm ngôn ngữ).
Chuỗi gốc là en.json; mọi ngôn ngữ khác phải có đủ cùng các khoá (script dừng và báo khoá thiếu)."""
import datetime, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANG_DIR = os.path.join(HERE, 'lang')
ROOT = os.path.join(HERE, '..', 'docs')
SITE = 'https://keel.keellabs.dev/'
TODAY = datetime.date.today().isoformat()
# (thư mục, mã hreflang, tên hiển thị, og:locale, tệp chuỗi)
LANGS = [
    ('', 'en', 'English', 'en_US', 'en'),
    ('vi/', 'vi', 'Tiếng Việt', 'vi_VN', 'vi'),
    ('zh/', 'zh-Hans', '简体中文', 'zh_CN', 'zh'),
    ('ja/', 'ja', '日本語', 'ja_JP', 'ja'),
    ('ko/', 'ko', '한국어', 'ko_KR', 'ko'),
    ('es/', 'es', 'Español', 'es_ES', 'es'),
    ('pt/', 'pt-BR', 'Português (Brasil)', 'pt_BR', 'pt'),
    ('ru/', 'ru', 'Русский', 'ru_RU', 'ru'),
]
FONT_LATIN = ('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700;12..96,800'
              '&family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap')
# Bricolage và Hanken không có chữ Kirin, nên tiếng Nga dùng Manrope.
FONT_CYRILLIC = ('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800'
                 '&family=JetBrains+Mono:wght@400;600&display=swap')
GLOBE = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 1 0 0 20 '
         '10 10 0 0 0 0-20Zm6.9 6h-3a15.7 15.7 0 0 0-1.4-3.6A8 8 0 0 1 18.9 8ZM12 4c.8 1.1 1.5 2.5 1.9 4h-3.8c.4-1.5 1.1-2.9 '
         '1.9-4ZM4.3 14a8.2 8.2 0 0 1 0-4h3.4a16.5 16.5 0 0 0 0 4H4.3Zm.8 2h3a15.7 15.7 0 0 0 1.4 3.6A8 8 0 0 1 5.1 16Zm3-8h-3'
         'a8 8 0 0 1 4.4-3.6A15.7 15.7 0 0 0 8.1 8ZM12 20c-.8-1.1-1.5-2.5-1.9-4h3.8c-.4 1.5-1.1 2.9-1.9 4Zm2.3-6H9.7a14.7 14.7 0 '
         '0 1 0-4h4.6a14.7 14.7 0 0 1 0 4Zm.3 5.6a15.7 15.7 0 0 0 1.4-3.6h3a8 8 0 0 1-4.4 3.6Zm1.7-5.6a16.5 16.5 0 0 0 0-4h3.4'
         'a8.2 8.2 0 0 1 0 4h-3.4Z"/></svg>')


def safe_json(v):
    """JSON để nhúng trong <script>/<style>: không cho chuỗi dịch đóng thẻ sớm bằng '</'."""
    return json.dumps(v, ensure_ascii=False).replace('</', '<\\/')


def load(name):
    with open(os.path.join(LANG_DIR, name + '.json'), encoding='utf-8') as f:
        return json.load(f)


def page_url(d):
    return SITE + d


def rel(src, dst):
    """Đường dẫn tương đối giữa hai thư mục ngôn ngữ (đều kết thúc bằng / hoặc rỗng)."""
    up = '../' if src else ''
    return (up + dst) or './'


def build(d, code, label, og, fname, strings, template):
    base = '../' if d else ''
    lang_attr = code
    alts = '\n'.join(f'<link rel="alternate" hreflang="{c}" href="{page_url(dd)}">' for dd, c, _, _, _ in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{page_url("")}">'
    ogs = f'<meta property="og:locale" content="{og}">\n' + '\n'.join(
        f'<meta property="og:locale:alternate" content="{o}">' for dd, _, _, o, _ in LANGS if dd != d)
    cur = ' aria-current="page"'
    items = ''.join(
        f'<li><a href="{rel(d, dd)}" hreflang="{c}" lang="{c}"{cur if dd == d else ""}>{lab}</a></li>'
        for dd, c, lab, _, _ in LANGS)
    menu = (f'<details class="lang-menu"><summary aria-label="{html.escape(strings["lang_label"])} / Language">{GLOBE}<span>{html.escape(strings["lang_label"])}</span></summary>'
            f'<ul>{items}</ul></details>')
    ld = {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'Keel', 'url': page_url(d),
        'description': strings['ld_description'], 'applicationCategory': 'DeveloperApplication',
        'operatingSystem': 'macOS, Windows, Linux', 'inLanguage': code, 'image': SITE + 'img/og.png',
        'downloadUrl': page_url(d) + '#download', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
        'publisher': {'@type': 'Organization', 'name': 'Keel Labs', 'url': 'https://keellabs.dev/'},
    }
    i18n = {'download_for': strings['js_download_for'], 'release_note': strings['js_release_note']}
    extra = {
        'lang': lang_attr, 'canonical': page_url(d), 'hreflang': '\n' + alts + '\n', 'oglocale': '\n' + ogs + '\n',
        'ldjson': safe_json(ld), 'base': base, 'home': '/' + d if d else '/',
        'fonts': FONT_CYRILLIC if code == 'ru' else FONT_LATIN, 'langmenu': menu,
        'i18n': safe_json(i18n),
    }

    def sub(m):
        kind, key = m.group(1), m.group(2)
        if kind is None:
            return extra[key]
        v = strings[key]
        return {'t': v, 'a': html.escape(v, quote=True), 'x': html.escape(v, quote=False)}[kind]

    out = re.sub(r'\{\{(?:([tax]):)?([A-Za-z0-9_]+)\}\}', sub, template)
    # --your-system: nhãn "Máy của bạn" của thẻ hệ điều hành đang dùng (CSS không đọc được chuỗi từ HTML).
    out = out.replace('</head>', f'<style>:root {{ --your-system: {safe_json(strings["your_system"])}; }}</style>\n</head>', 1)
    path = os.path.join(ROOT, d, 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(out)


def main():
    with open(os.path.join(LANG_DIR, 'index.template.html'), encoding='utf-8') as f:
        template = f.read()
    en = load('en')
    problems = []
    loaded = []
    sig = lambda v: (sorted(re.findall(r'</?[a-z]+', v)), sorted(re.findall(r'\{[a-z]+\}', v)),
                     sorted(re.findall(r'(?:href|class|data-[a-z-]+)="[^"]*"|data-version', v)))
    for d, code, label, og, fname in LANGS:
        s = load(fname)
        missing = sorted(set(en) - set(s))
        extra = sorted(set(s) - set(en))
        if missing or extra:
            problems.append(f'{fname}: thiếu {missing} thừa {extra}')
            continue
        for k, v in en.items():  # giữ nguyên thẻ HTML, giá trị href/class và chỗ giữ chỗ {…} của bản gốc
            if sig(v) != sig(s[k]):
                problems.append(f'{fname}.{k}: thẻ, href hoặc chỗ giữ chỗ khác bản gốc')
            if '<' in en[k]:
                if s[k].count('<') != en[k].count('<') or s[k].count('&') != en[k].count('&'):
                    problems.append(f'{fname}.{k}: số ký tự < hoặc & khác bản gốc')
            elif '<' in s[k]:
                problems.append(f'{fname}.{k}: chuỗi thuần không được chứa <')
        loaded.append((d, code, label, og, fname, s))
    if problems:  # không sinh trang nào khi còn lỗi, để khỏi để lại trang hỏng
        print('\n'.join(problems)); sys.exit(1)
    for d, code, label, og, fname, s in loaded:
        build(d, code, label, og, fname, s, template)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for d, _, _, _, _ in LANGS:
        links = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{c}" href="{page_url(dd)}"/>' for dd, c, _, _, _ in LANGS)
        links += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url("")}"/>'
        out.append(f'  <url><loc>{page_url(d)}</loc><lastmod>{TODAY}</lastmod>{links}\n  </url>')
    out.append('</urlset>')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    print('xong')


if __name__ == '__main__':
    main()
