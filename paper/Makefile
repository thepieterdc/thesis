all: abstracts thesis.pdf

abstracts: clean
	(cd abstract-en; latexmk --shell-escape -pdf -quiet extended-abstract.tex; latexmk -c)
	(cd abstract-nl; latexmk --shell-escape -pdf -quiet extended-abstract.tex; latexmk -c)

clean:
	latexmk -C
	(cd abstract-en; latexmk -C; rm -rf extended-abstract.run.xml extended-abstract.synctex.gz)
	(cd abstract-nl; latexmk -C; rm -rf extended-abstract.run.xml extended-abstract.synctex.gz)
	rm -f thesis.acn thesis.glg thesis.glo thesis.gls thesis.ist thesis.lol
	rm -f thesis.bbl
	rm -f thesis.run.xml
	rm -f thesis.synctex.gz

%.pdf: %.tex
	latexmk --shell-escape -pdf -quiet $<
