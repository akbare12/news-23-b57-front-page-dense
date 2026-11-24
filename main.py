"""news-23 b57 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is empty", file=sys.stderr)
        return 1
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(HERE)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        print("error: MAKEFUN_OUTPUT_DIR must not be inside the repo", file=sys.stderr)
        return 1
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > 1024 * 1024:
        print("error: entry.png over 1 MiB", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: bad PNG signature", file=sys.stderr)
        return 1
    w, h, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (w, h) != (1024, 1024):
        print("error: expected 1024x1024, got %dx%d" % (w, h), file=sys.stderr)
        return 1
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        print("error: malformed PNG trailer", file=sys.stderr)
        return 1
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        check = f.read()
    if check != data:
        print("error: output differs from source", file=sys.stderr)
        return 1
    sha = hashlib.sha256(data).hexdigest()
    print("source: %s (%d bytes, %dx%d, sha256 %s)" % (SRC, len(data), w, h, sha))
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), sha))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
