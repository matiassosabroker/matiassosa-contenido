import os
ROOT='/home/matiassosacom/public_html'
log=[]
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

print('\n'.join(log))
