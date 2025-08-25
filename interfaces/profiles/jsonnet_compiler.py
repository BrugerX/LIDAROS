import _jsonnet, sys, pathlib

infile = sys.argv[1] if len(sys.argv) > 1 else "testdevice_persona.jsonnet"
out = _jsonnet.evaluate_file(infile)
path = pathlib.Path(infile).with_suffix(".json")
path.write_text(out)
print(f"Wrote {path}")
