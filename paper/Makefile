all: thesis.pdf

clean:
	latexmk -C
	rm -f thesis.run.xml
	rm -f thesis.synctex.gz


%.pdf: %.tex
	 latexmk --shell-escape -pdf $<
	 latexmk -c
