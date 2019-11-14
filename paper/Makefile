all: thesis.pdf

clean:
	latexmk -C

%.pdf: %.tex
	 		 latexmk --shell-escape -pdf $<
			 latexmk -c
