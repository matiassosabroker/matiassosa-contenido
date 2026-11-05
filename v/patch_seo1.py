import os, re, shutil
ROOT='/home/matiassosacom/public_html'; V=ROOT+'/resources/views'
G="request('preview') === 'ms-preview-2026'"
log=[]
def rd(p): return open(p,encoding='utf-8').read()
def patch(path, fn, marker):
    p=V+'/'+path; s=rd(p)
    if marker in s: log.append('YA APLICADO '+path); return
    b=p+'.antes-seo1'
    if not os.path.exists(b): shutil.copy(p,b)
    n=fn(s)
    if n is None: log.append('FALLO '+path); return
    open(p,'w',encoding='utf-8').write(n); os.system('chown matiassosacom:matiassosacom '+p); log.append('OK '+path)

# home: segundo h1 -> h2 (misma clase = mismo look)
def f_home(s):
    k='<x-text type="h1" variant="text_white text_size_72 text_secondary"'
    parts=s.split(k)
    if len(parts)<3: return None
    return parts[0]+k+parts[1]+'<x-text :type="('+G+") ? 'h2' : 'h1'\" variant=\"text_white text_size_72 text_secondary\""+k.join(parts[2:]) if False else parts[0]+k+parts[1]+'<x-text :type="('+G+") ? 'h2' : 'h1'\" variant=\"text_white text_size_72 text_secondary\""+(k.join(parts[2:]))
patch('front/pages/index.blade.php', f_home, "? 'h2' : 'h1'")

# tasacion: el h1 de desktop-oculto -> h2
def f_tas(s):
    rx=re.compile(r'(<x-text\s+)type="h1"(\s+variant="hide-desktop section_title)')
    if not rx.search(s): return None
    return rx.sub(lambda m: m.group(1)+':type="('+G+") ? 'h2' : 'h1'\""+m.group(2), s, 1)
patch('front/pages/tasacion.blade.php', f_tas, "? 'h2' : 'h1'")

# contacto: h1 oculto visualmente
def f_con(s):
    m=re.search(r"@section\('content'\)\s*\n", s)
    if not m: return None
    h=("@if ("+G+")\n<h1 style=\"position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0\">Contacto | Mat&iacute;as Sosa Broker Inmobiliario en Mar del Plata</h1>\n@endif\n")
    return s[:m.end()]+h+s[m.end():]
patch('front/pages/contacto.blade.php', f_con, 'position:absolute;width:1px;height:1px')

# viewport: permitir zoom
def f_vp(s):
    if 'user-scalable=no, ' not in s: return None
    return s.replace('user-scalable=no, ', "{{ ("+G+") ? '' : 'user-scalable=no, ' }}",1)
patch('front/layouts/master.blade.php', f_vp, "? '' : 'user-scalable=no, '")

# footer: aria-label en redes
def f_foot(s):
    rx=re.compile(r'<a target="_blank" href="(https?://[^"]*(instagram|facebook|youtube|tiktok|linkedin|wa\.me|whatsapp)[^"]*)"')
    names={'instagram':'Instagram','facebook':'Facebook','youtube':'YouTube','tiktok':'TikTok','linkedin':'LinkedIn','wa.me':'WhatsApp','whatsapp':'WhatsApp'}
    if not rx.search(s): return None
    return rx.sub(lambda m: m.group(0)+" {!! ("+G+") ? 'aria-label=\""+names[m.group(2)]+"\"' : '' !!}", s)
patch('front/components/footer.blade.php', f_foot, "aria-label=")
print('\n'.join(log))
