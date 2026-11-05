import os, shutil
p='/home/matiassosacom/public_html/resources/views/front/layouts/master.blade.php'
G="request('preview') === 'ms-preview-2026'"
s=open(p,encoding='utf-8').read()
shutil.copy(p,p+'.antes-publicar-css1') if not os.path.exists(p+'.antes-publicar-css1') else None
a=s.count("@if (!("+G+"))\n<link"); b=s.count("@if (!("+G+") || request()->is('propiedad/*'))")
s=s.replace("@if (!("+G+"))\n<link","@if (!(true))\n<link").replace("@if (!("+G+") || request()->is('propiedad/*'))","@if (!(true) || request()->is('propiedad/*'))")
open(p,'w',encoding='utf-8').write(s); os.system('chown matiassosacom:matiassosacom '+p)
print('OK css=%d fancy=%d'%(a,b))
