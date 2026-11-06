# Recorrido 3D desde el plano: 7 prompts

Método tomado del post de @joacoquiroogaa (Instagram), "Copiá estos 7 prompts y vendele a una inmobiliaria recorridos 3D desde el plano".

- Los prompts **01 a 04** son los que se leen en las imágenes del post. El 04 está cortado al final en la captura, así que su cierre es una reconstrucción.
- Los prompts **05 a 07** el autor los da por privado. Los de abajo **no son los originales**: los escribí yo siguiendo la misma lógica, para usarlos en Claude Code.

Orden de armado: plano.json → recorrido.html → muebles → materiales y luz → caminar → ficha → publicar.

---

## 01 · Leer el plano
Primero las medidas. Nada de 3D.

> Te paso el plano de [PROPIEDAD] (foto o PDF). Antes de construir nada, leelo y devolveme: los ambientes con ancho y largo en metros, los muros con su espesor, y cada puerta y ventana con su muro, su ancho y hacia dónde abre. Sacá la escala de la cota más larga que se lea y controlala con otra: si difieren más de [3] %, avisame. Lo que no se lea, no lo inventes: listalo como pregunta. Guardá todo en plano.json, en metros, con el origen en una esquina, y esperá mi OK antes de seguir.

## 02 · Levantar el recorrido
Los muros, a su altura real.

> Con plano.json, armá recorrido.html: un solo archivo, three.js por import map desde jsDelivr con la versión fija. 1 unidad = 1 metro. Muros extruidos a [2,60] m con su espesor real, los vanos de puertas y ventanas recortados (no pintados encima), piso por ambiente y techo. La cámara arranca en la puerta de entrada, a 1,60 m de altura. Sumá un botón «Planta» que muestre todo desde arriba con el nombre de cada ambiente. Que ande fluido en un celular de gama media: geometría simple y una sola luz con sombra. Para probarlo: python3 -m http.server.

## 03 · Amoblar con las fotos
A medida real, sin bajar modelos.

> Te paso las fotos de la propiedad con el ambiente en el nombre (living-1.jpg, dormitorio-1.jpg…). De cada una, decime qué muebles se ven, dónde están, su color y su material. Armalos con primitivas de three.js (BoxGeometry, CylinderGeometry, RoundedBoxGeometry) a medida real: sillón de 3 cuerpos 2,10 × 0,90 m, cama doble 1,40 × 1,90, mesa, placares, mesada. Nada de modelos bajados de internet. Que no tapen puertas ni ventanas y dejen 0,80 m de paso. Si una foto no es clara, dejalo afuera y anotalo en pendientes.md. Si se vende vacía, sumá un botón «Amoblado / Vacío».

## 04 · Materiales y luz
Que se parezca a la propiedad.

> Ahora que se parezca a la propiedad. Sacá de las fotos el piso de cada ambiente (madera, porcelanato, cerámico) y el color de las paredes, y armá los materiales con MeshStandardMaterial: texturas generadas en código o color plano con su rugosidad, sin bajar imágenes con derechos. Luz de día que entre por las ventanas según la orientación [NORTE / SUR / ESTE / OESTE] del plano, un RoomEnvironment para los reflejos suaves y tone mapping ACES Filmic. *(cierre cortado en la captura)*

---

## 05 · Caminarlo (versión propia, no es la original)

> Sobre recorrido.html, hacé que se pueda caminar en primera persona. En celular: joystick táctil abajo a la izquierda para moverse y arrastrar con un dedo para mirar. En computadora: WASD o flechas y arrastrar con el mouse. Velocidad de paso de 1,4 m/s. Colisión con muros y muebles con un radio de cuerpo de 0,25 m, que deslice a lo largo de la pared en vez de frenar en seco, y que pase por las puertas (ancho mínimo 0,70 m). Altura de ojos fija en 1,60 m. Un botón «Volver a la entrada». Que no se pueda salir del departamento. Probalo atravesando cada puerta y cada pasillo del plano.json y avisame si algún paso queda bloqueado por un mueble.

## 06 · La ficha adentro (versión propia, no es la original)

> Sumá a recorrido.html una ficha de la propiedad que se abra desde un botón «Ficha»: dirección, m² cubiertos, ambientes, orientación, expensas y precio (leelos de ficha.json, no los inventes: si falta un dato, dejalo vacío). Además, un cartel flotante con el nombre de cada ambiente que aparezca cuando estoy dentro de ese ambiente, y un botón «Contactar» con el WhatsApp de la inmobiliaria [NÚMERO] y un mensaje ya escrito que nombre la propiedad. Todo en el mismo HTML, sin librerías nuevas, y legible en celular.

## 07 · Publicarlo (versión propia, no es la original)

> Dejá recorrido.html listo para publicar: un solo archivo, con los datos de plano.json y de la ficha embebidos adentro, sin pedir nada que no esté en el archivo salvo three.js desde jsDelivr con versión fija. Agregá un título y una vista previa para compartir por WhatsApp (etiquetas og:title y og:image), y un favicon en data URI. Probalo abriéndolo desde un servidor local y desde un celular de gama media. Después decime los pasos para subirlo a un hosting estático (GitHub Pages o Netlify) y cómo queda el link por propiedad.
