# PIT ALERT v0.2 — Roadmap de Instalador Mínimo Profesional

## Objetivo

Convertir el MVP actual de PIT ALERT en una aplicación instalable en Windows, sin cambiar su lógica principal.

El objetivo práctico es que el usuario ya no tenga que entrar manualmente a la carpeta del build:

```text
dist\PIT_ALERT\PIT_ALERT.exe
```

En su lugar, PIT ALERT deberá poder abrirse desde:

```text
Menú Inicio de Windows → PIT ALERT
```

El usuario también podrá anclarlo manualmente a:

```text
Barra de tareas
Menú Inicio
Escritorio
```

---

## Alcance de la versión 0.2

### Incluido

```text
1. Crear instalador con Inno Setup
2. Instalar PIT ALERT en Program Files
3. Crear acceso directo en Menú Inicio
4. Crear acceso directo opcional en Escritorio
5. Incluir ícono oficial de PIT ALERT
6. Crear uninstaller
7. Mantener el comportamiento actual de la app
8. Preparar archivo instalador para GitHub Releases
```

### No incluido

```text
1. System tray
2. Auto-start con Windows
3. Cerrar a bandeja
4. Alertas ON por default al iniciar Windows
5. Single instance
6. Logs avanzados
8. Firma digital
9. Auto-update
```

La versión 0.2 debe ser una mejora de distribución, con una migración acotada de configuración y caché a `LocalAppData` para permitir uso profesional por cuenta de Windows.

La distribución pública usará la `PIT ALERT Community License 1.0`: permite uso, mejoras y distribución gratuita con atribución, pero prohíbe reventa, sublicencia comercial y servicios de pago basados sustancialmente en la app.

---

## Resultado esperado

Al finalizar esta versión, deberá existir un instalador:

```text
PIT_ALERT_Setup_0.2.0.exe
```

El usuario ejecuta el instalador y PIT ALERT queda instalado en:

```text
C:\Program Files\PIT ALERT\
```

Los datos personales de cada usuario se guardarán en:

```text
%LOCALAPPDATA%\PIT ALERT\
```

Después podrá abrirlo desde:

```text
Menú Inicio → PIT ALERT
```

También podrá desinstalarlo desde:

```text
Configuración de Windows → Aplicaciones instaladas
```

o desde el uninstaller creado por Inno Setup.

---

# Fase 1 — Verificación del build actual

## Objetivo

Confirmar que el `.exe` actual sigue funcionando correctamente antes de crear el instalador.

## Tareas

```text
1. Confirmar que python app.py funciona.
2. Confirmar que el build de PyInstaller funciona.
3. Confirmar que el ícono oficial aparece correctamente.
4. Confirmar que la carpeta dist\PIT_ALERT contiene todo lo necesario.
5. Confirmar que PIT_ALERT.exe abre correctamente desde dist.
```

## Criterio de aceptación

El siguiente comando debe abrir la app correctamente:

```powershell
.\dist\PIT_ALERT\PIT_ALERT.exe
```

La aplicación debe conservar el comportamiento aprobado del MVP.

---

# Fase 2 — Limpieza de archivos para distribución

## Objetivo

Asegurar que el instalador solo empaquete lo necesario.

## Carpeta a incluir

```text
dist\PIT_ALERT\
```

Esta carpeta debe contener el ejecutable y los archivos generados por PyInstaller, por ejemplo:

```text
PIT_ALERT.exe
_internal/
assets/
config/
data/
```

La estructura exacta puede variar dependiendo de cómo PyInstaller genere el build.

## Archivos a excluir

```text
.venv/
build/
*.spec
__pycache__/
.git/
archivos temporales
archivos de desarrollo que no sean necesarios para el usuario final
```

## Criterio de aceptación

La carpeta `dist\PIT_ALERT` debe poder ejecutarse por sí sola antes de pasar a Inno Setup.

---

# Fase 3 — Crear script de Inno Setup

## Objetivo

Crear el archivo de configuración del instalador.

Archivo sugerido:

```text
installer/PIT_ALERT.iss
```

## El script deberá definir

```text
1. Nombre de la app: PIT ALERT
2. Versión: 0.2.0
3. Publisher: Mithril Mountain o el nombre que se decida usar
4. Carpeta destino: C:\Program Files\PIT ALERT\
5. Ejecutable principal: PIT_ALERT.exe
6. Ícono oficial: pit_alert.ico
7. Acceso directo en Menú Inicio
8. Acceso directo opcional en Escritorio
9. Uninstaller
10. Nombre del instalador de salida
```

## Criterio de aceptación

Inno Setup debe compilar sin errores y generar:

```text
PIT_ALERT_Setup_0.2.0.exe
```

---

# Fase 4 — Instalación local de prueba

## Objetivo

Probar el instalador como lo haría un usuario real.

## Tareas

```text
1. Ejecutar PIT_ALERT_Setup_0.2.0.exe.
2. Instalar en Program Files.
3. Abrir PIT ALERT desde Menú Inicio.
4. Confirmar que la app carga calendario.
5. Confirmar que las alertas siguen funcionando.
6. Confirmar que el ícono aparece correctamente.
7. Confirmar que se puede cerrar normalmente.
```

## Criterio de aceptación

PIT ALERT debe funcionar igual que el MVP actual, pero ya instalado en Windows.

---

# Fase 5 — Validar desinstalación

## Objetivo

Confirmar que el usuario puede quitar PIT ALERT correctamente.

## Tareas

```text
1. Ir a Aplicaciones instaladas en Windows.
2. Desinstalar PIT ALERT.
3. Confirmar que se elimina la carpeta de Program Files.
4. Confirmar que se elimina el acceso directo del Menú Inicio.
5. Confirmar que no quedan accesos directos rotos.
```

## Criterio de aceptación

El programa debe desinstalarse limpiamente.

---

# Fase 6 — Ajuste de documentación

## Objetivo

Actualizar documentación para usuario final.

## Archivos sugeridos

```text
README.md
CHANGELOG.md
```

## Contenido mínimo del README

```text
1. Qué es PIT ALERT
2. Cómo instalar
3. Cómo abrir desde Menú Inicio
4. Cómo desinstalar
5. Limitaciones actuales
6. Disclaimer de trading
7. Versión actual: 0.2.0
```

## Criterio de aceptación

Un usuario debe poder instalar y usar PIT ALERT sin instrucciones manuales sobre dónde encontrar el `.exe`.

---

# Fase 7 — Preparar release

## Objetivo

Dejar listo el instalador para distribución.

## Artifact final

```text
PIT_ALERT_Setup_0.2.0.exe
```

## Release notes sugeridas

```text
PIT ALERT v0.2.0

Changes:
- Added Windows installer using Inno Setup.
- Added installation to Program Files.
- Added Start Menu shortcut.
- Added optional Desktop shortcut.
- Added official PIT ALERT icon.
- Added uninstaller.
- Preserved current MVP behavior.
```

## Criterio de aceptación

El archivo está listo para subirse a GitHub Releases o compartirse directamente.

---

# Definition of Done

La versión 0.2 estará terminada cuando:

```text
1. Existe PIT_ALERT_Setup_0.2.0.exe.
2. El instalador corre correctamente.
3. PIT ALERT queda instalado en Program Files.
4. PIT ALERT aparece en Menú Inicio.
5. PIT ALERT abre correctamente desde Menú Inicio.
6. El ícono oficial aparece correctamente.
7. La app mantiene el comportamiento actual.
8. El uninstaller funciona.
9. La documentación básica está actualizada.
```

---

# Orden recomendado de ejecución

```text
1. Rebuild limpio con PyInstaller.
2. Probar dist\PIT_ALERT\PIT_ALERT.exe.
3. Crear carpeta installer/.
4. Crear PIT_ALERT.iss.
5. Compilar instalador en Inno Setup.
6. Instalar localmente.
7. Probar app instalada.
8. Probar desinstalación.
9. Ajustar README / CHANGELOG.
10. Guardar versión en Git.
```

---

# Estrategia aprobada

La versión 0.2 será un instalador mínimo profesional.

No se tocará la lógica funcional del MVP.

El objetivo principal es mejorar la instalación, el acceso desde Windows y la experiencia básica de distribución.
