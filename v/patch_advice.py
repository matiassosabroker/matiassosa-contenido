#!/usr/bin/env python3
# Componente personalizedAdvice: tarjeta nueva (solo preview)
import shutil
P = 'resources/views/front/components/personalizedAdvice.blade.php'
old = open(P, encoding='utf-8').read()
shutil.copy(P, P + '.antes-tarjeta')
if 'hr-adv-card' in old:
    raise SystemExit('ya parcheado')

NEW = r'''@php
$hrWa = 'https://wa.me/5492233447092?text=Hola%21%20No%20encontr%C3%A9%20la%20propiedad%20que%20busco%20en%20la%20web%20y%20quiero%20que%20me%20ayuden%20a%20encontrarla.';
@endphp
<style>
.hr-adv{background:#EEEEED;padding:24px 0 80px}
.hr-adv-card{background:#fff;border-radius:20px;padding:44px 48px;display:flex;gap:32px;align-items:center;justify-content:space-between;border-left:6px solid #C9A66B;box-shadow:0 10px 30px rgba(0,0,0,.06)}
.hr-adv-card h3{font-size:clamp(24px,2.6vw,34px);font-weight:800;letter-spacing:-.02em;line-height:1.12;margin:0 0 12px;color:#1B1B1B}
.hr-adv-card p{font-size:18px;line-height:1.55;margin:0;color:#444;max-width:680px}
.hr-adv-btn{white-space:nowrap;flex:0 0 auto;width:auto!important;padding:16px 30px!important}
@media(max-width:768px){.hr-adv-card{flex-direction:column;align-items:flex-start;padding:30px 24px}.hr-adv{padding:16px 0 56px}.hr-adv-btn{width:100%!important;justify-content:center}}
</style>
<section class="hr-adv">
<div class="container">
<div class="hr-adv-card">
<div>
<h3>&iquest;No encontraste la propiedad que busc&aacute;s?</h3>
<p>Si lo que busc&aacute;s no aparece en nuestra cartera, igual pod&eacute;s escribirnos. Contanos qu&eacute; propiedad quer&eacute;s y ponemos a un asesor comercial a trabajar exclusivamente en encontr&aacute;rtela.</p>
</div>
<a class="button_dark button_dark_fit_content hr-adv-btn" href="{{ $hrWa }}" target="_blank" rel="noopener">Contanos qu&eacute; busc&aacute;s</a>
</div>
</div>
</section>
'''
out = "@if (request('preview') === 'ms-preview-2026')\n" + NEW + "@else\n" + old + "\n@endif\n"
open(P, 'w', encoding='utf-8').write(out)
print('OK componente', len(out))
