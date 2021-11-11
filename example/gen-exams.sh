python3 ../generator.py ../bank.yaml --n 5 --latex sample-exam-a.tex --output sample-exam-a.ans --preamble ../preamble.tex --seed 1
python3 ../generator.py ../bank.yaml --n 5 --latex sample-exam-b.tex --output sample-exam-b.ans --preamble ../preamble.tex --seed 2
pdflatex sample-exam-a.tex ; pdflatex sample-exam-a.tex ; pdflatex sample-exam-a.tex
pdflatex sample-exam-b.tex ; pdflatex sample-exam-b.tex ; pdflatex sample-exam-b.tex
rm *.aux *.log *.out
