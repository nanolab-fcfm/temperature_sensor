#!/usr/bin/env python3
"""Recolour component meshes in a KiCad-exported GLB.

`kicad-cli pcb export glb` writes the board's copper/soldermask colours but
leaves component meshes with no material, so they render solid white. This
script assigns a material to each component mesh based on its reference
designator (R = resistor, C = capacitor, D = diode/LED, Q = transistor,
U = IC, L = inductor, J = connector, SW = switch), in place.

Usage:
    python tools/recolor_glb.py docs/assets/3d/<board>.glb
    python tools/recolor_glb.py in.glb out.glb

No third-party dependencies (standard library only).
"""
import json
import struct
import sys

# baseColorFactor (linear RGB), metallic, roughness — by ref-designator prefix.
PALETTE = {
    "R": ([0.09, 0.16, 0.42], 0.0, 0.5),    # blue metal-film resistor
    "C": ([0.55, 0.40, 0.18], 0.0, 0.55),   # tan ceramic capacitor
    "D": ([0.10, 0.10, 0.12], 0.0, 0.5),    # dark diode body
    "Q": ([0.04, 0.04, 0.05], 0.0, 0.6),    # black transistor
    "U": ([0.05, 0.05, 0.06], 0.0, 0.55),   # black IC
    "L": ([0.12, 0.12, 0.12], 0.2, 0.5),    # dark inductor
    "J": ([0.05, 0.05, 0.06], 0.0, 0.7),    # black connector/header
    "S": ([0.10, 0.10, 0.12], 0.1, 0.6),    # switch (SW*)
}
DEFAULT = ([0.18, 0.18, 0.20], 0.1, 0.55)   # charcoal for anything else


def recolor(src: str, dst: str) -> None:
    blob = open(src, "rb").read()
    assert blob[:4] == b"glTF", "not a GLB file"
    off, chunks = 12, []
    while off < len(blob):
        clen, ctype = struct.unpack("<I4s", blob[off:off + 8])
        off += 8
        chunks.append([ctype, blob[off:off + clen]])
        off += clen

    gltf = json.loads(chunks[0][1].decode("utf-8"))
    materials = gltf.setdefault("materials", [])
    cache: dict[str, int] = {}

    def material_for(prefix: str) -> int:
        if prefix not in cache:
            color, metal, rough = PALETTE.get(prefix, DEFAULT)
            materials.append({
                "name": f"component_{prefix or 'misc'}",
                "pbrMetallicRoughness": {
                    "baseColorFactor": color + [1.0],
                    "metallicFactor": metal,
                    "roughnessFactor": rough,
                },
            })
            cache[prefix] = len(materials) - 1
        return cache[prefix]

    meshes = gltf["meshes"]
    filled = 0
    for node in gltf.get("nodes", []):
        mi = node.get("mesh")
        name = (node.get("name") or "").strip()
        if mi is None or not name[:1].isalpha():
            continue
        prims = meshes[mi].get("primitives", [])
        if any(p.get("material") is None for p in prims):
            idx = material_for(name[0].upper())
            for p in prims:
                if p.get("material") is None:
                    p["material"] = idx
                    filled += 1

    new_json = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
    while len(new_json) % 4:
        new_json += b" "
    binchunk = chunks[1][1] if len(chunks) > 1 else b""
    while len(binchunk) % 4:
        binchunk += b"\x00"

    total = 12 + 8 + len(new_json) + (8 + len(binchunk) if binchunk else 0)
    out = bytearray(struct.pack("<4sII", b"glTF", 2, total))
    out += struct.pack("<I4s", len(new_json), b"JSON") + new_json
    if binchunk:
        out += struct.pack("<I4s", len(binchunk), b"BIN\x00") + binchunk
    open(dst, "wb").write(out)
    print(f"recoloured {filled} primitives; wrote {dst} ({len(out)} bytes)")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    recolor(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else sys.argv[1])
