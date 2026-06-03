# Historial de Cambios (Changelog)

Todos los cambios notables en el repositorio LiveSkills están documentados en este archivo.

El formato sigue las pautas de [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).  
El versionado sigue el [SemVer (Versionado Semántico)](https://semver.org/spec/v2.0.0.html).

---

## [1.3.1] — 2026-06-02

### Modificaciones
- **Clarificación de la Audiencia de Agentes**: Se amplió el README principal para documentar explícitamente la compatibilidad con agentes como Gemini, Antigravity-ide, Codex, Opencode y otros modelos Frontier.

---

## [1.3.0] — 2026-06-02

### Seguridad y Estandarización de Stack
- **Gestor de Paquetes (`pnpm`)**: Se reemplazó el uso de `npm` por `pnpm` en todas las referencias, guías y configuraciones (Docker, workflows de CI/CD, comandos de prueba) por motivos de seguridad y rendimiento.
- **Normalización del Stack UI**: Se eliminó la referencia a `Next.js` en los skills, dejando el estándar web de componentes y vistas basado exclusivamente en `React + Vite + TailwindCSS`.
- **Limpieza de Referencias de Clientes**: Se removieron todas las referencias y menciones específicas en todos los archivos de skills y referencias, sustituyéndolas por nombres o descripciones genéricas de clientes B2B.

---

## [1.2.0] — 2026-06-02

### Agregado
- **Script Wrapper para CLI (`run-skill.sh`)**: Ejecuta de manera local un skill enviándolo directamente como contexto del sistema a Claude CLI.
- **Generador Dinámico de Prompts (`build-prompt.py`)**: Script en Python para combinar dinámicamente cualquier skill con todas sus referencias markdown y copiar el prompt resultante al portapapeles de macOS (`pbcopy`) automáticamente.
- **Validador de Manifiesto (`validate-manifest.py`)**: Script para comprobar la integridad de `MANIFEST.json` contra el esquema local y verificar que no existan referencias rotas en el repositorio.
- **Esquema JSON Local (`manifest.schema.json`)**: Definición del esquema estructural para autocompletado y validación de tipos en tiempo real.
- **CI con GitHub Actions**: Workflow automatizado para correr el script validador en cada commit o Pull Request.

---

## [1.1.0] — 2026-06-02

### Modificaciones
- **Traducción de Documentación**: Se tradujo la documentación principal del repositorio (`README.md`, `_template/README.md` y `CHANGELOG.md`) al español, manteniendo los skills y sus referencias en inglés.
- **Prompts Operativos**: Se crearon e integraron 8 prompts operativos autotenidos (en inglés) en la sección `## Prompts Operativos (Copy-Paste para CLI)` del `README.md` principal, permitiendo copiar y pegar el skill de manera directa en el CLI sin clonar el repositorio.

---

## [1.0.0] — 2026-06-02

### Auditoría Completa y Expansión del Directorio de Skills de Agentes

### Agregado

**Fase 1 — Higiene del Repositorio**
- `.gitignore` — Archivos de macOS, env, dependencias, compilados, archivos de IDE.
- `LICENSE.md` — Licencia propietaria (uso interno únicamente).
- Corrección del nombre del repositorio en el README de `live-developer-skills/` a `LiveSkills/`.
- Normalización de los tokens de diseño CSS en `landing-pages.md` y `dashboards.md` para coincidir con la nomenclatura canónica de `design-system.md` (`--color-*` → `--bg-*`, `--text-*`, `--border-*`, `--accent`).
- Eliminación de archivos `.DS_Store` del repositorio.

**Fase 2 — Referencias Faltantes para Skills Existentes**
- `dev-code-agent/references/bash-shell.md` — Cabeceras estrictas, registro de logs, scripts de despliegue, análisis de argumentos, seguridad.
- `dev-code-agent/references/sql-postgresql.md` — Convenciones de esquemas, patrones de consultas, migraciones, indexación, rendimiento.
- `frontend-ui-agent/references/react-components.md` — React Query, React Hook Form + Zod, Zustand, enrutamiento, cliente de API.

**Fase 3 — Nuevos Skills Críticos**
- `devops-infra-agent/` — Servidores, máquinas virtuales, CI/CD, Docker, Nginx, monitoreo.
  - `references/proxmox-vms.md` — Creación de VMs, plantillas, endurecimiento, redes, respaldos.
  - `references/ci-cd.md` — GitHub Actions, despliegue con Docker, Nginx, SSL, DNS, retrocesos.
  - `references/monitoring.md` — Endpoints de salud, Uptime Kuma, gestión de logs, respuesta a incidentes.
- `content-copywriting-agent/` — SEO, redacción, campañas de correo electrónico.
  - `references/seo.md` — Investigación de palabras clave, SEO en página, plantillas de contenido, SEO técnico, marcado de esquemas.
  - `references/copywriting.md` — Fórmulas de titulares, marcos de persuasión (PAS/AIDA/BAB), redacción de CTA, microcopy.
  - `references/email-campaigns.md` — Secuencias, líneas de asunto, segmentación, entregabilidad (SPF/DKIM/DMARC).
- `qa-testing-agent/` — Pruebas, revisión de código, auditorías de seguridad.
  - `references/testing-strategies.md` — Patrones por lenguaje (pytest, Vitest, Pest), simulación (mocking), estrategia de cobertura.
  - `references/code-review.md` — Lista de verificación de revisión, formato de comentarios, sistema de severidad, pautas de tamaño de PR.

**Fase 4 — Infraestructura de Descubrimiento**
- `MANIFEST.json` — Registro de skills legible por máquina con disparadores, esquemas de E/S y lógica de enrutamiento.
- `_template/` — Plantilla para crear nuevos skills (SKILL.md + plantillas de referencia).
- Actualización de `dev-code-agent/SKILL.md` — se agregaron bash-shell.md y sql-postgresql.md a la sección de referencias.
- Actualización de `frontend-ui-agent/SKILL.md` — se agregó react-components.md a la sección de referencias.
- Rediseño completo de `README.md` con árbol expandido, índice de skills, mapa de dominios y documentación de descubrimiento.

**Fase 5 — Skills Secundarios**
- `audiovisual-agent/` — Flujo de producción de video (DOM-AV).
  - `references/pre-production.md` — Análisis de briefs, redacción de guiones (formato de dos columnas), guiones gráficos, listas de tomas, dirección creativa.
  - `references/post-production.md` — Flujo de trabajo de edición, gradación de color, mezcla de audio (LUFS), gráficos en movimiento, especificaciones de exportación por plataforma.
- `data-analysis-agent/` — Análisis de datos y generación de reportes (DOM-DEV).
  - `references/analysis-patterns.md` — Flujo de trabajo de EDA, series de tiempo, análisis de cohortes, embudos, RFM, pruebas A/B, ETL.
  - `references/reporting.md` — Plantillas de reportes, código Chart.js/matplotlib, diseño de tableros, salida Excel.
- `project-management-agent/` — Planificación y coordinación (DOM-OPS).
  - `references/planning.md` — Briefs de proyectos, planificación de sprints, hojas de ruta, gestión de riesgos, estimación.
  - `references/coordination.md` — Reportes de estado, comunicaciones con clientes, orquestación de agentes, matriz RACI.
- `CHANGELOG.md` — Este archivo.

### Estadísticas del Repositorio (v1.0.0)

| Métrica | Valor |
|---|---|
| Total de skills | 8 |
| Total de archivos de referencia | 24 |
| Total de archivos (md + json) | 38 |
| Dominios cubiertos | 5 (DOM-DEV, DOM-HST, DOM-MKT, DOM-AV, DOM-OPS) |
| Plantilla incluida | Sí |
| Manifiesto para máquina | Sí |

---

## [0.0.0] — 2025-06

### Agregado
- Creación inicial por Daniel Calisaya / Live Developer.
- `dev-code-agent/` con 4 referencias (python, php-laravel, typescript-node, agent-process-patterns).
- `frontend-ui-agent/` con 3 referencias (landing-pages, dashboards, design-system).
- `README.md` con estructura básica e índice de skills.
