#!/usr/bin/env python3
"""Export embedded PNG images from a Jupyter notebook without running it."""
import argparse
import base64
import json
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--notebook", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, default=Path("figures/extracted"))
    args=p.parse_args()
    notebook=json.loads(args.notebook.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    count=0
    for i,cell in enumerate(notebook.get("cells",[])):
        for j,output in enumerate(cell.get("outputs",[])):
            raw=output.get("data",{}).get("image/png")
            if raw:
                data="".join(raw) if isinstance(raw,list) else raw
                target=args.output_dir / f"{args.notebook.stem}_cell_{i:02d}_image_{j:02d}.png"
                target.write_bytes(base64.b64decode(data))
                print(target)
                count+=1
    print(f"Extracted {count} PNG images")

if __name__=="__main__":
    main()
