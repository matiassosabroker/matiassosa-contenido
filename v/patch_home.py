#!/usr/bin/env python3
# Parche del home (landing) - SOLO PREVIEW (?preview=ms-preview-2026)
import re, shutil, sys

P = 'resources/views/front/pages/landing.blade.php'
s = open(P, encoding='utf-8').read()
shutil.copy(P, P + '.antes-home2')
PV = "request('preview') === 'ms-preview-2026'"

# 1) Sacar el boton "Te asesoramos en tu busqueda" (solo preview)
old = 'buttonText="Te asesoramos en tu búsqueda"'
assert s.count(old) == 1, 'hero button'
s = s.replace(old, ':buttonText="' + PV + " ? '' : 'Te asesoramos en tu búsqueda'\"")

# 2) Destacadas: el slider viejo queda solo para la web publica
pat = re.compile(r"@if \(true\)(\s*<style>\s*\.ms-slider\{)")
assert len(pat.findall(s)) == 1, 'slider block'
s = pat.sub(lambda m: "@if (request('preview') !== 'ms-preview-2026')" + m.group(1), s)

NEW_FEAT = r'''
@if (request('preview') === 'ms-preview-2026')
<style>
.hf-wrap{position:relative;margin-top:8px}
.hf-page{display:none;gap:20px}
.hf-page.on{display:grid;animation:hfIn .35s ease}
.hf-p12{grid-template-columns:repeat(4,minmax(0,1fr))}
.hf-p6{grid-template-columns:repeat(2,minmax(0,1fr))}
@keyframes hfIn{from{opacity:0;transform:translateX(16px)}to{opacity:1;transform:none}}
.hf-cell{min-width:0}
.hf-cell>*{width:100%!important;max-width:100%!important}
.hf-arrow{position:absolute;top:50%;margin-top:-24px;width:48px;height:48px;border-radius:50%;border:1px solid #d8d8d4;background:#fff;box-shadow:0 4px 14px rgba(0,0,0,.18);cursor:pointer;font-size:26px;line-height:1;z-index:5;display:flex;align-items:center;justify-content:center;transition:background .2s,color .2s,border-color .2s}
.hf-arrow:hover{background:#141414;color:#C9A66B;border-color:#141414}
.hf-prev{left:-22px}.hf-next{right:-22px}
.hf-dots{display:flex;justify-content:center;align-items:center;gap:8px;margin-top:22px}
.hf-dots i{width:9px;height:9px;border-radius:50%;background:#cfcfca;display:block;cursor:pointer;transition:background .2s,transform .2s}
.hf-dots i.on{background:#141414;transform:scale(1.25)}
.hf-track{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding:4px 2px 12px}
.hf-track::-webkit-scrollbar{display:none}
.hf-slide{flex:0 0 86%;scroll-snap-align:start}
@media (max-width:1250px){.hf-prev{left:-8px}.hf-next{right:-8px}}
</style>
<script>
document.addEventListener('DOMContentLoaded',function(){
var sec=document.querySelector('.featured_section');if(!sec)return;
var first=sec.querySelector('.property_card_container');if(!first)return;
var grid=first.parentElement;
var protos=[].slice.call(grid.children).map(function(c){return c.cloneNode(true);});
if(protos.length<2)return;
var wrap=document.createElement('div');wrap.className='hf-wrap';
grid.parentNode.insertBefore(wrap,grid);
grid.style.display='none';
var mob=document.getElementById('featureCardsCarousel');if(mob){mob.style.display='none';}
var mode='',cur=0,pages=[],dots=null;
function perPage(){var w=window.innerWidth;return w>=1100?12:(w>700?6:0);}
function go(i){
  if(!pages.length)return;
  cur=(i+pages.length)%pages.length;
  pages.forEach(function(p,k){p.classList.toggle('on',k===cur);});
  if(dots){[].forEach.call(dots.children,function(d,k){d.className=(k===cur)?'on':'';});}
}
function build(){
  var pp=perPage(),m=pp?('p'+pp):'m';
  if(m===mode)return;
  mode=m;wrap.innerHTML='';pages=[];dots=null;cur=0;
  if(!pp){
    var tr=document.createElement('div');tr.className='hf-track';
    protos.forEach(function(c){var d=document.createElement('div');d.className='hf-cell hf-slide';d.appendChild(c.cloneNode(true));tr.appendChild(d);});
    wrap.appendChild(tr);return;
  }
  var n=Math.ceil(protos.length/pp);
  for(var i=0;i<n;i++){
    var pg=document.createElement('div');pg.className='hf-page hf-p'+pp+(i===0?' on':'');
    protos.slice(i*pp,(i+1)*pp).forEach(function(c){var d=document.createElement('div');d.className='hf-cell';d.appendChild(c.cloneNode(true));pg.appendChild(d);});
    wrap.appendChild(pg);pages.push(pg);
  }
  if(n>1){
    var pr=document.createElement('button');pr.type='button';pr.className='hf-arrow hf-prev';pr.setAttribute('aria-label','Anteriores');pr.innerHTML='&#8249;';
    var nx=document.createElement('button');nx.type='button';nx.className='hf-arrow hf-next';nx.setAttribute('aria-label','Siguientes');nx.innerHTML='&#8250;';
    pr.onclick=function(){go(cur-1);};nx.onclick=function(){go(cur+1);};
    wrap.appendChild(pr);wrap.appendChild(nx);
    dots=document.createElement('div');dots.className='hf-dots';
    for(var k=0;k<n;k++){(function(k){var d=document.createElement('i');d.onclick=function(){go(k);};dots.appendChild(d);})(k);}
    wrap.appendChild(dots);go(0);
  }
}
window.addEventListener('resize',build);
build();
});
</script>
@endif
'''

anchor = '<div class="our_ventures_section">'
assert s.count(anchor) == 1, 'ventures anchor'
s = s.replace(anchor, NEW_FEAT + anchor)

# 3) Resenas de compradores + 4) Asesoramiento
reviews = [
 ('Sandra S.', 'Compré un departamento con su intermediación. Desde la primer comunicación me contactaron y derivaron con una agente, Camila. Disposición total, respuestas inmediatas. Felicito el trato y consideración de mis diferentes inquietudes!'),
 ('Laura S.', 'Excelente experiencia con la inmobiliaria Matías Sosa. Desde el primer momento me brindaron un asesoramiento integral y transparente para la compra de mi departamento en Mar del Plata. Quiero destacar especialmente la atención personalizada de Camila, quien demostró un profesionalismo impecable, paciencia y una calidez humana que facilitó todo el proceso. Me sentí acompañada en cada etapa. Totalmente recomendables! Muchas gracias!'),
 ('Justo José R.', 'La experiencia con la inmobiliaria Matias Sosa Broker fue realmente muy buena. Desde el primer contacto nos atendieron muy bien y respondieron todas nuestras consultas. Hicimos la compra de la propiedad con crédito hipotecario, en ese sentido fueron muy eficientes en conseguir toda la documentación necesaria para presentar en el Banco. Muchas gracias!!!'),
 ('Nicolás M.', 'Experiencia increíble. Estuvimos con mi novia mas de 3 meses buscando una casa para comprar y además de no encontrar nada, ninguna inmobiliaria nos atendía bien, llegamos a Matias por medio de un amigo en común y la verdad que desde el momento uno se ocupo de nuestra búsqueda, nos derivo con uno de sus colaboradores para que se dedique exclusivamente a nuestro pedido y en 2 semanas reservamos lo que hoy es nuestra nueva casa, mas que satisfechos con todo el proceso.'),
 ('Paola M.', 'Excelente elección desde el primer momento. La mejor experiencia!!! La predisposición, la atención, la amabilidad y el carisma de Florencia, lo hizo muy llevadero y tranquilo a todo lo que para nosotros fue nuevo. Felices con la compra que pudimos concretar. Recomendable cien por ciento. Muchas gracias.'),
 ('Orlando C.', 'Muy profesional el trabajo de Flor, nos acompaño en todo el proceso de compra, y nos ayudó a solucionar muchísimas cosas. MEJOR? imposible.. muchas gracias por todo Flor.'),
 ('Estefanía M.', 'Mi experiencia fue excelente! Flor me ayudó en la búsqueda de mi departamento y además de que logramos cerrar la operación, esta compra fue para mi una experiencia inolvidable en la cual me sentí acompañada con su calidez y muy bien asesorada desde el primer momento. Muchas gracias a todo el equipo! Los súper recomiendo.'),
 ('Lucía M.', 'La experiencia de la compra de nuestra primer propiedad fue excelente, fuimos acompañados por Celeste quien nos asesoró de la mejor forma hasta el último momento. Estamos súper felices!'),
 ('Jorge W.', 'Todo el proceso de compra de nuestro departamento fue coordinado por Florencia, con un compromiso, una buena onda, muy dificil de encontrar, y que nos sorprendió desde el primer día... Sin ella no hubiésemos logrado nuestro sueño... Un trabajo IMPECABLE!!! Agradecidos para siempre.'),
 ('Carlos M.', 'Nuestra experiencia con Matias Sosa Broker ha sido muy positiva. Agradecemos especialmente la excelente atención de Lucas, como asesor inmobiliario, permitiéndonos tomar una rápida decisión de compra de un inmueble para nuestra hija. Esto gracias a la confianza que trasmite como persona, su seriedad profesional y su calidez, cualidades que uno desearía encontrar siempre en este tipo de operaciones y también en otros órdenes de la vida. Muchas gracias Lucas!'),
 ('Florencia', 'Genios! Súper recomendado, hicimos una venta y una compra con ellos y fue todo excelente (tiempos, predisposición, organización). Volvería a contratarlos. Excelente atención de Matías y Flor!'),
]
def q(x):
    return "'" + x.replace('\\', '\\\\').replace("'", "\\'") + "'"
php_rev = ",\n".join("['n'=>%s,'t'=>%s]" % (q(n), q(t)) for n, t in reviews)

NEW_BLOCK = r'''
@if (request('preview') === 'ms-preview-2026')
@php
$hrReviews = [
__REVIEWS__
];
$hrWa = 'https://wa.me/5492233447092?text=Hola%21%20No%20encontr%C3%A9%20la%20propiedad%20que%20busco%20en%20la%20web%20y%20quiero%20que%20me%20ayuden%20a%20encontrarla.';
$hrMaps = 'https://www.google.com/maps/place/Mat%C3%ADas+Sosa+Broker+Inmobiliario/@-38.0214871,-57.5340494,17z';
@endphp
<style>
.hr-rev{background:#EEEEED;color:#1B1B1B;padding:84px 0 56px}
.hr-rev h2{font-size:clamp(28px,3.8vw,48px);font-weight:800;letter-spacing:-.025em;text-align:center;line-height:1.08;margin:0}
.hr-rev h2 span{color:#b08d4f}
.hr-score{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:12px 16px;margin:18px 0 40px;font-weight:700;font-size:18px}
.hr-stars{color:#C9A66B;letter-spacing:3px;font-size:24px}
.hr-score a{color:#1B1B1B;text-decoration:underline;text-underline-offset:4px;font-weight:600}
.hr-track{display:flex;gap:22px;overflow-x:auto;scroll-snap-type:x mandatory;padding:10px 4px 34px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.hr-track::-webkit-scrollbar{display:none}
.hr-card{flex:0 0 min(430px,86vw);scroll-snap-align:start;background:#fff;border-radius:20px;padding:30px 28px 26px;box-shadow:0 10px 30px rgba(0,0,0,.07);display:flex;flex-direction:column;justify-content:space-between;border-top:4px solid #C9A66B}
.hr-card .hr-stars{font-size:20px}
.hr-card p{font-size:17px;line-height:1.55;margin:14px 0 24px;color:#2a2a2a}
.hr-who{display:flex;align-items:center;gap:12px}
.hr-av{width:46px;height:46px;border-radius:50%;background:#1B1B1B;color:#C9A66B;font-weight:800;display:flex;align-items:center;justify-content:center;flex:0 0 46px}
.hr-who b{display:block;line-height:1.2}
.hr-who small{color:#777;font-size:13px}
.hr-arrows{display:flex;justify-content:center;gap:12px;margin-top:6px}
.hr-arrows button{width:52px;height:52px;border-radius:50%;border:2px solid #1B1B1B;background:transparent;color:#1B1B1B;font-size:22px;cursor:pointer;transition:all .2s}
.hr-arrows button:hover{background:#1B1B1B;color:#C9A66B}
.hr-adv{background:#EEEEED;padding:24px 0 80px}
.hr-adv-card{background:#fff;border-radius:20px;padding:44px 48px;display:flex;gap:32px;align-items:center;justify-content:space-between;border-left:6px solid #C9A66B;box-shadow:0 10px 30px rgba(0,0,0,.06)}
.hr-adv-card h3{font-size:clamp(24px,2.6vw,34px);font-weight:800;letter-spacing:-.02em;line-height:1.12;margin:0 0 12px;color:#1B1B1B}
.hr-adv-card p{font-size:18px;line-height:1.55;margin:0;color:#444;max-width:680px}
.hr-adv-btn{white-space:nowrap;flex:0 0 auto;width:auto!important;padding:16px 30px!important}
@media(max-width:768px){.hr-rev{padding:56px 0 40px}.hr-adv-card{flex-direction:column;align-items:flex-start;padding:30px 24px}.hr-adv{padding:16px 0 56px}.hr-adv-btn{width:100%!important;justify-content:center}}
</style>
<section class="hr-rev">
<div class="container">
<h2>Compraron con nosotros <span>y nos recomiendan</span></h2>
<div class="hr-score">
<span class="hr-stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
<span>4,9 de 5 &middot; m&aacute;s de 250 rese&ntilde;as en Google</span>
<a href="{{ $hrMaps }}" target="_blank" rel="noopener">Ver todas las rese&ntilde;as</a>
</div>
<div class="hr-wrap">
<div class="hr-track" id="hrTrack" tabindex="0" aria-label="Rese&ntilde;as de clientes que compraron">
@foreach ($hrReviews as $r)
<article class="hr-card">
<div>
<div class="hr-stars" aria-label="5 estrellas">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
<p>&ldquo;{{ $r['t'] }}&rdquo;</p>
</div>
<div class="hr-who">
<div class="hr-av">{{ mb_substr($r['n'], 0, 1) }}</div>
<div><b>{{ $r['n'] }}</b><small>Rese&ntilde;a en Google</small></div>
</div>
</article>
@endforeach
</div>
<div class="hr-arrows">
<button type="button" id="hrPrev" aria-label="Rese&ntilde;a anterior">&larr;</button>
<button type="button" id="hrNext" aria-label="Rese&ntilde;a siguiente">&rarr;</button>
</div>
</div>
</div>
</section>
<script>
(function(){
var tr=document.getElementById('hrTrack');if(!tr)return;
function step(){var c=tr.querySelector('.hr-card');return c?c.offsetWidth+22:400;}
function next(){if(tr.scrollLeft+tr.clientWidth>=tr.scrollWidth-6){tr.scrollTo({left:0,behavior:'smooth'});}else{tr.scrollBy({left:step(),behavior:'smooth'});}}
function prev(){if(tr.scrollLeft<=4){tr.scrollTo({left:tr.scrollWidth,behavior:'smooth'});}else{tr.scrollBy({left:-step(),behavior:'smooth'});}}
var timer=null,reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function start(){if(reduce||timer)return;timer=setInterval(next,4500);}
function stop(){clearInterval(timer);timer=null;}
function restart(){stop();start();}
document.getElementById('hrNext').addEventListener('click',function(){next();restart();});
document.getElementById('hrPrev').addEventListener('click',function(){prev();restart();});
['mouseenter','focusin','touchstart'].forEach(function(e){tr.addEventListener(e,stop,{passive:true});});
['mouseleave','focusout','touchend'].forEach(function(e){tr.addEventListener(e,start,{passive:true});});
if('IntersectionObserver' in window){new IntersectionObserver(function(es){es[0].isIntersecting?start():stop();},{threshold:0.3}).observe(tr);}else{start();}
})();
</script>
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
<div style="display:none" aria-hidden="true">
<x-commentCarousel :data="$data"></x-commentCarousel>
</div>
@else
<x-commentCarousel :data="$data"></x-commentCarousel>
<x-personalizedAdvice></x-personalizedAdvice>
@endif
'''.replace('__REVIEWS__', php_rev)

oldblk = '<x-commentCarousel :data="$data"></x-commentCarousel>\n<x-personalizedAdvice></x-personalizedAdvice>'
if s.count(oldblk) != 1:
    # tolerante a saltos de linea CRLF
    oldblk = re.search(r'<x-commentCarousel :data="\$data"></x-commentCarousel>\s*<x-personalizedAdvice></x-personalizedAdvice>', s).group(0)
s = s.replace(oldblk, NEW_BLOCK.strip('\n'))

open(P, 'w', encoding='utf-8').write(s)
print('OK landing parcheado', len(s))
