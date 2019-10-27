all: 2019-11-02-progress.pdf

clean:
	latexmk -C

%.pdf: %.tex
	 		 latexmk --shell-escape -pdf $<
			 latexmk -c
