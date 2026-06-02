# Plantilla de Skill

Usa esta plantilla para crear un nuevo skill. Copia todo el directorio `_template/` y cámbiale el nombre.

## Inicio Rápido

```bash
# Crear un nuevo skill
cp -r _template/ mi-nuevo-agent/

# Editar el SKILL.md
# 1. Actualizar el frontmatter YAML (name, description, version)
# 2. Rellenar el Proceso de Pensamiento del Agente (Agent Thinking Process)
# 3. Definir los tipos de tareas y sus referencias
# 4. Establecer los estándares de calidad
# 5. Definir el formato de salida estructurado

# Crear archivos de referencia
# 1. Un archivo .md por cada tema principal
# 2. Incluir plantillas de código, patrones y listas de verificación
# 3. Mantener cada referencia autocontenida y cargable de forma independiente
```

## Convenciones

- Nombre del directorio de skill: `kebab-case-agent/` (ej. `data-analysis-agent/`)
- Archivo principal: `SKILL.md` (siempre este nombre exacto)
- Referencias: `references/*.md` (uno por tema)
- Frontmatter YAML requerido: `name`, `description`, `version`, `maintainer`
- Después de crear el skill, agrégalo a `MANIFEST.json` en el directorio raíz
