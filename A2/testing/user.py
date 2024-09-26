from utensile import *
# say_hello()
# print(add_nums(1, 2, 3, 4, 5))


import numpy as np
array=np.array([0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[3,0,0,0,0,0,3],[3,3,0,0,0,3,3],[3,3,3,0,3,3,3])
print(array().shape)

class This_test:
    def __init__(self,name,age,nums=[0]) -> None:
        self.name:str =name
        self.age:int=age
        self.nums:list[int]=nums
        self.sum=self.sum_nums(nums)
    
    def sum_nums(self,nums:list[int]) -> int:
        r=0
        for i in nums:
            r=add_nums(r,i)
        return r
    def desciption(self):
        print(f'Name: {self.name}, Age: {self.age}, Sum: {self.sum}')
        
    
def main():
    my_test=This_test('John',25,[1,2,3,4,5])
    my_test.desciption()
    # print(get_dim(array))
    
if __name__ == '__main__':
    main()