#!/usr/bin/env python3
import sys
import os
import json
import subprocess

def load_manifest():
    manifest_path = "MANIFEST.json"
    if not os.path.exists(manifest_path):
        print(f"Error: {manifest_path} not found in current directory.", file=sys.stderr)
        sys.exit(1)
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_skill_prompt(skill):
    prompt_parts = []
    
    # 1. Main skill file
    skill_path = skill.get("path")
    if skill_path and os.path.exists(skill_path):
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
            prompt_parts.append(f"# SKILL: {skill['name']}\n\n{content}")
    else:
        print(f"Warning: Skill file {skill_path} not found.", file=sys.stderr)

    # 2. Reference files
    references = skill.get("references", [])
    if references:
        prompt_parts.append("\n## REFERENCE DOCUMENTATION\n")
        for ref_path in references:
            if os.path.exists(ref_path):
                with open(ref_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    ref_name = os.path.basename(ref_path)
                    prompt_parts.append(f"### Reference: {ref_name}\n\n{content}\n")
            else:
                print(f"Warning: Reference file {ref_path} not found.", file=sys.stderr)
                
    return "\n---\n".join(prompt_parts)

def copy_to_clipboard(text):
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
        return True
    except Exception:
        return False

def main():
    manifest = load_manifest()
    skills = manifest.get("skills", [])
    skill_ids = [s["id"] for s in skills]

    if len(sys.argv) < 2:
        print("Usage: python3 build-prompt.py <skill-id>", file=sys.stderr)
        print("\nAvailable Skill IDs:", file=sys.stderr)
        for sid in skill_ids:
            print(f"  - {sid}", file=sys.stderr)
        sys.exit(1)

    target_id = sys.argv[1]
    matching_skill = next((s for s in skills if s["id"] == target_id), None)

    if not matching_skill:
        print(f"Error: Skill '{target_id}' not found.", file=sys.stderr)
        print(f"Available Skill IDs: {', '.join(skill_ids)}", file=sys.stderr)
        sys.exit(1)

    print(f"Building prompt for skill: {matching_skill['name']}...", file=sys.stderr)
    prompt = get_skill_prompt(matching_skill)
    
    # Try to copy to clipboard
    copied = copy_to_clipboard(prompt)
    
    # Print the prompt to stdout so it can be redirected
    print(prompt)
    
    if copied:
        print(f"\n[Success] Prompt for '{target_id}' copied to your clipboard (macOS pbcopy)!", file=sys.stderr)
    else:
        print(f"\n[Notice] Prompt built successfully. Clipboard not supported or pbcopy failed.", file=sys.stderr)

if __name__ == "__main__":
    main()
