def say_hello():
    print("Hello, world!")

def add_nums(*args:int)->int:
    return sum(args)
import numpy as np

def get_dim(array:np.array):
    return array.shape[0]


'
next_chatgpt_question='my strategy is like if the  dim is below 7 then first fix at any corner of the borad and then get the list of adjacent corners for the next move if this moves are valid then place the move in the next move as one of the adjacent corner and then try to make the bridge or fork by placing the moves along the edge

