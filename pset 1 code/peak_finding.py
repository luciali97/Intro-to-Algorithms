from __future__ import division

class AdversarialGame(object):
    """
    Represents an instance of the 1D peak-finding game.

    Args:
        n (int): the number of cells in the array. n is guaranteed to be a positive integer.
    """
    def __init__(self, n):
        self.n = n
        ###################### Begin student code ######################
        self.board_state = [None]*n
        self.query_count = 0
        self.low = 0
        self.high = self.n-1
        self.center = int((self.low+self.high)/2)
        self.left_val = 0
        self.left_ind = 0
        self.right_val = 0
        self.right_ind = 0

        ###################### End Student code  #######################

    def query(self, i):
        """
        Returns the value in the ith cell. 
        The return value must be positive and consistent with previous queries.
        """
        ###################### Begin student code ######################
        if self.board_state[i]:
            return self.board_state[i]
        if self.n < 5:
            self.board_state[i] = i+1
            return i+1
        value = self.n
        if i>=self.low and i<=self.center:
            self.low = self.center
            self.center = int((self.low+self.high)/2)                   
        elif i<=self.high and i>self.center:
            self.high = self.center
            self.center = int((self.low+self.high)/2)

        if i<=self.low:
            if self.left_val == 0:
                self.left_val = i+1
                self.left_ind = i
            value = self.left_val+i-self.left_ind
        elif i>=self.high:
            if self.right_val ==0:
                self.right_val = self.n-i
                self.right_ind = i
            value = self.right_val-i+self.right_ind

        #print ('n = ', self.n, 'i = ', i, 'value = ',value)
        self.board_state[i] = value
        return value

        ###################### End Student code  #######################
