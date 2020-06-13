all: notes

notes:
	pandoc -t latex 2019-12-16/.notes-settings.yaml 2019-12-16/notes.md -o 2019-12-16/notes.pdf
	python3 extract-notes.py 2020-06-19/presentation.md 2020-06-19/presentation.pdfpc
