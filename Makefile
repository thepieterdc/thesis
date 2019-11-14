all: literature/bronnen.pdf \
		 literature/techniques.pdf \
		 meetings/15-10-2019.pdf \
		 paper \
		 reports \

clean:
	latexmk -c

%.pdf: %.md
	pandoc -N -t latex --latex-engine=xelatex -o $<.pdf $<

paper:
	(cd paper/; make)

reports:
	(cd reports/; make)
