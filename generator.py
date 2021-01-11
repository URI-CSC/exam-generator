import sys
import yaml
import random

def print_body(fid):
    fid.write(r"""
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{hyperref}

\linespread{1.25}
\extrawidth{.75in}
\setlength\linefillheight{.5in}

\pagestyle{headandfoot}

\runningheadrule
\firstpageheader
    {CSC 212 / URI}
    {Final Exam}
    {Dec 19, 2020}
\runningheader
    {CSC 212 / URI}
    {Final Exam, Page \thepage\ of \numpages}
    {Dec 19, 2020}
\firstpagefooter
    {}
    {}
    {}
\runningfooter
    {}
    {}
    {}

\begin{document}

~{\large
    \vspace{.5in}

    This exam has \numquestions\ questions, for a total of \numpoints\ points.  You have 2.5 hours to complete the exam.  Please read carefully the guidelines below:

    \begin{itemize}
        \item[-] Your submission to Gradescope must include the following files:
        \begin{enumerate}
            \item A text file named \verb|XXXX.txt|, where \verb|XXXX| are the last four digits of your {\bf student ID}.  \underline{This file is the most important} as it will be used for {\bf grading} your work.  This file must contain your final answers to all questions, one per line.  If you don't have an answer, you can leave the line empty.  A template is provided at: \url{https://homepage.cs.uri.edu/~malvarez/stationary/exam/ans.txt}.
            \item A PDF file named \verb|XXXX.pdf|, where \verb|XXXX| are the last four digits of your {\bf student ID}.  This file will contain your work.  You can write your solutions on your own paper(s) and then scan or photograph them into a single PDF.  Do not worry about alignment or format, as long as your work is readable. In this file, your work on each question can be in any order.
        \end{enumerate}
        \item[-] If the question is multiple choice, the answer {\bf must be} the corresponding letter (A, B, C, ...).  If the question is open, the answer will be a single number, or as otherwise specified in the question.
        \item[-] You may use any of our lecture notes, books, or additional written/online references.  However, when solving the questions, your solution must follow the algorithms and formulas introduced in our lectures.
    \end{itemize}
    
    By submitting my solutions to this exam I acknowledge that I have read and understood the guidelines above, that all answers are my own, and that I have neither gained unfairly from others nor have I assisted others in obtaining an unfair advantage.
}

\pagebreak

\begin{questions}
    """)

######################################################################
######################################################################
######################################################################

def print_tf(fid, q):
    answer = 0
    # shuffle statements in place
    random.shuffle(q['statements'])
    # print question
    fid.write('\n\n\\question[{}] {}'.format(q['points'], q['question']))
    fid.write('\\begin{itemize}')
    for i in range(q['number']):
        fid.write('\t\\item[$({})$] {}'.format(2**i, q['statements'][i][1]))
        if q['statements'][i][0] == 'True':
            answer += 2**i
    fid.write('\\end{itemize}')
    fid.write('\\answerline')
    sys.stderr.write('{}\n'.format(answer))
    # delete used statements
    del q['statements'][0:q['number']]

def print_single(fid, q):
    fid.write('\n\n\\question[{}] {}'.format(q['points'], q['question']))
    fid.write('\\answerline')
    sys.stderr.write('{}\n'.format(q['answer']))

def print_choices(fid, q):
    fid.write('\n\n\\question[{}] {}'.format(q['points'], q['question']))
    fid.write('\\begin{choices}')
    my_list = [ '\\CorrectChoice {}'.format(ans) for ans in q['correct'] ]
    my_list +=  [ '\\choice {}'.format(ans) for ans in q['wrong'] ]        
    random.shuffle(my_list)
    correct = None
    for i in range(len(my_list)):
        if 'CorrectChoice' in my_list[i]:
            correct = i
        fid.write('\t{}'.format(my_list[i]))
    fid.write('\\end{choices}')
    fid.write('\\answerline')
    sys.stderr.write('{}\n'.format(chr(ord('A')+correct)))

def remove_group(db, g):
    # find indices to be removed
    idxs = [i for i in range(len(db)) if 'group' in db[i].keys() and g == db[i]['group']]
    # delete elements
    for idx in sorted(idxs, reverse = True):
        del db[idx] 

def next_question(fid, db, n_q):
    # shuffle questions in place
    random.shuffle(db)
    # print questions and delete used question from pool
    if db[0]['type'] == 'tf':
        print_tf(fid, db[0])
        if len(db[0]['statements']) < db[0]['number']:
            del db[0]
    elif db[0]['type'] == 'single':
        print_single(fid, db[0])
        if n_q != -1 and 'group' in db[0].keys():
            remove_group(db, db[0]['group'])
        else:
            del db[0]
    elif db[0]['type'] == 'choices':
        print_choices(fid, db[0])
        if n_q != -1 and 'group' in db[0].keys():
            remove_group(db, db[0]['group'])
        else:
            del db[0]

def print_latex(fname, n_q, data):
    with open(fname, 'wt') as fid:
        fid.write('\\documentclass[12pt,addpoints]{exam}')
        print_body(fid)
        count = 0
        while len(data) > 0 and (count < n_q or n_q == -1):
            next_question(fid, data, n_q)
            count += 1        
        fid.write('\n\n\\end{questions}')
        fid.write('\n\\end{document}')

def main(yaml_fname, total, out_fname):    
    # load questions
    with open(yaml_fname, 'rt') as in_fid:
        data = yaml.safe_load(in_fid)
    # save exam
    print_latex(out_fname, total, data)

#####################################################################
# get command line arguments
# HOW TO USE THE PROGRAM
# python3 generator.py <YAML_FNAME> <N_QUESTIONS> <LATEX_FNAME> <SEED>
# N_QUESTIONS can be -1 if you want to generate a latex file with ALL
# questions in the databank
#####################################################################
if __name__ == "__main__":
    random.seed(int(sys.argv[4]))
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
