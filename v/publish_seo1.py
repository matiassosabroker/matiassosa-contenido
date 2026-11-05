import os, shutil
V='/home/matiassosacom/public_html/resources/views'
G="request('preview') === 'ms-preview-2026'"
log=[]
def rep(path,pairs):
    p=V+'/'+path; s=open(p,encoding='utf-8').read()
    b=p+'.antes-publicar-seo1'
    if not os.path.exists(b): shutil.copy(p,b)
    for o,n in pairs:
        c=s.count(o)
        if c==0: log.append('FALLO/YA %s :: %s'%(path,o[:35])); continue
        s=s.replace(o,n); log.append('OK x%d %s'%(c,path))
    open(p,'w',encoding='utf-8').write(s); os.system('chown matiassosacom:matiassosacom '+p)
rep('front/pages/index.blade.php',[(":type=\"("+G+") ? 'h2' : 'h1'\"",":type=\"(true) ? 'h2' : 'h1'\"")])
rep('front/pages/tasacion.blade.php',[(":type=\"("+G+") ? 'h2' : 'h1'\"",":type=\"(true) ? 'h2' : 'h1'\"")])
rep('front/pages/contacto.blade.php',[("@if ("+G+")\n<h1 style=\"position:absolute","@if (true)\n<h1 style=\"position:absolute")])
rep('front/layouts/master.blade.php',[("{{ ("+G+") ? '' : 'user-scalable=no, ' }}","{{ (true) ? '' : 'user-scalable=no, ' }}")])
rep('front/components/footer.blade.php',[("{!! ("+G+") ? 'aria-label=","{!! (true) ? 'aria-label=")])
print('\n'.join(log))
