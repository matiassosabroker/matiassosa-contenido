import os, shutil
p='/home/matiassosacom/public_html/resources/views/front/layouts/master.blade.php'
G="request('preview') === 'ms-preview-2026'"
s=open(p,encoding='utf-8').read()
if 'ms-css1' in s:
    print('YA APLICADO'); raise SystemExit
b=p+'.antes-css1'
if not os.path.exists(b): shutil.copy(p,b)
def wrap(s,line,cond):
    if line not in s: print('FALLO',line[:60]); return s
    return s.replace(line,"{{-- ms-css1 --}}\n@if ("+cond+")\n"+line+"\n@endif",1)
fan="request()->is('propiedad/*')"
s=wrap(s,'<link href="{{ asset(\'front/vendors/css/aos.min.css\') }}" rel="stylesheet">',"!("+G+")")
s=wrap(s,'<link href="{{ asset(\'front/vendors/css/animate.min.css\') }}" rel="stylesheet">',"!("+G+")")
s=wrap(s,'<link href="{{ asset(\'front/vendors/css/fancybox.min.css\') }}" rel="stylesheet">',"!("+G+") || "+fan)
s=wrap(s,'<script src="{{ asset(\'front/vendors/js/fancybox.min.js\') }}" defer></script>',"!("+G+") || "+fan)
open(p,'w',encoding='utf-8').write(s)
os.system('chown matiassosacom:matiassosacom '+p)
print('OK')
