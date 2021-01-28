<!--- 
## Steps to generate exams
### To generate the LaTeX:

```
python3 generator.py <YAML_FNAME> <N_QUESTIONS> <LATEX_FNAME> <SEED>
```

> Can use -1 as `<N_QUESTIONS>` to generate an exam with ALL questions

### To generate the PDF:

```
pdflatex <LATEX_FNAME>
```

> If figures and references are used, then might want to run `pdflatex` twice
--->

# Overview
This tool randomly generates a number of distinct exams (along with their answers) from a given question bank. This is particularly useful for online courses where proctoring exams is considerably more difficult as each student can be given a truly distinct exam. 

# Usage


## Question Bank formatting
Each question is formatted as a yaml dictionary with specifically named fields. The common fields are as follows:


- question: The actual question you wish to pose on the exam, any latex formatting used in the question will carry over to the completed latex source file.

- points: How many points a given question is worth.

<!--- - answer: The correct answer to the powsed question. --->

- group: (OPTIONAL) A means of grouping similar questions together (See [Question Groups](#question-groups))

- type: What type of question is being posed, MUST be one of the question formats in [Supported Question Formats](#supported-question-formats)


### Supported Question Formats
- `single`
    - `single` questions are traditional, single answer, free-response exam questions. They have a single answer, contained within the answer field.
    
    - Example of a fully formatted `single` question:
    ```
    - question: |
        Assuming you have a valid max-heap with $7$ elements such that a post-order traversal outputs the sequence $1,2,\dots,6,7$.  What is the sum of all nodes of height $h=1$?
      points: 7
      type: single
      answer: 9
      group: g1
    ```
    Which corresponds to the following compiled latex:
    
    ![single question example](img/single.png)

- `tf`
    - `tf` questions present students with a set number of true/false questions from a provided bank of true/false questions. They make use of a `statements` field which stores individual true/false questions and their answers, as well as a `number` field, which determines how many questions to pull from the `statements` field for a single exam.
    
    - Example of a fully formatted `tf` question:
    ```
    - question: |
        Considering the statements below, indicate the sum of the values corresponding to all statements that are \verb|True|.  If none are \verb|True|, the answer should be $0$:
      type: tf
      statements:
        - ['True', 'The minimum number of nodes in a binary heap of height $h$ is $2^h$']
        - ['True', 'In the worst-case, the \verb|up-heap| method of a binary heap is less expensive than \verb|down-heap|']
        - ['False', 'Assuming a BST with keys between $1$ and $500$, after searching for $256$, the sequence 352, 28, 40, 50, 45, 47, 46 could be a valid sequence of nodes examined']
        - ['True', 'Assuming a BST with keys between $1$ and $500$, after searching for $256$, the sequence 352, 28, 40, 350, 45, 347, 46 could be a valid sequence of nodes examined']
        - ['True', 'Any complete tree can be efficiently implemented as an array']
        - ['False', 'In a max-heap each key is greater or equal to the keys of all ancestors']
        - ['False', 'Two vertices are adjacent if there is a path of any length connecting them']
        - ['True', 'Two vertices are connected if there is a path of any length connecting them']
      number: 4
      points: 7
    ```

- `choices`
    - info  

### Question Groups