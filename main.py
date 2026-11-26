"""Texts From Your Future Self — make.fun entry.

Writes one line (94 chars) to /output/entry.txt, no trailing newline.
Stdlib only, no network.
"""

import os
import sys

LINE = "It's me, you, ten years from now. The gym membership is still charging you. It always will be."


def main():
    # Guards: sealed gate is 1-200 UTF-8 chars, single line, not only whitespace.
    assert isinstance(LINE, str)
    assert 1 <= len(LINE) <= 200, f"line length {len(LINE)} outside 1-200"
    assert LINE.strip(), "line is only whitespace"
    assert "\n" not in LINE and "\r" not in LINE, "line must be a single line"
    encoded = LINE.encode("utf-8")  # strict UTF-8 round-trip
    assert encoded.decode("utf-8") == LINE
    assert not encoded.startswith(b"\xef\xbb\xbf"), "no BOM allowed"
    assert "  " not in LINE, "no double spaces"
    assert LINE == LINE.strip(), "no leading/trailing whitespace"
    assert not any(ord(c) < 32 for c in LINE), "no control characters"

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(encoded)

    # Read-back byte-for-byte verification.
    with open(path, "rb") as f:
        back = f.read()
    assert back == encoded, "read-back mismatch"
    assert len(back.decode("utf-8")) == 94, "char count mismatch"
    # Entry must read as a text message from the future self: first person,
    # a time jump, and a concrete ongoing fact — all present by construction.
    assert LINE.startswith("It's me, you,"), "future-self voice check"
    assert "ten years from now" in LINE, "time-jump check"


if __name__ == "__main__":
    main()
