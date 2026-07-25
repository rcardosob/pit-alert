# PIT ALERT — Storyboard Definitivo & Arquitectura de Línea Continua

## 1. La Idea Rectoral: La Línea Continua (The Thread Line)

Toda la landing page no se compone de 7 secciones aisladas, sino de **una única trayectoria vectorial SVG persistente** (`The Thread Line`) que recorre vertical/diagonalmente la pantalla durante los 7 momentos.

Esta línea cambia de estado, geometría, densidad y color según la tensión narrativa, guiando el ojo del visitante en un movimiento ininterrumpido.

---

## 2. Definiciones de Marca & Restricciones Tácticas

* **Color de Alerta Único:** `#FFB800` (Pit Lane Amber).
* **Base Neutra:** Carbon Black (`#09090B`), Asphalt Charcoal (`#121316`), Zinc Metal (`#27272A`), Off-White (`#F4F4F5`).
* **Sistema Tipográfico Exclusivo:**
  * **Space Grotesk:** Headlines, títulos, body text e interfaz UI.
  * **JetBrains Mono:** Countdown, marcas de tiempo, datos de telemetría y coordenadas.
* **Stack Técnico Confirmado:**
  * **DOM / SVG / GSAP + ScrollTrigger:** Renderizado 100% vectorial para máxima nitidez en retina y cero lag.
  * **Scroll Nativo:** Prioritario. (Lenis descartado por ahora).
  * **Canvas 2D / Three.js:** Descartados para el MVP (únicamente SVG optimizado).
  * **Audio:** Eliminado (experiencia 100% visual y silenciosa).

---

## 3. Storyboard Escena por Escena

```
+-------------------------------------------------------------------------+
| SCENE 01: THE TRACK                                                     |
| [Marca sobre asfalto / Calma monumental]                                 |
+-------------------------------------------------------------------------+
                                    │
                                    │ (The Thread Line se acelera)
                                    ▼
+-------------------------------------------------------------------------+
| SCENE 02: THE DRIVER                                                    |
| [La línea genera coordenadas, cuadrícula y telemetría abstracta]        |
+-------------------------------------------------------------------------+
                                    │
                                    │ (La línea se aplana y desacelera)
                                    ▼
+-------------------------------------------------------------------------+
| SCENE 03: SOMETHING IS COMING                                           |
| [El flujo se detiene / Countdown monumental / Tensión Ámbar]            |
+-------------------------------------------------------------------------+
                                    │
                                    │ (La línea se bifurca en dos)
                                    ▼
+-------------------------------------------------------------------------+
| SCENE 04: LEAVE THE TRACK                                               |
| [Bifurcación a PIT LANE / Revelación de la pista / PIT.]               |
+-------------------------------------------------------------------------+
                                    │
                                    │ (La línea de Pit Lane rodea la app)
                                    ▼
+-------------------------------------------------------------------------+
| SCENE 05: THE PRODUCT                                                   |
| [App PIT ALERT protagonista con anotaciones mínimas]                     |
+-------------------------------------------------------------------------+
                                    │
                                    │ (La línea se simplifica horizontalmente)
                                    ▼
+-------------------------------------------------------------------------+
| SCENE 06: THE FUTURE                                                    |
| [Today, scheduled events. Next, the unexpected.]                        |
+-------------------------------------------------------------------------+
                                    │
                                    │ (La línea regresa al centro)
                                    ▼
+-------------------------------------------------------------------------+
| SCENE 07: BACK TO RACING                                                |
| [Reincorporación a la pista principal / CTA Download Windows]           |
+-------------------------------------------------------------------------+
```

---

### SCENE 01 — THE TRACK

#### A. Composición Visual
Minimalista, cinematográfica, espacial. Fondo `#09090B` con un patrón SVG casi imperceptible de grano de asfalto y marcas de trazado. En el centro visual, una sola línea vertical gruesa en Off-White que representa la línea ideal de carrera.

#### B. Transformación de la Línea Conductora (`The Thread Line`)
Nace en la parte superior como una **marca blanca sólida sobre asfalto** (carril central), perfectamente recta e inmóvil en reposo.

#### C. Copy Visible
* Headline (Space Grotesk, Monumental):
  > Sometimes the best trade  
  > is leaving the track.
* Brand Identity (Esquina superior izquierda): `PIT ALERT`
* Header secundario derecho (Space Grotesk / JetBrains Mono): `PIT WALL / ACTIVE`

#### D. Comportamiento Durante Scroll
Al hacer scroll, el titular se desplaza suavemente hacia arriba con fading de opacidad, mientras `The Thread Line` comienza a extenderse verticalmente y a estrecharse, adquiriendo velocidad visual.

#### E. Transición a Scene 02
La línea blanca recta comienza a pulsar sutilmente y a emitir pequeñas ramificaciones laterales en forma de guías numéricas/coordenadas.

---

### SCENE 02 — THE DRIVER

#### A. Composición Visual
Atmosférica y técnica. Sin gráficos de velas (candlesticks) tradicionales. Se sustituye por un plano cartesiano abstracto de telemetría de alta velocidad: coordenadas flotantes, marcas de tick y datos en movimiento constante.

#### B. Transformación de la Línea Conductora
La línea deja de ser un trazo sólido de pista y **se transforma en un vector de trayectoria/datos**. Comienza a oscilar suavemente en ondas geométricas precisas (estilo señal de osciloscopio o telemetría de carrera).

#### C. Copy Visible
* Headline (Space Grotesk):
  > Your eyes belong on the market.
* Subtitle (Space Grotesk, Muted):
  > Not on the economic calendar.

#### D. Comportamiento Durante Scroll
El scroll controla el ritmo de oscilación de la línea. A mayor scroll, la telemetría adyacente (JetBrains Mono) parpadea y corre verticalmente con mayor velocidad.

#### E. Transición a Scene 03
La oscilación de la línea se vuelve rígida, horizontaliza su curso y su color pasa gradualmente de Off-White a un todo zinc opaco, presagiando que algo interrumpe el flujo.

---

### SCENE 03 — SOMETHING IS COMING

#### A. Composición Visual
Tensión máxima. El layout visual **se congela**. Las coordenadas de la Scene 02 se desvanecen por completo, dejando la pantalla limpia pero cargada de tensión.

#### B. Transformación de la Línea Conductora
La línea llega al centro de la pantalla y **su movimiento rectilíneo se frena a cero**. Justo en el punto de detención, la línea se torna **`#FFB800` (Pit Lane Amber)** y se expande concéntricamente en un anillo o punto de datos fijo.

#### C. Copy Visible
* Badge de Impacto (JetBrains Mono):
  > `[ HIGH IMPACT EVENT ]`
* Evento (Space Grotesk):
  > US CPI
* Countdown Monumental (JetBrains Mono, ultra-grande):
  > 03:00
* Micro-copy (Space Grotesk):
  > PIT ALERT is watching.

#### D. Comportamiento Durante Scroll
Al hacer scroll, el tiempo en pantalla "se detiene": el contador desciende rápidamente (`03:00 → 02:30 → 01:00 → 00:05`) sincronizado milimétricamente con la posición del scroll del usuario. El halo `#FFB800` proyecta una luz sutil sobre el fondo.

#### E. Transición a Scene 04
Cuando el contador llega cerca de cero, `The Thread Line` (ahora de color `#FFB800`) se divide bruscamente en **dos caminos vectoriales**: la vía principal y una salida de emergencia.

---

### SCENE 04 — LEAVE THE TRACK (Visual Climax)

#### A. Composición Visual
El clímax de la experiencia. La perspectiva del SVG se inclina ligeramente (vía cámara virtual/viewBox transformation) para revelar que la línea que veníamos siguiendo **siempre fue una pista de carreras vista desde arriba**.

#### B. Transformación de la Línea Conductora
Ocurre la **bifurcación explícita (Pit Lane Exit)**:
* La línea de la pista principal (Racing Line) continúa hacia el abismo (oscuridad/gris).
* La **`Thread Line` encendida en `#FFB800` toma la curva de salida hacia el Pit Lane**.

#### C. Copy Visible
* Headline Gigante (Space Grotesk, Ultra-Bold, Centrado):
  > **PIT.**
* Manifest Copy (Space Grotesk):
  > No predictions.  
  > No signals.  
  > No trading advice.  
  > *Just a warning before the moment arrives.*

#### D. Comportamiento Durante Scroll
El scroll hace volar la cámara siguiendo la maniobra de entrada a boxes (la línea `#FFB800`). La palabra **`PIT.`** se escala de forma monumental ocupando el 70% del ancho de pantalla antes de dar paso a la calma.

#### E. Transición a Scene 05
La línea de Pit Lane `#FFB800` se desacelera, vuelve a tornarse en un tono Off-White ultra limpio y enmarca el contorno de una estructura: la aplicación PIT ALERT.

---

### SCENE 05 — THE PRODUCT

#### A. Composición Visual
Protagonismo absoluto de la aplicación REAL de PIT ALERT. **Cero cards SaaS decorativas o grids convencionales**. La app se muestra en su UI real, suspendida sobre un fondo carbon black con anotaciones mínimas a su alrededor.

#### B. Transformación de la Línea Conductora
`The Thread Line` **se convierte en el marco estructural exterior del mockup de la app**, rodeándola como un chasis de protección y conectando directamente con tres puntos de anotación.

#### C. Copy Visible / Anotaciones (Space Grotesk + JetBrains Mono)
* Anotación 1 (Top): `01 / ECONOMIC CALENDAR FILTER`
* Anotación 2 (Middle): `02 / CUSTOM ALERT ANTICIPATION`
* Anotación 3 (Bottom): `03 / AUDIBLE & VISUAL WARNING`

#### D. Comportamiento Durante Scroll
La ventana de la aplicación permanece fija en pantalla (pinned por GSAP) durante un tramo de scroll mientras las tres anotaciones aparecen secuencialmente a medida que `The Thread Line` dibuja los conectores hacia los hotspots del software.

#### E. Transición a Scene 06
La línea abandona el marco de la aplicación por su borde inferior y continúa descendiendo en una trayectoria simple y fluida.

---

### SCENE 06 — THE FUTURE

#### A. Composición Visual
Limpia, sobria, enfocada en la visión del producto. Generosa en espacio negativo.

#### B. Transformación de la Línea Conductora
La línea adopta una forma rectilínea limpia que divide horizontalmente los dos estados del producto (El Presente y El Futuro).

#### C. Copy Visible
* Estado Actual (Space Grotesk):
  > Today, scheduled events.
* Visión Futura (Space Grotesk, Accentuation):
  > Next, the unexpected.
* Etiquetas secundarias discretas (JetBrains Mono):
  > `[ BREAKING NEWS ]`  `[ PUBLICATIONS ]`  `[ MARKET EVENTS ]`

#### D. Comportamiento Durante Scroll
Al hacer scroll, la frase "Today, scheduled events" baja su opacidad para dar el foco a "Next, the unexpected", mientras las tres etiquetas secundarias parpadean sutilmente en baja opacidad.

#### E. Transición a Scene 07
La línea retoma la aceleración vertical, alineándose nuevamente al centro del viewport para la reincorporación final.

---

### SCENE 07 — BACK TO RACING

#### A. Composición Visual
Sensación de control recuperado, calma y llamado a la acción. Reincorporación de la salida de boxes a la pista principal.

#### B. Transformación de la Línea Conductora
`The Thread Line` sale del Pit Lane y **se reincorpora fluidamente a la línea central de la pista (Racing Line)**, cerrando el ciclo visual que comenzó en la Scene 01.

#### C. Copy Visible
* Closing Claim (Space Grotesk):
  > Stay focused on the race.  
  > We'll watch the track.
* CTA Button (Space Grotesk + JetBrains Mono):
  > **DOWNLOAD PIT ALERT**  
  > `FOR WINDOWS — v1.0`
* Brand Lockup (Footer): `PIT ALERT — Situational Awareness for Traders`

#### D. Comportamiento Durante Scroll
La línea se asienta en el fondo. El botón de descarga emerge centrado en la pantalla con un pulso de borde sutil en `#FFB800` en estado hover/active.

---

## 4. Elementos Persistentes en Todo el Journey

1. **Header de Marca Minimalista (Fixed Top):** `PIT ALERT` a la izquierda, estado `PIT WALL / ACTIVE` a la derecha (ocultable en responsive si congestiona).
2. **`The Thread Line` (SVG Principal):** Un único objeto `<svg>` posicionado con `position: fixed` o `sticky` que actualiza su atributo `d=""` (path data) y color mediante GSAP a lo largo de todo el scroll.
3. **Indicador de Coordenadas de Scroll (Fixed Bottom Right):** Marcador numérico discreto en JetBrains Mono que muestra la escena actual (`SCENE 01/07`, `SCENE 02/07`, etc.).

---

## 5. Inventario de Assets Requeridos

1. **Pattern de Asfalto (SVG / WebP):** 1x textura Seamless ultra-ligera de ruido/grano de asfalto en baja opacidad (5%).
2. **Interface Graphic de PIT ALERT (SVG / WebP / HTML Real UI):** Fiel representación de la interfaz real de la aplicación desktop.
3. **Tipografías (Google Fonts):**
   * *Space Grotesk* (Weights: 400, 500, 700).
   * *JetBrains Mono* (Weights: 400, 600).
4. **Icono de Sistema Operativo:** SVG vectorial de Windows.

---

## 6. Documentación Guardada
Este storyboard definitivo ha sido escrito en el archivo local de tu proyecto:
📄 **[PIT_ALERT_STORYBOARD.md](file:///C:/Users/rcard/Documents/pit-alert/PIT_ALERT_STORYBOARD.md)**
