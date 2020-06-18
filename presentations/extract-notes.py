#!/usr/bin/env python3

# Verify arguments.
import sys

in_file, out_file = sys.argv[1:3]

# Parse markdown.
notes = []
with open(in_file, "r") as fh:
    slide_notes = []
    for line in fh.readlines():
        if line.startswith('---'):
            notes.append(slide_notes)
            slide_notes = []

        elif line.startswith('<!-- Note:'):
            slide_notes.append(line[10:].rstrip().rstrip("-->").strip())

# Write file.
with open(out_file, "w+") as fh:
    fh.write("[font_size]\n34\n[notes]\n")
    for slide, slide_notes in enumerate(notes):
        if slide_notes:
            fh.write(f"### {slide + 1}\n")
            for note in slide_notes:
                fh.write(f"{note}\n\n")
