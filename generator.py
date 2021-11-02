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
        # print questions and delete used question from pool
        if self.data[0]['type'] == 'tf':
            self.print_tf(ltx_fid, ans_fid, self.data[0])
            if len(self.data[0]['statements']) < self.data[0]['number']:
                del self.data[0]
        elif self.data[0]['type'] == 'single':
            self.print_single(ltx_fid, ans_fid, self.data[0])
            if self.n_questions != -1 and 'group' in self.data[0].keys():
                self.remove_group(self.data[0]['group'])
            else:
                del self.data[0]
        elif self.data[0]['type'] == 'choices':
            self.print_choices(ltx_fid, ans_fid, self.data[0])
            if self.n_questions != -1 and 'group' in self.data[0].keys():
                self.remove_group(self.data[0]['group'])
            else:
                del self.data[0]

    def print_tf(self, ltx_fid, ans_fid, q):
        answer = 0
        # shuffle statements in place
        random.shuffle(q['statements'])
        # print question
        ltx_fid.write('\n\n\\question[{}] {}'.format(q['points'], q['question']))
        ltx_fid.write('\\begin{itemize}')
        for i in range(q['number']):
            ltx_fid.write('\t\\item[$({})$] {}'.format(2**i, q['statements'][i][1]))
            if q['statements'][i][0] == 'True':
                answer += 2**i
        ltx_fid.write('\\end{itemize}')
        ltx_fid.write('\\answerline')
        ans_fid.write('{}\n'.format(answer))
        # delete used statements
        del q['statements'][0:q['number']]

    def print_single(self, ltx_fid, ans_fid, q):
        ltx_fid.write('\n\n\\question[{}] {}'.format(q['points'], q['question']))
        ltx_fid.write('\\answerline')
        ans_fid.write('{}\n'.format(q['answer']))

    def print_choices(self, ltx_fid, ans_fid, q):
        ltx_fid.write('\n\n\\question[{}] {}'.format(q['points'], q['question']))
        ltx_fid.write('\\begin{choices}')
        my_list = [ '\\CorrectChoice {}'.format(ans) for ans in q['correct'] ]
        my_list +=  [ '\\choice {}'.format(ans) for ans in q['wrong'] ]        
        random.shuffle(my_list)
        correct = None
        for i in range(len(my_list)):
            if 'CorrectChoice' in my_list[i]:
                correct = i
            ltx_fid.write('\t{}'.format(my_list[i]))
        ltx_fid.write('\\end{choices}')
        ltx_fid.write('\\answerline')
        ans_fid.write('{}\n'.format(chr(ord('A')+correct)))

    def remove_group(self, g):
        # find indices to be removed
        idxs = [i for i in range(len(self.data)) if 'group' in self.data[i].keys() and g == self.data[i]['group']]
        # delete elements
        for idx in sorted(idxs, reverse = True):
            del self.data[idx] 

#####################################################################
#####################################################################
#####################################################################
if __name__ == "__main__":
    ## configure the command line options
    parser = ap.ArgumentParser(description='Generate a random exam in LaTeX format.')
    parser.add_argument('yaml_fname', help='File name for the question bank')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', action='store', type=int, default=0, help='number of questions (default: 4)')
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
