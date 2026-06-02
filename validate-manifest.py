#!/usr/bin/env python3
import json
import os
import sys

def main():
    manifest_path = "MANIFEST.json"
    
    # 1. Check if manifest exists
    if not os.path.exists(manifest_path):
        print(f"Error: {manifest_path} no existe.", file=sys.stderr)
        sys.exit(1)
        
    # 2. Try parsing manifest
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: {manifest_path} no es un JSON válido: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer {manifest_path}: {e}", file=sys.stderr)
        sys.exit(1)
        
    skills = manifest.get("skills", [])
    if not skills:
        print("Advertencia: No se encontraron skills en el manifiesto.", file=sys.stderr)
        
    errors = 0
    
    # 3. Validate each skill
    for index, skill in enumerate(skills):
        skill_name = skill.get("name", f"Skill #{index}")
        skill_id = skill.get("id", f"skill_{index}")
        
        # Validate path
        skill_path = skill.get("path")
        if not skill_path:
            print(f"[-] Skill '{skill_id}' no tiene el campo 'path' definido.", file=sys.stderr)
            errors += 1
        elif not os.path.exists(skill_path):
            print(f"[-] Archivo de skill no encontrado para '{skill_id}': {skill_path}", file=sys.stderr)
            errors += 1
        else:
            print(f"[+] Skill '{skill_id}' path verificado: {skill_path}")
            
        # Validate references
        references = skill.get("references", [])
        for ref_path in references:
            if not os.path.exists(ref_path):
                print(f"[-] Referencia no encontrada en skill '{skill_id}': {ref_path}", file=sys.stderr)
                errors += 1
            else:
                print(f"[+] Referencia verificada para '{skill_id}': {ref_path}")
                
    if errors > 0:
        print(f"\n[Fallo] Se encontraron {errors} error(es) en MANIFEST.json.", file=sys.stderr)
        sys.exit(1)
        
    print("\n[Éxito] ¡MANIFEST.json es válido y todos los archivos referenciados existen!")
    sys.exit(0)

if __name__ == "__main__":
    main()
