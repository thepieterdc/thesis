all: 2019-12-16/notes.pdf

%.pdf: %.md
	pandoc -t latex .notes-settings.yaml $< -o $@
