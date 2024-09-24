import heapq


class PriorityQueue:
    def __init__(self,max_len):
        self.items = []
        self.max_len=max_len

    def push(self,item):
        sort_value = item[0]
        heapq.heappush(self.items,(sort_value,item))
        if len(self.items)>self.max_len:
            self.items=heapq.nsmallest(self.max_len,self.items)
            heapq.heapify(self.items)
    
    def pop(self):
        return heapq.heappop(self.items)[1]
    
    def is_empty(self):
        return len(self.items)==0
    
    def __len__(self):
        return len(self.items)
    
    def __repr__(self):
        return repr([item[1] for item in sorted(self.items)])




class Agent(object):
    def __init__(self, phoneme_table, vocabulary) -> None:
        """
        Your agent initialization goes here. You can also add code but don't remove the existing code.
        """
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None
        self.environment = None
       
        self.min_cost=float('inf')
        self.table_correction(phoneme_table)
        self.max_key_len=max([len(key) for key in self.phoneme_table])
       
    def table_correction(self, table):
        """_summary_
            This function is used to correct phoneme table as the given phoneme table which converts
            correct_phoneme : List[ incorrect_phoneme] to incorrect_phoneme : List[correct_phoneme]
            by this we can able to replace the given substring with the correct phoneme compared with the previous table. 

        Args:
            table (str:List[str]): It is the phoneme table which contains the correct_phoneme : List[ incorrect_phoneme]
        """
        new_table = {}
        for key, values in table.items():
            for value in values:
                if value not in new_table:
                    new_table[value] = [key]
                else:
                    new_table[value].append(key)
        self.phoneme_table = new_table
 

    def phoneme_correction(self, environment):
        """_summary_
            This function is used to correct the similar sounding character errors in the given sentence 
            generated by the Automatic Speech Recognition(ASR) system. It uses the phoneme table to generate 
            the possible states from the given state and then selects the best state from the generated 
            states based on the cost function. It uses the 2 Priority Queues queue to generate the next states 
            and make the makes the next state in queue of the fixed length of 5. 
        Args:
            environment (Object):
                This contains the Object which contains the initial state and computing cost which is used to give the cost of the sentence 
                this is used to evaluate the cost of the sentence 
        
        Returns:
            None: But modifies the best_state and the minimum cost of the sentence
        """
        init_state = environment.init_state        
        cost=environment.compute_cost(init_state)

        queue = PriorityQueue(5)
        queue.push((cost,init_state,0))
        while not queue.is_empty():
            new_queue=PriorityQueue(5)
            while not queue.is_empty():
                current_cost,current_state,start=queue.pop()
                if start>=len(current_state):
                    if self.min_cost>current_cost:
                        self.min_cost=current_cost
                        self.best_state=current_state
                        
                    continue
                for next_state,point in self.generate_states(current_state,start):
                    next_cost=environment.compute_cost(next_state)
                    new_queue.push((next_cost,next_state,point))
            
            queue=new_queue
            
            
    def generate_states(self,current_state,start):
        """
            This function is used to generate the next neighbor states from a given point of the current state and then returns all this neighbors states

        Args:
            current_state (string): It is the current state from which the next states will be generated
            start (int): This is the point of the current state from which the next states will be generated

        Returns:
            List[(str,int)]:It gives the list of Neighbours states and there next starting point
        """
        new_states=[]
        for j in range(1,self.max_key_len+1):
            if start+j>len(current_state):
                break
            substring=current_state[start:start+j]
            if substring in self.phoneme_table:
                for value in self.phoneme_table[substring]:
                    new_state=current_state[:start]+value+current_state[start+j:]
                    new_states.append((new_state,start+len(value)))
        new_states.append((current_state,start+1))
        return new_states       
        
        
            
    def vocabulary_correction(self, environment):
        """
            This function is used to correct the vocabulary errors in the given sentence 
            generated by the Automatic Speech Recognition(ASR) system. It uses the Vocabulary table for the solving
            the whole word missing error by  making the word of the vocabulary table is placed at the beginning or end of the sentence
            and then calculating the cost of the sentence. It selects the best state from the generated gives the best state and min_cost 
            of the given sentence

        Args:
            environment (Object):
                This contains the Object which contains the initial state and computing cost which is used to give the cost of the sentence 
                this is used to evaluate the cost of the sentence 
        
        Returns:
            None: But modifies the best_state and the minimum cost of the sentence      
        """
        vocabulary = self.vocabulary
        current_state = self.best_state
        self.min_cost = environment.compute_cost(current_state)
        for word in vocabulary:
            next_state = f'{word} {current_state}'
            next_cost = environment.compute_cost(next_state)
            if next_cost < self.min_cost:
                self.best_state = next_state
                self.min_cost = next_cost
        
        for word in vocabulary:
            next_state = f'{current_state} {word}'
            next_cost = environment.compute_cost(next_state)
            if next_cost < self.min_cost:
                self.best_state = next_state
                self.min_cost = next_cost
        
    def asr_corrector(self, environment):
        """
        Your ASR corrector agent goes here. Environment object has following important members.
        - environment.init_state: Initial state of the environment. This is the text that needs to be corrected.
        - environment.compute_cost: A cost function that takes a text and returns a cost. E.g., environment.compute_cost("hello") -> 0.5

        Your agent must update environment.best_state with the corrected text discovered so far.
        """
        self.best_state = environment.init_state
        cost = environment.compute_cost(environment.init_state)
        self.min_cost = cost
        # print(f'Initial State: {self.best_state} \nMinimum Cost: {self.min_cost}')
        self.phoneme_correction(environment)
        self.vocabulary_correction(environment)
        # print(f'Best State after Phoneme Correction: {self.best_state}')
        # print(f'Minimum Cost: {self.min_cost}')
