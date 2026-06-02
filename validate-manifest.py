#!/usr/bin/env python3
import json
import os
import re
import sys

def main():
    manifest_path = "MANIFEST.json"
    schema_path = "manifest.schema.json"
    
    # 1. Check if files exist
    if not os.path.exists(manifest_path):
        print(f"Error: {manifest_path} no existe.", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(schema_path):
        print(f"Error: {schema_path} no existe.", file=sys.stderr)
        sys.exit(1)
        
    # 2. Try parsing manifest
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: {manifest_path} no es un JSON válido: {e}", file=sys.stderr)
        sys.exit(1)
        
    errors = 0
    
    # Helper to print errors
    def report_error(msg):
        nonlocal errors
        print(f"[-] {msg}", file=sys.stderr)
        errors += 1

    # 3. Schema Validation (No dependencies, custom parser to match manifest.schema.json)
    root_required = ["name", "version", "description", "maintainer", "skills", "domains", "routing"]
    for req in root_required:
        if req not in manifest:
            report_error(f"Falta el campo requerido en la raíz: '{req}'")
            
    if errors > 0:
        sys.exit(1)
        
    # Validate types of root
    if not isinstance(manifest["name"], str): report_error("El campo 'name' debe ser un string.")
    if not isinstance(manifest["version"], str): report_error("El campo 'version' debe ser un string.")
    if not isinstance(manifest["description"], str): report_error("El campo 'description' debe ser un string.")
    if not isinstance(manifest["maintainer"], str): report_error("El campo 'maintainer' debe ser un string.")
    if not isinstance(manifest["skills"], list): report_error("El campo 'skills' debe ser una lista.")
    if not isinstance(manifest["domains"], dict): report_error("El campo 'domains' debe ser un objeto/dict.")
    if not isinstance(manifest["routing"], dict): report_error("El campo 'routing' debe ser un objeto/dict.")
    
    if errors > 0:
        sys.exit(1)
        
    # Validate domains map
    for k, v in manifest["domains"].items():
        if not isinstance(k, str) or not k.startswith("DOM-"):
            report_error(f"La clave de dominio '{k}' debe ser un string que comience con 'DOM-'.")
        if not isinstance(v, str):
            report_error(f"La descripción del dominio para '{k}' debe ser un string.")

    # Validate routing section
    routing = manifest["routing"]
    routing_required = ["strategy", "fallback", "instructions"]
    for r_req in routing_required:
        if r_req not in routing:
            report_error(f"Falta el campo requerido en 'routing': '{r_req}'")
        elif not isinstance(routing[r_req], str):
            report_error(f"El campo '{r_req}' en 'routing' debe ser un string.")

    # Validate each skill
    skills = manifest["skills"]
    skill_required = ["id", "name", "domain", "version", "path", "description", "triggers", "languages", "references", "input", "output"]
    
    for index, skill in enumerate(skills):
        skill_id = skill.get("id", f"skill_{index}")
        
        # Check required fields
        for s_req in skill_required:
            if s_req not in skill:
                report_error(f"Skill '{skill_id}': Falta el campo requerido '{s_req}'")
                
        if errors > 0:
            continue
            
        # Validate field types and constraints
        if not isinstance(skill["id"], str) or not re.match(r"^[a-z0-9-]+-agent$", skill["id"]):
            report_error(f"Skill '{skill_id}': 'id' debe cumplir con el patrón '^[a-z0-9-]+-agent$'.")
            
        if not isinstance(skill["name"], str):
            report_error(f"Skill '{skill_id}': 'name' debe ser un string.")
            
        if not isinstance(skill["domain"], str) or not re.match(r"^DOM-[A-Z]+$", skill["domain"]):
            report_error(f"Skill '{skill_id}': 'domain' debe cumplir con el patrón '^DOM-[A-Z]+$'.")
        elif skill["domain"] not in manifest["domains"]:
            report_error(f"Skill '{skill_id}': el dominio '{skill['domain']}' no está registrado en la sección 'domains'.")
            
        if not isinstance(skill["version"], str) or not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", skill["version"]):
            report_error(f"Skill '{skill_id}': 'version' debe ser semántica '^X.Y.Z$'.")
            
        if not isinstance(skill["path"], str) or not re.match(r"^[a-z0-9-]+-agent/SKILL\.md$", skill["path"]):
            report_error(f"Skill '{skill_id}': 'path' debe cumplir con el patrón '^[a-z0-9-]+-agent/SKILL.md$'.")
        elif not os.path.exists(skill["path"]):
            report_error(f"Skill '{skill_id}': Archivo no encontrado en '{skill['path']}'")
        else:
            print(f"[+] Skill '{skill_id}' path verificado: {skill['path']}")
            
        if not isinstance(skill["description"], str):
            report_error(f"Skill '{skill_id}': 'description' debe ser un string.")
            
        # Triggers
        if not isinstance(skill["triggers"], list):
            report_error(f"Skill '{skill_id}': 'triggers' debe ser una lista.")
        else:
            for t in skill["triggers"]:
                if not isinstance(t, str):
                    report_error(f"Skill '{skill_id}': disparador '{t}' debe ser un string.")
                    
        # Languages
        if not isinstance(skill["languages"], list):
            report_error(f"Skill '{skill_id}': 'languages' debe ser una lista.")
        else:
            for l in skill["languages"]:
                if not isinstance(l, str):
                    report_error(f"Skill '{skill_id}': lenguaje '{l}' debe ser un string.")

        # References
        if not isinstance(skill["references"], list):
            report_error(f"Skill '{skill_id}': 'references' debe ser una lista.")
        else:
            for ref_path in skill["references"]:
                if not isinstance(ref_path, str) or not re.match(r"^[a-z0-9-]+-agent/references/[a-z0-9-]+\.md$", ref_path):
                    report_error(f"Skill '{skill_id}': Referencia '{ref_path}' no cumple con el patrón.")
                elif not os.path.exists(ref_path):
                    report_error(f"Skill '{skill_id}': Archivo de referencia no encontrado: '{ref_path}'")
                else:
                    print(f"[+] Referencia verificada para '{skill_id}': {ref_path}")
                    
        # Input object
        input_data = skill["input"]
        if not isinstance(input_data, dict) or "required" not in input_data:
            report_error(f"Skill '{skill_id}': 'input' debe ser un objeto/dict con la clave 'required'.")
        else:
            if not isinstance(input_data["required"], list):
                report_error(f"Skill '{skill_id}': 'input.required' debe ser una lista.")
            if "optional" in input_data and not isinstance(input_data["optional"], list):
                report_error(f"Skill '{skill_id}': 'input.optional' debe ser una lista.")
                
        # Output object
        output_data = skill["output"]
        if not isinstance(output_data, dict) or "format" not in output_data or "artifacts" not in output_data:
            report_error(f"Skill '{skill_id}': 'output' debe ser un objeto/dict con las claves 'format' y 'artifacts'.")
        else:
            if not isinstance(output_data["format"], str):
                report_error(f"Skill '{skill_id}': 'output.format' debe ser un string.")
            if not isinstance(output_data["artifacts"], list):
                report_error(f"Skill '{skill_id}': 'output.artifacts' debe ser una lista.")

    if errors > 0:
        print(f"\n[Fallo] Se encontraron {errors} error(es) en MANIFEST.json.", file=sys.stderr)
        sys.exit(1)
        
    print("\n[Éxito] ¡MANIFEST.json cumple con el esquema manifest.schema.json y todos los archivos existen!")
    sys.exit(0)

if __name__ == "__main__":
    main()
