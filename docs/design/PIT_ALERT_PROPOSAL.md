# PIT ALERT — Propuesta de Dirección Creativa & Arquitectura Visual

## 1. Manifiesto y Dirección Creativa
La landing page de **PIT ALERT** no debe parecer una página SaaS convencional. La dirección de arte fusiona la **alta precisión del motorsport (editorial de carreras de resistencia / pit wall)** con la **tecnología financiera de baja latencia**.

El usuario experimentará una tensión narrativa progresiva:
`CALMA → FOCO → ADVERTENCIA → TENSIÓN → PIT (CLÍMAX) → DECISIÓN → CALMA → DESCARGA`.

---

## 2. Sistema de Diseño & Dirección de Arte

### A. Paleta Cromática (High-Contrast Stealth + Alert Signal)
* **Fondo Principal:** `#09090B` (Carbon Black)
* **Superficies / Paneles:** `#121316` (Asphalt Charcoal)
* **Bordes & Estructura:** `#27272A` (Zinc Dark Metal)
* **Texto Primario:** `#F4F4F5` (Off-White Pure)
* **Texto Secundario:** `#A1A1AA` (Muted Metallic)
* **Color de Alerta Único:** `#FFB800` (Pit Lane Amber / Safety Yellow) o `#FF3B30` (Telemetry Red).
  * *Regla:* Reservado exclusivamente para la activación de la escena del evento y la orden de `PIT`. Nunca usado como mero adorno.

### B. Tipografía
* **Headlines / Títulos Prominentes:** *Syne* o *Space Grotesk* (Geometría refinada, ancha, con carácter industrial y futurista).
* **Números / Telemetría / Contadores:** *JetBrains Mono* o *Space Mono* (Sensación de reloj de boxes / terminal de datos).
* **Copy de Acompañamiento:** *Inter* (Legibilidad máxima en pantallas de alta densidad).

### C. Motion & Atmosphere
* Estética de velocidad y precisión.
* Uso de líneas paralelas de pista, grano sutil de asfalto y desenfoque direccional (motion blur) en elementos de alta velocidad.

---

## 3. Arquitectura Visual de las 7 Escenas y Scroll Mechanics

### SCENE 01 — THE TRACK
* **Sensación:** Calma, velocidad contenida, enfoque.
* **Composición:** Pantalla predominantemente oscura. Grano sutil de asfalto. Líneas abstractas de pista en perspectiva 3D (CSS/Canvas).
* **Copy:** 
  > Sometimes the best trade  
  > is leaving the track.
* **Scroll Mechanics:** El scroll hace avanzar la cámara a lo largo de las líneas de asfalto mientras el texto permanece fijo y luego se disuelve en profundidad.

### SCENE 02 — THE DRIVER
* **Sensación:** Enfoque total, ritmo acelerado.
* **Composición:** Las líneas abstractas de la pista se convierten fluidamente en ejes de un gráfico financiero de alta velocidad. Flujo continuo de números de telemetría y velas monocromáticas.
* **Copy:** 
  > Your eyes belong on the market.  
  > *Not on the economic calendar.*
* **Scroll Mechanics:** A medida que se navega hacia abajo, el gráfico aumenta de velocidad simulando la carga cognitiva del trader.

### SCENE 03 — SOMETHING IS COMING
* **Sensación:** Tensión ascendente, advertencia.
* **Composición:** El ritmo visual se frena abruptamente. El fondo adquiere un tono más profundo y un temporizador toma el centro de la pantalla.
* **Elementos:** `HIGH IMPACT — US CPI`, Contador regresivo prominente `03:00 → 02:59 → 02:58` con estética de semáforo de pit lane.
* **Copy:** 
  > PIT ALERT is watching.
* **Scroll Mechanics:** El número del temporizador se reduce con el movimiento del scroll, mientras un destello de luz ámbar pulsa suavemente en el horizonte.

### SCENE 04 — LEAVE THE TRACK (Visual Climax)
* **Sensación:** Decisión táctica, impacto visual máximo.
* **Composición:** La línea principal del gráfico se desvía bruscamente fuera del canal central dirigiéndose hacia la línea de boxes (*Pit Lane*).
* **Copy:** 
  > **PIT.**  
  > No predictions. No signals. No trading advice.  
  > *Just a warning when the track is about to change.*
* **Scroll Mechanics:** La palabra **PIT** aparece a una escala gigantesca. El color de alerta cubre los bordes del viewport.

### SCENE 05 — THE PRODUCT
* **Sensación:** Claridad tecnológica, herramienta de precisión.
* **Composición:** Revelado del software PIT ALERT. Interfaz flotante minimalista sobre fondo oscuro neutro con detalles de telemetría.
* **Highlights Clave:**
  1. Calendario económico filtrado.
  2. Ajuste de anticipación de alerta.
  3. Notificación auditiva y visual.
* **Scroll Mechanics:** Pin horizontal o rotación 3D leve del panel del producto al hacer scroll.

### SCENE 06 — THE FUTURE
* **Sensación:** Visión a largo plazo, contención.
* **Composición:** Bloques limpios de datos en baja opacidad.
* **Copy:** 
  > Today, scheduled events.  
  > Tomorrow, anything that can move the market.
* **Scroll Mechanics:** Desplazamiento progresivo de cards sutiles.

### SCENE 07 — BACK TO RACING
* **Sensación:** Retorno a la calma, control total.
* **Composición:** Retorno a las líneas neutras de la pista. El entorno se vuelve silencioso y ordenado.
* **Copy:** 
  > Stay focused on the race. We'll watch the track.
* **CTA Primario:** `DOWNLOAD PIT ALERT` (Badge: Windows | Versión actual).
* **Scroll Mechanics:** El botón permanece centrado con un brillo sutil en estado de reposo.

---

## 4. Desglose Técnico de Componentes

| Escena | Elementos HTML / CSS | Animaciones (Canvas / SVG / Motion) | Assets Visuales Requeridos |
| :--- | :--- | :--- | :--- |
| **Scene 01** | Typography, Brand Header | Perspective 3D lines, scroll parallax | Pattern de textura de asfalto (SVG noise / WebP) |
| **Scene 02** | Headlines, Stat counters | Canvas 2D / SVG Financial chart motion | Stream de datos numéricos |
| **Scene 03** | Timer layout, Event Badge | Countdown ticker animation, Amber pulse glow | Iconografía de impacto (High Impact Badge) |
| **Scene 04** | Giant Copy ("PIT"), Body text | Trajectory detour to Pit Lane (Canvas path animation) | Ninguno (100% vectorial/Canvas) |
| **Scene 05** | Feature list, Callout badges | Product UI interactive micro-animations | Mockup/Render vectorial de alta fidelidad de PIT ALERT |
| **Scene 06** | Text & Specs cards | Smooth fade-ins | Vector graphic indicators |
| **Scene 07** | CTA Button, Footer, OS badges | Subtle glow loop on CTA | Logo PIT ALERT / Windows Icon |

---

## 7. MVP Visual vs. Efectos Complejos Opcionales

### MVP Visual (Prioridad Alta - Ejecución limpia & fluida)
* Transiciones de escenas basadas en scroll mediante GSAP ScrollTrigger / CSS Scroll-Driven.
* Pista y gráfico financiero dibujados dinámicamente en Canvas 2D o SVG optimizado.
* Sistema tipográfico estricto con Google Fonts (*Syne* + *JetBrains Mono* + *Inter*).
* Representación limpia y pulida de la app PIT ALERT.

### Efectos Complejos (Fase 2 / Polish)
* Shaders 3D en WebGL (Three.js) para simulación realista de asfalto y luces.
* Efectos de audio táctico al hacer scroll o interactuar con el pit wall.

---

## 8. Decisiones Técnicas & Limitaciones Identificadas
1. **Performance de Scroll:** Se implementará la librería **Lenis Scroll** para garantizar que las animaciones de scroll sean suaves en todas las plataformas sin alterar el scroll nativo.
2. **Compatibilidad Móvil:** En dispositivos móviles, la pista 3D se adaptará a un flujo vertical vectorial más simplificado para evitar consumo excesivo de batería/GPU.
