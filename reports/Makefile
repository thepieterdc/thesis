all: 2019-11-02-progress.pdf 2020-02-16-progress.pdf

clean:
	latexmk -C

%.pdf: %.tex
	 		 latexmk --shell-escape -pdf $<
			 latexmk -c
