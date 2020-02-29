all: meetings/01-10-2019.pdf \
	meetings/15-10-2019.pdf \
	meetings/20-03-2020.pdf \
	paper \
	proposal/thesis-proposal.pdf \
	reports

.PHONY: paper reports

clean:
	rm -f meetings/*.pdf
	(cd paper/; make clean)
	rm -f proposal/*.pdf
	(cd reports/; latexmk -C)

%.pdf: %.md
	pandoc -N -t latex --latex-engine=xelatex -o $<.pdf $<

paper:
	(cd paper/; make)

reports:
	(cd reports/; make)
