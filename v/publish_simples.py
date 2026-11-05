import os, shutil
ROOT='/home/matiassosacom/public_html'; V=ROOT+'/resources/views'
G="request('preview') === 'ms-preview-2026'"
log=[]
def rep(path, pairs):
    p=V+'/'+path
    s=open(p,encoding='utf-8').read()
    b=p+'.antes-publicar-simples'
    if not os.path.exists(b): shutil.copy(p,b)
    for old,new in pairs:
        n=s.count(old)
        if n==0: log.append('FALLO/YA   %s :: %s'%(path,old[:40])); continue
        s=s.replace(old,new); log.append('OK x%d     %s'%(n,path))
    open(p,'w',encoding='utf-8').write(s)
    os.system('chown matiassosacom:matiassosacom '+p)
rep('front/components/footer.blade.php',[("("+G+") ? 'Pol&iacute;tica'","(true) ? 'Pol&iacute;tica'")])
for pg in ('landing','busqueda-nuevo','busqueda'):
    pairs=[("if (!("+G+")) { echo 'console.log","if (!(true)) { echo 'console.log")]
    if pg=='landing':
        pairs.append(("{{ "+G+" ? 'true' : 'false' }}","true"))
    rep('front/pages/%s.blade.php'%pg,pairs)
rep('front/components/propertyCard.blade.php',[("("+G+") ? html_entity_decode(html_entity_decode(","(true) ? html_entity_decode(html_entity_decode(")])
rep('front/pages/blog-post.blade.php',[("@if ("+G+")\n<style>.blog-body table","@if (true)\n<style>.blog-body table")])
rep('front/layouts/master.blade.php',[("@if ("+G+")\n@php $__og","@if (true)\n@php $__og"),("{{ ("+G+") ? 'IE=edge'","{{ (true) ? 'IE=edge'")])
rep('errors/404.blade.php',[("@if ("+G+")\n@include","@if (true)\n@include")])
print('\n'.join(log))
