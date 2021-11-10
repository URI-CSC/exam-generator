import yaml
import random
import argparse as ap

#####################################################################
#####################################################################
#####################################################################
class Generator:
    def __init__(self, args):
        self.latex_fname = args.latex
        self.output_fname = args.output
        self.n_questions = -1 if args.all else args.n
        # load questions
        with open(args.yaml_fname, 'rt') as in_fid:
            self.data = yaml.safe_load(in_fid)
        # load preamble
        with open(args.preamble, 'rt') as in_fid:
            self.preamble = in_fid.read()

    def run(self):
        with open(self.latex_fname, 'wt') as ltx_fid, open(self.output_fname, 'wt') as ans_fid:
            # top
            ltx_fid.write('\\documentclass[12pt,addpoints]{exam}\n')
            ltx_fid.write(self.preamble)
            ltx_fid.write('\n\pagebreak\n')
            ltx_fid.write('\n\\begin{questions}')
            # questions
            count = 0
            while len(self.data) > 0 and (count < self.n_questions or self.n_questions == -1):
                self.next_question(ltx_fid, ans_fid)
                count += 1        
            # bottom
            ltx_fid.write('\n\n\\end{questions}')
            ltx_fid.write('\n\n\\end{document}')

    def next_question(self, ltx_fid, ans_fid):
        # shuffle questions in place
        random.shuffle(self.data)
        q = self.data[0]
        # print question header
        ltx_fid.write('\n\n\\question[{}] {}\n'.format(q['points'], q['head'] if 'head' in q.keys() else ''))
        # print questions and delete used question from pool
        if q['type'] == 'tf':
            self.print_tf(ltx_fid, ans_fid, q)
            if len(q['statements']) < q['number']:
                del self.data[0]
        elif q['type'] == 'single':
            self.print_single(ltx_fid, ans_fid, q)
            if self.n_questions != -1 or len(q['question']) == 0:
                del self.data[0]
        elif q['type'] == 'choices':
            self.print_choices(ltx_fid, ans_fid, q)
            if self.n_questions != -1 or len(q['question']) == 0:
                del self.data[0]

    def print_tf(self, ltx_fid, ans_fid, q):
        answer = 0
        # shuffle statements in place
        random.shuffle(q['statements'])
        # print question
        ltx_fid.write(q['question'])
        ltx_fid.write('\\begin{itemize}')
        for i in range(q['number']):
            ltx_fid.write('\n\t\\item[$({})$] {}'.format(2**i, q['statements'][i][1]))
            if q['statements'][i][0] == 'True':
                answer += 2**i
        ltx_fid.write('\\end{itemize}')
        ltx_fid.write('\n\\answerline')
        ans_fid.write('{}\n'.format(answer))
        # delete used statements
        del q['statements'][0:q['number']]

    def print_single(self, ltx_fid, ans_fid, q):
        idx = random.randint(0, len(q['question'])-1)
        ltx_fid.write(q['question'][idx])
        ltx_fid.write('\n\\answerline')
        ans_fid.write('{}\n'.format(q['answer'][idx]))
        del q['question'][idx]
        del q['answer'][idx]

    def print_choices(self, ltx_fid, ans_fid, q):
        idx = random.randint(0, len(q['question'])-1)
        ltx_fid.write(q['question'][idx])
        ltx_fid.write('\n\\begin{choices}')
        my_list = []
        if 'common' in q.keys():
            my_list += [ '\n\t\\choice {}'.format(ans) for ans in q['common'] ]
        my_list += ['\n\t\\choice {}'.format(q['answer'][idx])]
        wrong = random.sample(range(len(q['random'])), 5 - len(my_list))
        my_list += [ '\n\t\\choice {}'.format(q['random'][i]) for i in wrong ]
        random.shuffle(my_list)
        [ltx_fid.write('\t{}'.format(ch)) for ch in my_list]
        ltx_fid.write('\n\\end{choices}')
        ltx_fid.write('\n\\answerline')
        correct = [k for k, s in enumerate(my_list) if q['answer'][idx] in s]
        assert(len(correct) == 1)
        ans_fid.write('{}\n'.format(chr(ord('A')+correct[0])))
        del q['question'][idx]
        del q['answer'][idx]

#####################################################################
#####################################################################
#####################################################################
if __name__ == "__main__":
    ## configure the command line options
    parser = ap.ArgumentParser(description='Generate a random exam in LaTeX format.')
    parser.add_argument('yaml_fname', help='File name for the question bank')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--n', action='store', type=int, default=4, help='number of questions (default: 4)')
    group.add_argument('--all', help='output ALL questions', action='store_true')
    parser.add_argument('--latex', metavar='<latex_fname>', action='store', help='File name for the LaTeX output', required=True)
    parser.add_argument('--output', metavar='<output_fname>', action='store', help='File name for the answers file', required=True)
    parser.add_argument('--preamble', metavar='<preamble_fname>', action='store', help='File name for the LaTeX preamble section', required=True)
    parser.add_argument('--seed', metavar='<seed>', action='store', type=int, default=0, help='seed value for the random generator (default: 0)')
    arguments = parser.parse_args()

    ## initialize the seed and launch the main() function    
    random.seed(arguments.seed)
    generator = Generator(arguments)
    generator.run()
