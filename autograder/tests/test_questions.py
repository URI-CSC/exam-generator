import re
import glob
import unittest
from gradescope_utils.autograder_utils.decorators import weight, number

class TestQuestions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # verify both files exist
        cls.pdf = glob.glob('/autograder/submission/[0-9][0-9][0-9][0-9].pdf')
        cls.txt = glob.glob('/autograder/submission/[0-9][0-9][0-9][0-9].txt')
        if len(cls.txt)==1 and len(cls.pdf)==1:
            cls.id = cls.txt[0][-8:-4]
            # read in correct answers            
            cls.correct = {}
            with open('./solution/'+cls.id+'.ans', 'rt') as fid:
                count = 1
                lines = fid.readlines()
                for line in lines:
                    cls.correct['{}.'.format(count)] = list(filter(lambda x: x!= '', re.split(',| |\t', line.strip())))
                    count += 1
            # read in student's solutions
            cls.answers = {}
            with open(cls.txt[0], 'rt') as fid:
                lines = fid.readlines()
                for line in lines:
                    line = line.strip()
                    match = re.match('^\d+\.', line) 
                    if match:
                        cls.answers[match[0]] = list(filter(lambda x: x!= '', re.split(',| |\t', re.sub('^\d+\.', '',line))))

    def myfail(self, q):        
        self.fail('\nYour Answer: {}'.format(' '.join(self.answers[q])))

    def grade(self, q):
        if len(self.txt) != 1 or len(self.pdf) != 1:
            self.fail('Missing 1 or more required files')
        if q not in self.answers:
            self.fail('Answer for this question not found')
        print('Correct Answer: {}\n'.format(' '.join(self.correct[q])))        
        if len(self.correct[q]) != len(self.answers[q]):
            self.myfail(q)
        for i in range(len(self.correct[q])):
            if self.correct[q][i].lower().strip() != self.answers[q][i].lower().strip():
                self.myfail(q)

    @weight(7)
    def test_q01(self):
        """Question 01"""
        self.grade('1.')

    @weight(7)
    def test_q02(self):
        """Question 02"""
        self.grade('2.')

    @weight(7)
    def test_q03(self):
        """Question 03"""
        self.grade('3.')

    @weight(7)
    def test_q04(self):
        """Question 04"""
        self.grade('4.')

    @weight(7)
    def test_q05(self):
        """Question 05"""
        self.grade('5.')

    @weight(7)
    def test_q06(self):
        """Question 06"""
        self.grade('6.')

    @weight(7)
    def test_q07(self):
        """Question 07"""
        self.grade('7.')

    @weight(7)
    def test_q08(self):
        """Question 08"""
        self.grade('8.')

    @weight(7)
    def test_q09(self):
        """Question 09"""
        self.grade('9.')

    @weight(7)
    def test_q10(self):
        """Question 10"""
        self.grade('10.')

    @weight(7)
    def test_q11(self):
        """Question 11"""
        self.grade('11.')

    @weight(7)
    def test_q12(self):
        """Question 12"""
        self.grade('12.')

    @weight(7)
    def test_q13(self):
        """Question 13"""
        self.grade('13.')

    @weight(7)
    def test_q14(self):
        """Question 14"""
        self.grade('14.')

    @weight(7)
    def test_q15(self):
        """Question 15"""
        self.grade('15.')

    @weight(7)
    def test_q16(self):
        """Question 16"""
        self.grade('16.')
