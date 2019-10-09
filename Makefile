all: literature/bronnen.pdf \
		 meetings/15-10-2019.pdf

clean:
	latexmk -c

%.pdf: %.md
	pandoc -N -t latex --latex-engine=xelatex -o $<.pdf $<
