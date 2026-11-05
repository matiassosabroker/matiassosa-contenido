import os, re, shutil, sys

ROOT = '/home/matiassosacom/public_html'
V = ROOT + '/resources/views'
G = "request('preview') === 'ms-preview-2026'"
log = []


def rd(p):
    return open(p, encoding='utf-8').read()


def wr(p, s):
    open(p, 'w', encoding='utf-8').write(s)


def bak(p):
    b = p + '.antes-simples'
    if not os.path.exists(b):
        shutil.copy(p, b)


def patch(path, fn, marker):
    p = V + '/' + path
    s = rd(p)
    if marker in s:
        log.append('YA APLICADO  ' + path)
        return
    bak(p)
    n = fn(s)
    if n is None:
        log.append('FALLO       ' + path)
        return
    wr(p, n)
    log.append('OK           ' + path)


# 1) typo footer: "Poltica" -> "Política" (solo preview)
def f_footer(s):
    if 'Poltica' not in s:
        return None
    return s.replace('Poltica', "{!! (" + G + ") ? 'Pol&iacute;tica' : 'Poltica' !!}")
patch('front/components/footer.blade.php', f_footer, "'Pol&iacute;tica'")

# 2) console.log de depuracion (tiempo de render) fuera en preview
rx = re.compile(r"echo\s+'console\.log\('\.\(\$endTime - \$starttime\)\.'\)';")
for pg in ('landing', 'busqueda-nuevo', 'busqueda'):
    def f_log(s):
        if not rx.search(s):
            return None
        return rx.sub(lambda m: "if (!(" + G + ")) { " + m.group(0) + " }", s)
    patch('front/pages/%s.blade.php' % pg, f_log, "if (!(" + G + ")) { echo 'console.log")

# 3) direccion con &quot; en tarjetas
def f_card(s):
    old = "content=\"{{ $cardData['fake_address'] }}\""
    if old not in s:
        return None
    new = ("content=\"{{ (" + G + ") ? html_entity_decode(html_entity_decode((string) ($cardData['fake_address'] ?? ''), "
           "ENT_QUOTES | ENT_HTML5), ENT_QUOTES | ENT_HTML5) : $cardData['fake_address'] }}\"")
    return s.replace(old, new)
patch('front/components/propertyCard.blade.php', f_card, "ENT_QUOTES | ENT_HTML5) : $cardData['fake_address']")

# 4) tabla del blog desbordada en celular
def f_blog(s):
    m = re.search(r"@section\('content'\)\s*\n", s)
    if not m:
        return None
    css = ("@if (" + G + ")\n<style>.blog-body table{display:block;max-width:100%;overflow-x:auto;"
           "-webkit-overflow-scrolling:touch}.blog-body img{max-width:100%;height:auto}</style>\n@endif\n")
    return s[:m.end()] + css + s[m.end():]
patch('front/pages/blog-post.blade.php', f_blog, ".blog-body table{display:block")

# 5) og:image + twitter card + typo IE=edge (master)
def f_master(s):
    key = '<meta property="og:url" content="{{ $seoCanonical }}" />'
    if key not in s:
        return None
    add = (key + "\n@if (" + G + ")\n"
           "@php $__og = trim($__env->yieldContent('og_image')); if ($__og === '') { $__og = asset('front/images/og-default.jpg'); } @endphp\n"
           "    <meta property=\"og:image\" content=\"{{ $__og }}\" />\n"
           "    <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
           "    <meta name=\"twitter:image\" content=\"{{ $__og }}\" />\n"
           "@endif")
    s = s.replace(key, add, 1)
    s = s.replace('content="IE-edge"', 'content="{{ (' + G + ") ? 'IE=edge' : 'IE-edge' }}\"", 1)
    return s
patch('front/layouts/master.blade.php', f_master, 'og:image')

# 6) og_image en la ficha: primera foto
def f_det(s):
    m = re.search(r"@section\('keywords', ''\)\s*\n", s)
    if not m:
        return None
    return s[:m.end()] + "@section('og_image', $propiedad['images'][0]['url'] ?? '')\n" + s[m.end():]
patch('front/pages/propiedad-detalle.blade.php', f_det, "@section('og_image'")

# 7) pagina 404 propia (preview) + comportamiento actual intacto
err = V + '/errors'
os.makedirs(err, exist_ok=True)
p404 = err + '/404.blade.php'
if not os.path.exists(p404):
    wr(p404, "@if (" + G + ")\n@include('errors.404-nuevo')\n@else\n{!! view('errors::404', ['exception' => $exception])->render() !!}\n@endif\n")
    log.append('OK           errors/404.blade.php')
else:
    log.append('YA EXISTE    errors/404.blade.php')

html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,follow">
<title>No encontramos esa p&aacute;gina | Mat&iacute;as Sosa Broker Inmobiliario</title>
<style>
*{box-sizing:border-box}body{margin:0;min-height:100vh;display:flex;flex-direction:column;background:#141414;color:#fff;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.nf-top{padding:28px 32px}.nf-top img{height:34px;width:auto;display:block}
.nf-main{flex:1;display:flex;align-items:center;justify-content:center;padding:24px}
.nf-box{max-width:640px;text-align:left}
.nf-code{font-size:14px;letter-spacing:.32em;color:#C9A66B;font-weight:600;margin:0 0 18px}
.nf-box h1{font-size:clamp(34px,6vw,56px);line-height:1.05;margin:0 0 18px;font-weight:700}
.nf-box p{font-size:18px;line-height:1.55;color:#cfcfca;margin:0 0 34px}
.nf-btns{display:flex;flex-wrap:wrap;gap:12px}
.nf-btns a{display:inline-flex;align-items:center;justify-content:center;min-height:50px;padding:0 26px;border-radius:999px;font-weight:600;font-size:16px;text-decoration:none;border:1px solid #fff;color:#fff;transition:.2s}
.nf-btns a.main{background:#EEEEED;color:#141414;border-color:#EEEEED}
.nf-btns a.main:hover{background:#fff;border-color:#C9A66B}
.nf-btns a:hover{border-color:#C9A66B}
.nf-foot{padding:22px 32px;color:#8d8d88;font-size:13px}
</style>
</head>
<body>
<div class="nf-top"><a href="{{ url('/') }}"><img src="{{ asset('front/images/logo-matiassosa-blanco.svg') }}" alt="Mat&iacute;as Sosa Broker Inmobiliario"></a></div>
<div class="nf-main"><div class="nf-box">
<p class="nf-code">ERROR 404</p>
<h1>No encontramos lo que buscabas</h1>
<p>Puede que el link haya cambiado o que la propiedad ya no est&eacute; disponible. Mir&aacute; las que tenemos hoy o escribinos y te ayudamos a encontrar la ideal.</p>
<div class="nf-btns">
<a class="main" href="{{ url('/comprar-alquilar') }}">Ver propiedades</a>
<a href="{{ url('/') }}">Ir al inicio</a>
<a href="https://wa.me/5492233447092?text=Hola%21%20Llegu%C3%A9%20a%20una%20p%C3%A1gina%20que%20no%20existe%20en%20la%20web%20y%20quiero%20consultar." rel="noopener">Escribinos por WhatsApp</a>
</div></div></div>
<div class="nf-foot">Mat&iacute;as Sosa Broker Inmobiliario &middot; Mar del Plata</div>
</body>
</html>
"""
pn = err + '/404-nuevo.blade.php'
wr(pn, html)
log.append('OK           errors/404-nuevo.blade.php')

# 8) imagen og por defecto
og = ROOT + '/public/front/images/og-default.jpg'
try:
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), (241, 241, 239))
    d = ImageDraw.Draw(im)
    logo = Image.open(ROOT + '/public/front/images/Logo-matiassosa-negro.png').convert('RGBA')
    lw = 760
    lh = int(logo.height * lw / logo.width)
    logo = logo.resize((lw, lh))
    im.paste(logo, ((W - lw) // 2, 190), logo)
    d.rectangle([(W // 2 - 60, 190 + lh + 38), (W // 2 + 60, 190 + lh + 42)], fill=(201, 166, 107))
    fp = None
    for c in ('/usr/share/fonts/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf', '/usr/share/fonts/liberation/LiberationSans-Regular.ttf'):
        if os.path.exists(c):
            fp = c
            break
    if fp:
        ft = ImageFont.truetype(fp, 34)
        t = 'Propiedades en venta y alquiler en Mar del Plata'
        tw = d.textlength(t, font=ft)
        d.text(((W - tw) / 2, 190 + lh + 70), t, fill=(20, 20, 20), font=ft)
    im.save(og, 'JPEG', quality=88)
    os.system('chown matiassosacom:matiassosacom ' + og)
    log.append('OK           og-default.jpg %d bytes' % os.path.getsize(og))
except Exception as e:
    log.append('FALLO og-default.jpg: %r' % (e,))

os.system('chown -R matiassosacom:matiassosacom ' + V)
print('\n'.join(log))
