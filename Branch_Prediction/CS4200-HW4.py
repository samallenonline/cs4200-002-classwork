'''
This program will simulate branch prediction using 
one-bit and two-bit branch predictors.
'''

from random import paretovariate
from random import random 

def next_branch_outcome_loop():
    alpha = 2
    outcome = paretovariate(alpha)
    outcome = outcome > 2
    return outcome

def next_branch_outcome_random():
    outcome = random()
    outcome = outcome > 0.5
    return outcome 

class Predictor:
    def __init__(self):
        self.state = 0

    def next_predict(self):
        '''
        Use this method to return the prediction based off
        of the current state.
        '''
        raise NotImplementedError("Implement this method")
    
    def incorrect_predict(self):
        '''
        Use this method to set the next state if an incorrect
        predict occured. (self.state = next.state)
        '''
        raise NotImplementedError("Implement this method")
    
    def correct_predict(self):
        '''
        Use this method to set the next state if a correct
        predict occured. (self.state = next.state)
        '''
        raise NotImplementedError("Implement this method")
    
class OneBitPredictor(Predictor):
    def __init__(self):
        self.state = 0

    def next_predict(self):
        # if the current state is True,
        if self.state == 1:
            return 1 # predict True
        else: # if the current state is False,
            return 0 # predict False
    
    def incorrect_predict(self):
        # an incorrect prediction occured— set next state accordingly
        if self.state == 1: # flip state
            self.state = 0
        else:
            self.state = 1
    
    def correct_predict(self):
        # a correct prediction occured— set next state accordingly
        if self.state == 1: # keep state
            self.state = 1
        else:
            pass

class TwoBitPredictor(Predictor):
    def __init__(self):
        self.state = 0
        # 0 = 00, 1 = 01, 2 = 10, 3 = 11
        # 00 = strongly not taken
        # 01 = weakly not taken 
        # 10 = weakly taken
        # 11 = strongly taken
        
    def next_predict(self):
        if self.state > 1: # if either strongly or weakly taken,
            return 1 # return true
        else:  
            return 0 # return false

    def incorrect_predict(self):
        # an incorrect prediction occured— set next state accordingly
        # print("Incorrect prediction...")
        if self.state == 3: # strongly taken to weakly taken
            self.state = 2
        elif self.state == 2: # weakly taken to weakly not taken
            self.state = 1
        elif self.state == 0: # strongly not taken to weakly not taken
            self.state = 1
        elif self.state == 1: # weakly not taken to weakly taken
            self.state = 2

    def correct_predict(self):
        # a correct prediction occured— set next state accordingly
        # print("Correct prediction...")
        if self.state == 3: # strongly taken to strongly taken
            self.state = 3
        elif self.state == 2: # weakly taken to strongly taken
            self.state = 3
        elif self.state == 1: # weakly not taken to strongly not taken
            self.state = 0
        elif self.state == 0: # strongly not taken to strongly not taken
            self.state = 0

# EXTRA CREDIT
class NBitPredictor(Predictor):
    def next_predict(self):
        # MY CODE HERE
        raise NotImplementedError()
    
    def incorrect_predict(self):
        # MY CODE HERE
        raise NotImplementedError
    
    def correct_predict(self):
        # MY CODE HERE
        raise NotImplementedError

class main ():
    print("\n2.1 ONE-BIT PREDICTOR")
    ''' 
    2.1.1 Use the next_branch_outcome_random method to generate branch outcomes.
    Use the previously implemented methods to compute a prediction rate.
    '''
    print("------------------------------------------------------")
    print("Random Branch Prediction\n")

    one_bit_predictor1 = OneBitPredictor()

    # create an array of 100 random branch outcomes 
    list_size1 = 100
    branch_outcomes1 = [0] * list_size1
    print("Array of " + str(list_size1) + " random branch outcomes: ")
    for index in range(list_size1):
        branch_outcomes1[index] = next_branch_outcome_random()
        print (1 == branch_outcomes1[index])
    
    correct_predictions = 0
    prediction = 0

    print("\nBranch predictions using one-bit predictor: ")
    for outcome in branch_outcomes1:
        # generate prediction based on current state
        prediction = one_bit_predictor1.next_predict()
        print(1 == prediction)

        # if prediction is correct/incorrect, set state accordingly
        if prediction == outcome:
            one_bit_predictor1.correct_predict()
            correct_predictions += 1
        else:
            one_bit_predictor1.incorrect_predict()

    print("\nNumber of correct predictions: " + str(correct_predictions))

    # compute and print prediction rate 
    prediction_rate = (correct_predictions / list_size1)
    print("The one-bit predictior is correct " + str(prediction_rate * 100) + "% of the time")

    ''' 
    2.1.2 Use the next_branch_outcome_loop method to generate branch outcomes.
    Use the previously implemented methods to compute a prediction rate.
    '''
    print("\n------------------------------------------------------")
    print("Loop Branch Prediction\n")

    one_bit_predictor2 = OneBitPredictor()

    # create an array of 100 loop branch outcomes 
    list_size2 = 100
    branch_outcomes2 = [0] * list_size2
    print("Array of " + str(list_size2) + " loop branch outcomes: ")
    for index in range(list_size2):
        branch_outcomes2[index] = next_branch_outcome_loop()
        print(1 == branch_outcomes2[index])
    
    correct_predictions = 0
    prediction = 0

    print("\nBranch predictions using one-bit predictor: ")
    for outcome in branch_outcomes2:
        # generate prediction based on current state
        prediction = one_bit_predictor2.next_predict()
        print(1 == prediction)

        # if prediction is correct/incorrect, set state accordingly
        if prediction == outcome:
            one_bit_predictor2.correct_predict()
            correct_predictions += 1
        else:
            one_bit_predictor2.incorrect_predict()

    print("\nNumber of correct predictions: " + str(correct_predictions))

    # compute and print prediction rate 
    prediction_rate = (correct_predictions / list_size2)
    print("The one-bit predictior is correct " + str(prediction_rate * 100) + "% of the time")

    print("\n2.2 TWO-BIT PREDICTOR")
    ''' 
    2.2.1 Use the next_branch_outcome_random method to generate branch outcomes.
    Use the previously implemented methods to compute a prediction rate.
    '''
    print("------------------------------------------------------")
    print("Random Branch Prediction\n")

    two_bit_predictor1 = TwoBitPredictor()

    # create an array of 100 random branch outcomes 
    list_size3 = 100
    branch_outcomes3 = [0] * list_size3
    # test_list = [1,0,1,1,1]
    print("Array of " + str(list_size3) + " random branch outcomes: ")
    for index in range(list_size3):
        branch_outcomes3[index] = next_branch_outcome_random()
        print(1 == branch_outcomes3[index])

    correct_predictions = 0

    print("\nBranch predictions using two-bit predictor: ")
    for outcome in branch_outcomes3:
        # generate prediction based on current state
        prediction = two_bit_predictor1.next_predict()
        print(1 == prediction)

        # if prediction is correct/incorrect, set state accordingly
        if prediction == outcome:
            two_bit_predictor1.correct_predict()
            correct_predictions += 1
        else:
            two_bit_predictor1.incorrect_predict()

    print("\nNumber of correct predictions: " + str(correct_predictions))

    # compute and print prediction rate 
    prediction_rate = (correct_predictions / list_size3)
    print("The two-bit predictior is correct " + str(prediction_rate * 100) + "% of the time")
    
    ''' 
    2.2.2 Use the next_branch_outcome_loop method to generate branch outcomes.
    Use the previously implemented methods to compute a prediction rate.
    '''
    print("\n------------------------------------------------------")
    print("Loop Branch Prediction\n")

    two_bit_predictor2 = TwoBitPredictor()

    # create an array of 100 loop branch outcomes 
    list_size4 = 100
    branch_outcomes4 = [0] * list_size4
    # test_list = [1,0,1,1,1]
    print("Array of " + str(list_size4) + " loop branch outcomes: ")
    for index in range(list_size4):
        branch_outcomes4[index] = next_branch_outcome_loop()
        print(1 == branch_outcomes4[index])

    correct_predictions = 0

    print("\nBranch predictions using two-bit predictor: ")
    for outcome in branch_outcomes4:
        # generate prediction based on current state
        prediction = two_bit_predictor2.next_predict()
        print(1 == prediction)

        # if prediction is correct/incorrect, set state accordingly
        if prediction == outcome:
            two_bit_predictor2.correct_predict()
            correct_predictions += 1
        else:
            two_bit_predictor2.incorrect_predict()

    print("\nNumber of correct predictions: " + str(correct_predictions))

    # compute and print prediction rate 
    prediction_rate = (correct_predictions / list_size4)
    print("The two-bit predictor is correct " + str(prediction_rate * 100) + "% of the time")
