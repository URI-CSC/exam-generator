import sys
import yaml
import random

def print_body(fid):
    fid.write(r"""
\usepackage{listings}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{forest}

\linespread{1.25}
\extrawidth{.75in}
\lstset{language=C++}
\bracketedpoints
\setlength\linefillheight{.5in}
\newcommand{\tf}[1][{}]{%
    \fillin[#1][0.5in]%
}

\pagestyle{headandfoot}

\runningheadrule
\firstpageheader
    {CSC 212 / URI}
    {Midterm Exam}
    {Oct 27, 2020}
\runningheader
    {CSC 212 / URI}
    {Midterm Exam, Page \thepage\ of \numpages}
    {Apr 27, 2020}
\firstpagefooter
    {}
    {}
    {}
\runningfooter
    {}
    {}
    {}

\begin{document}

\begin{center}
    \fbox{\fbox{
        \parbox{5.5in}
        {\centering This exam has \numquestions\ questions, for a total of \numpoints\ points.  Please write your name and mark your answers {\bf clearly} on the bubble sheet template provided.}
    }}
\end{center}

\vspace{.2in}

\begin{questions}
    """)

def print_questions(fid, ansfid, n_questions, questions):
    # if all questions must be printed
    if n_questions < 0:
        for q in questions:
            print_question(fid, ansfid, q)
    # if a specific total is provided
    else:
        idx = 0
        count = 0
        groups = set()
        random.shuffle(questions)
        for q in questions:
            if count == n_questions:
                break
            if 'group' in q.keys():
                if q['group'] in groups:
                    continue
                groups.add(q['group'])
            print_question(fid, ansfid, q)
            count += 1

def print_question(fid, ansfid, q):
    my_list = []
    fid.write('\n\n\\question[{}] {}'.format(q['points'], q['question']))
    ansfid.write('\n\n\\question[{}] {}'.format(q['points'], q['question']))
    fid.write('\n\\begin{{{}}}'.format(q['type']))
    ansfid.write('\n\\begin{{{}}}'.format(q['type']))
    for ans in q['correct']:
        my_list.append('\\CorrectChoice {}'.format(ans))
    for ans in q['wrong']:
        my_list.append('\\choice {}'.format(ans))
    random.shuffle(my_list)
    for item in my_list:
        fid.write('\n\t{}'.format(item))
        ansfid.write('\n\t{}'.format(item))
    fid.write('\n\\end{{{}}}'.format(q['type']))
    ansfid.write('\n\\end{{{}}}'.format(q['type']))
        
def save_exam(fname, n_questions, questions):
    answer = 'answer-'+fname
    with open(fname, 'wt') as fid, open(answer, 'wt') as ansfid:
        fid.write('\\documentclass[12pt,addpoints{}]{{exam}}'.format(''))
        ansfid.write('\\documentclass[12pt,addpoints{}]{{exam}}'.format(',answers'))
        print_body(fid)
        print_body(ansfid)
        print_questions(fid, ansfid, n_questions, questions)
        fid.write('\n\n\\end{questions}')
        ansfid.write('\n\n\\end{questions}')
        fid.write('\n\\end{document}')
        ansfid.write('\n\\end{document}')

#####################################################################
# get command line arguments
# HOW TO USE THE PROGRAM
# python3 generator.py <YAML_FNAME> <N_QUESTIONS> <LATEX_FNAME>
# N_QUESTIONS can be -1 if you want to generate a latex file with ALL
# questions in the databank
#####################################################################
random.seed()
yaml_fname = sys.argv[1]
total = int(sys.argv[2]) # use -1 to print all
out_fname = sys.argv[3]

# load questions
with open(yaml_fname, 'rt') as in_fid:
    data = yaml.safe_load(in_fid)

# save two versions
save_exam(out_fname, total, data)
#save_exam('answers-'+out_fname, True, total, data)

## !!!!!!!
## NEED TO IMPROVE HOW TO GENERATE SOLUTIONS KEEPING THE SAME ORDER OF CHOICES FOR THE ANSWERS AND THE NON ANSWERS
## !!!!!!!
