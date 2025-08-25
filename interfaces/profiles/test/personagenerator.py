#!/usr/bin/env python3
import sys, json, os

def ensure_trailing_slash(s: str) -> str:
    return s if s.endswith("/") else s + "/"

def ensure_double_slash(s: str) -> str:
    if "//" in s:
        return s
    return s.replace("/", "//", 1) if "/" in s else s + "//"

def set_descriptor_type(obj, transform):
    """Recursively apply transform to every descriptor.type (string) in obj."""
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            if k == "descriptor" and isinstance(v, dict):
                v2 = v.copy()
                if isinstance(v2.get("type"), str):
                    v2["type"] = transform(v2["type"])
                new[k] = set_descriptor_type(v2, transform)
            else:
                new[k] = set_descriptor_type(v, transform)
        return new
    if isinstance(obj, list):
        return [set_descriptor_type(x, transform) for x in obj]
    return obj

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {os.path.basename(sys.argv[0])} <input.json>")
        sys.exit(1)

    in_path = sys.argv[1]
    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    variants = {
        "type_endslash":   lambda s: ensure_trailing_slash(s),
        "type_doubleslash":lambda s: ensure_double_slash(s),
        "type_empty":      lambda s: "",
    }

    base = os.path.splitext(os.path.basename(in_path))[0]
    outdir = os.path.dirname(os.path.abspath(in_path)) or "."

    for suffix, fn in variants.items():
        modified = set_descriptor_type(data, fn)
        out_path = os.path.join(outdir, f"{base}_{suffix}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(modified, f, ensure_ascii=False, indent=2)
        print(out_path)

if __name__ == "__main__":
    main()
