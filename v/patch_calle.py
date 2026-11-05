import shutil, os, re
P = '/home/matiassosacom/public_html/resources/views/front/pages/landing.blade.php'
if not os.path.exists(P + '.antes-calle'):
    shutil.copy(P, P + '.antes-calle')
s = open(P, encoding='utf-8').read()
if '_pv' in s:
    print('YA APLICADO'); raise SystemExit
old = "$('#filter-container').html(data);"
assert s.count(old) == 1, s.count(old)
new = ("var _pv = {{ request('preview') === 'ms-preview-2026' ? 'true' : 'false' }}; "
       "var $c = $('#filter-container'); "
       "var $s = _pv ? $c.children('div.container').has('input[name=calle]').detach() : $(); "
       "$c.html(data); "
       "if ($s.length) { "
       "var _id = parseInt(($c.find('.is-landing.active').attr('href') || '').split('/').pop(), 10) || 1; "
       "$s.find('form').attr('action', '/busqueda/' + _id + '/resultado'); "
       "$c.append($s); }")
s = s.replace(old, new)
# estilos del bloque de calle: que apliquen tambien a /busqueda/2/resultado
n = s.count('form[action*="busqueda/1/resultado"]')
s = s.replace('form[action*="busqueda/1/resultado"]', 'form[action*="/resultado"]')
open(P, 'w', encoding='utf-8').write(s)
os.system('chown matiassosacom:matiassosacom ' + P)
print('OK css selectors:', n)
