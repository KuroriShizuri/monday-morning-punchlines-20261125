#!/usr/bin/env python3
"""Monday Morning Punchlines - a make.fun one-line joke entry.

Running this script writes the entry line to ``entry.txt`` with no
trailing newline. The competition gate needs 1-200 characters of UTF-8
text that is not only whitespace, so the line is checked before it is
written and the file is read back and compared afterwards.
"""

import os
import sys

LINE = "Monday morning is the only meeting I never agreed to attend, yet somehow I am always the one running late to it."
MAX_CHARS = 200


def output_path():
    """Where entry.txt goes: the grader's output dir, else this folder."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "."
    return os.path.join(out_dir, "entry.txt")


def check_line(text):
    """Raise SystemExit unless the line passes the competition gate."""
    if not text.strip():
        raise SystemExit("entry line must not be blank")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            "entry line is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    text.encode("utf-8")
    return text


def write_entry():
    text = check_line(LINE)
    path = output_path()
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(text.encode("utf-8"))
    with open(path, "rb") as handle:
        written = handle.read().decode("utf-8")
    if written != text:
        raise SystemExit("entry.txt does not match the entry line after writing")
    return path


def self_test():
    """Write to a scratch folder and confirm the bytes are exact."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        old = os.environ.get("MAKEFUN_OUTPUT_DIR")
        os.environ["MAKEFUN_OUTPUT_DIR"] = tmp
        try:
            path = write_entry()
            with open(path, "rb") as handle:
                data = handle.read()
        finally:
            if old is None:
                os.environ.pop("MAKEFUN_OUTPUT_DIR", None)
            else:
                os.environ["MAKEFUN_OUTPUT_DIR"] = old
        expected = LINE.encode("utf-8")
        assert data == expected, "bytes differ: %r vs %r" % (data, expected)
        assert not data.endswith(b"\n"), "entry.txt must have no trailing newline"
        assert len(data) == len(LINE) == 112, "expected 112 bytes"
    print("self-test OK: entry.txt is exactly the 112-character line")


def main(argv):
    if "--self-test" in argv or "--check" in argv:
        check_line(LINE)
        self_test()
        return 0
    path = write_entry()
    print("wrote %s (%d characters, no trailing newline)" % (path, len(LINE)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
