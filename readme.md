# Intro TO NLP Assignment 1
# Submitted by - Somya Lalwani (2020201092)

## Tokenization

Run the tokenization.py file using the command
`python3 2020201092_tokenization.py`

## LM 
To run the language model code, use the command:-
`python3 language_model.py <smoothing type> <path to corpus>`
example
python3 language_model.py k ./medical-corpus.txt


- Smoothing type can be k for Kneyser-Ney or w for Witten-Bell.
- an example:
    `$ python3 language_model.py k ./corpus.txt`
    `input sentence: I am a man.`
    `0.89972021`