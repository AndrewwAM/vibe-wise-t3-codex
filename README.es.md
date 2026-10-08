# VibeWise para T3 Code y Codex

[English](README.md)

Adaptación independiente de [VibeWise](https://github.com/nykooi1/vibe-wise), de
**Noah Kim (@nykooi1)**. Aprendes a diseñar software mientras Codex implementa
el alcance que acuerdas.

**Alfa experimental — `0.1.0-alpha.1`.** Los helpers y el descubrimiento nativo
de skills/hooks están probados. Quedan pendientes las conversaciones completas
en T3, la calidad educativa y la restauración tras una reanudación o compactación
real. Pruébalo primero en un proyecto desechable.

## Requisitos

- Python **3.8+** como `python3`, sin dependencias adicionales para los helpers.
- Codex con skills/hooks nativos; descubrimiento verificado con **0.159.3** y **0.162.0**.
- T3 opcional: integración inspeccionada en **v0.0.44**; debe usar el mismo perfil de Codex.
- Entorno de shell Linux/macOS. Linux probado; macOS, Windows y WSL sin verificar.

Son versiones verificadas, no una afirmación sobre las versiones mínimas históricas.
Consulta [compatibilidad y limitaciones](docs/compatibility.md).

## Instalación

Revisa el código antes de ejecutar el instalador:

```sh
git clone https://github.com/AndrewwAM/vibe-wise-t3-codex.git
cd vibe-wise-t3-codex
git checkout v0.1.0-alpha.1
python3 -B scripts/install.py
python3 -B scripts/install.py --apply
```

La primera ejecución sólo muestra los cambios. `--apply` instala ambas skills
en `~/.codex/skills`, o en el `CODEX_HOME` existente, y agrega el hook a `hooks.json`.
Conserva los hooks anteriores y respalda la configuración antes de modificarla.
Si una skill instalada difiere, se detiene. Repetir la instalación no duplica hooks.
Puedes elegir otro perfil con `--codex-dir /ruta/absoluta/al/perfil`.

Abre `codex`, ejecuta `/hooks` y revisa “Restoring VibeWise learning context”.
Debes confiar en el hook para que se ejecute. Un hook habilitado pero sin confianza
se omite. El instalador no elude esa revisión ni cambia autenticación o sandbox.
Si el selector de T3 está desactualizado, abre una conversación nueva o actualiza
el proveedor y comprueba que utiliza el mismo perfil.

## Uso

Dentro de un proyecto:

```text
$vibe-wise-learn Quiero construir una herramienta para organizar mis notas.
```

Codex pregunta por tu enfoque, explica lo necesario y espera la decisión correspondiente
antes de implementar. Puedes pedir pistas, saltar una decisión o autorizar una
implementación directa sin confirmaciones redundantes. Para pausar, di
«pausa el modo de aprendizaje». Invocar Learn otra vez retoma las notas existentes.

Las notas son `.vibe-wise/profile.md`, `progress.md` y `project-map.md`. También
se reconoce `.sensible-vibes/`. El hook es de sólo lectura, no activa proyectos
nuevos y respeta límites de repositorio/worktree y rutas enlazadas.

`$vibe-wise-reset` muestra el destino y los archivos. Tras confirmar esa vista
previa, respalda las notas y reinicia el onboarding. Conserva el código y Git;
los respaldos permanecen en el directorio de notas.

En T3 **Plan** se conversa e inspecciona sin escribir código ni notas. Cambia a
**Default** para guardar el estado e implementar el paso acordado. La skill no
cambia el modo de T3. Los checkpoints son instrucciones al modelo, no una barrera
técnica ni una garantía de cumplimiento.

## Privacidad

Los helpers no hacen solicitudes de red ni recogen telemetría. Codex puede enviar
las notas que lee y sus rutas al proveedor de modelos como contexto. Mantén
credenciales, datos de clientes, URLs privadas y transcripciones fuera de ellas.

Agrega `.vibe-wise/` y `.sensible-vibes/` al `.gitignore` de **cada proyecto** antes
de publicarlo. El instalador no modifica los archivos de otros proyectos.
Consulta [SECURITY.md](SECURITY.md) antes de compartir diagnósticos.

## Validación y mantenimiento

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_release.py
python3 -B scripts/smoke_app_server.py
```

El control de publicación revisa los archivos registrados por Git. El smoke test
utiliza Codex real y un proyecto temporal, sin inferencia ni cambios de confianza.
Los tests ejecutan el hook directamente con eventos sintéticos. CI ejecuta tests,
controles de privacidad, Gitleaks y descubrimiento nativo. El
[registro de pruebas](docs/testing.md) distingue lo verificado de lo pendiente.

No hay actualización/desinstalación automática. Para actualizar, compara y
respalda las skills instaladas antes de reemplazarlas. Para desinstalar, quita
sólo el registro SessionStart de VibeWise y sus dos carpetas de skills, preservando
hooks ajenos, configuración y notas. Puedes deshabilitar el hook desde `/hooks`.

El manifiesto portable está incluido, pero la instalación por marketplace no está
validada. El instalador independiente es el método probado. Usa un solo método
para evitar hooks duplicados. La publicación es en GitHub.

## Créditos y licencia

El flujo educativo, los checkpoints y las notas Markdown son de **VibeWise, de Noah Kim**.
Base: **0.1.43**, commit
[`c5fc8d813ce6789ebaf631ff4dd2a69658da3f31`](https://github.com/nykooi1/vibe-wise/tree/c5fc8d813ce6789ebaf631ff4dd2a69658da3f31).
Se conserva la **licencia MIT completa y el copyright original** en raíz y skills.
[ATTRIBUTION.md](ATTRIBUTION.md) detalla la procedencia y los cambios.

Otros ports: [djolex999/vibe-wise-codex](https://github.com/djolex999/vibe-wise-codex)
y [yava-code/vibe-wise-mcp](https://github.com/yava-code/vibe-wise-mcp). Este proyecto
parte del original y no afirma ser el primero ni tener respaldo oficial.
