#!/usr/bin/env bash

set -euo pipefail

# Print usage instructions
usage() {
    echo "Uso: $0 <skill-id> <tarea>"
    echo "Ejemplo: $0 dev-code-agent \"Escribe un script en Python para parsear JSON\""
    exit 1
}

# Check arguments
if [ "$#" -lt 2 ]; then
    usage
fi

SKILL_ID="$1"
# Combine all remaining arguments as the task
shift
USER_TASK="$*"

# Check if build-prompt.py exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_PROMPT_PY="${SCRIPT_DIR}/build-prompt.py"

if [ ! -f "${BUILD_PROMPT_PY}" ]; then
    echo "Error: No se encontró build-prompt.py en ${SCRIPT_DIR}" >&2
    exit 1
fi

# Build prompt using Python script (hiding the success message from stdout)
echo "Generando contexto para el skill '${SKILL_ID}'..." >&2
if ! SYSTEM_PROMPT=$(python3 "${BUILD_PROMPT_PY}" "${SKILL_ID}" 2>/dev/null); then
    echo "Error: No se pudo generar el prompt para el skill '${SKILL_ID}'." >&2
    python3 "${BUILD_PROMPT_PY}" "${SKILL_ID}" 2>&1 >/dev/null || true
    exit 1
fi

# Prepare combined command prompt
COMBINED_PROMPT="[SYSTEM INSTRUCTION: You must act according to the following skill guidelines]

${SYSTEM_PROMPT}

[USER TASK]
${USER_TASK}"

# Check if 'claude' CLI is available
if command -v claude &> /dev/null; then
    echo "Ejecutando Claude CLI con el skill '${SKILL_ID}'..." >&2
    claude "${COMBINED_PROMPT}"
else
    echo "Nota: El comando 'claude' no está instalado en el sistema." >&2
    echo "A continuación se muestra el prompt completo compilado para que lo copies:" >&2
    echo "----------------------------------------------------------------------"
    echo "${COMBINED_PROMPT}"
    echo "----------------------------------------------------------------------"
fi
