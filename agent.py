import random
import re

hold = []
holdcounter = 0
readfrom = 0
gamenumber = 1
dict = {
}

def flips( board, index, piece, step ):
   other = ('X' if piece == 'O' else 'O')
   # is an opponent's piece in first spot that way?
   here = index + step
   if here < 0 or here >= 36 or board[here] != other:
      return False
      
   if( abs(step) == 1 ): # moving left or right along row
      while( here // 6 == index // 6 and board[here] == other ):
         here = here + step
      # are we still on the same row and did we find a matching endpiece?
      return( here // 6 == index // 6 and board[here] == piece )
   
   else: # moving up or down (possibly with left/right tilt)
      while( here >= 0 and here < 36 and board[here] == other ):
         here = here + step
      # are we still on the board and did we find a matching endpiece?
      return( here >= 0 and here < 36 and board[here] == piece )
   
# decide if this is a valid move
def isValidMove( b, x, p ): # board, index, piece
   # invalid index
   if x < 0 or x >= 36:
      return False
   # space already occupied
   if b[x] != '-':
      return False 
   # otherwise, check for flipping pieces
   up    = x >= 12   # at least third row down
   down  = x <  24   # at least third row up
   left  = x % 6 > 1 # at least third column
   right = x % 6 < 4 # not past fourth column
   return (          left  and flips(b,x,p,-1)  # left
         or up   and left  and flips(b,x,p,-7)  # up/left
         or up             and flips(b,x,p,-6)  # up
         or up   and right and flips(b,x,p,-5)  # up/right
         or          right and flips(b,x,p, 1)  # right
         or down and right and flips(b,x,p, 7)  #down/right
         or down           and flips(b,x,p, 6)  # down
         or down and left  and flips(b,x,p, 5)) # down/left


class Agent:
   
    symbol = 'X'
   
    def __init__( self, xORo ):
        self.symbol = xORo
    
    def getMove( self, gameboard ):
        global readfrom
        global holdcounter
        # play in the next open space, looking from top corner
        hold.append(gameboard)
        holdcounter += 1
        # picks a random point, then cycles to the next available space
        if readfrom == 0:
            if self.symbol == "O":
                try:
                    with open("trainingO.txt", "r") as file:
                        lines = file.readlines()
                        #line = lines.split(",")
                        #print(lines)
                        for i in range(len(lines)):
                            #print(len(lines))
                            line = lines[i]
                            #print(line)
                            splitlines = line.split(",")
                            values = []
                            #print(len(splitlines))
                            for n in range(len(splitlines)):
                                if n != 0:
                                    #print(splitlines[n])
                                    values.append(splitlines[n].rstrip("\n"))
                            dict.update({splitlines[0] : values})
                        readfrom = 1
                except:
                    m = random.randint(0,36)
                    while not isValidMove(gameboard,m,self.symbol):
                        m = ( m + 1 ) % 36
                    readfrom = 1
                    return m
            else:
                try:
                    f = open("trainingX.txt", "r")
                    lines = f.readlines
                    values = []
                    for line in lines:
                        splitlines = line.split(",")
                        for i in range(len(splitlines)):
                            if i == 0:
                                continue
                            else:
                                values[i-1] = splitlines[i]
                        dict.update({splitlines[0] : values})
                        readfrom = 1
                    f.close()
                except:
                    m = random.randint(0,36)
                    while not isValidMove(gameboard,m,self.symbol):
                        m = ( m + 1 ) % 36
                    readfrom = 1
                    return m
            readfrom = 1
        if gameboard in dict:
            x = random.random()
            y = dict[gameboard]
            # print(y)
            m = 0
            l = 0
            for i in range(1, len(y), 2):
                x -= float(y[i])
                if x <= 0:
                    return int(y[i-1])
                elif l > 10:
                    break
                l += 1
        m = random.randint(0,36)
        while not isValidMove(gameboard,m,self.symbol):
            m = ( m + 1 ) % 36
        return m
     
    # Try using arrays instead of using a dictionary because I have no idea what I am doing
    def endGame( self, status, gameboard):
        global holdcounter
        global gamenumber
        multiplier = 0.20
        #print(gamenumber)
        gamenumber += 1
        if gamenumber % 100 == 0:
            print(gamenumber)
        numofmoves = 0
        hold.append(gameboard)
        numofmoves = holdcounter
        #print("help")
        if status == 1:
            if self.symbol == "X":
                while (len(hold) > 0):
                    holdinghold = hold.pop()
                    holdcounter -= 1
                    opposite = len(holdinghold)
                    if holdcounter < 0:
                        checkhold = "--------------XO----OX--------------"
                        placeholder = dict.items()
                        checkcheckhold = -1
                        check = False
                        holding = []
                        if checkhold in dict:
                            valueholder = dict.items()[i]
                            checkarray2 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
                            for i in range(36):
                                if holdinghold[i] != checkhold[i] and checkhold[i] == "X":
                                    checkcheckhold = i
                                if isValidMove(holdinghold, i, "X"):
                                    checkarray2[i] = True
                            for i in range(len(valueholder)):
                                if valueholder[i] == checkcheckhold:
                                    valueholder[i] = str(float(valueholder[i]) * 1.5)
                                    holding.append(float(valueholder[i]) * 1.5 - float(valueholder[i]))
                            dict.update({holdinghold: holding})
                        else:
                            hol = []
                            dict.update({holdinghold: holdinghold})
                            counter = 0.0
                            for i in range(36):
                                if isValidMove(holdinghold, i, "X"):
                                    counter += 1
                            for i in range(36):
                                if isValidMove(holdinghold, i, "X"):
                                    hol.append(str(i))
                                    hol.append(str(float(1/counter)))
                            dict.update({holdinghold: hol})
                    else:
                        checkhold = hold[holdcounter]
                    placeholder = dict.items()
                    checkcheckhold = -1
                    check = False
                    holding = []
                    if holdinghold in dict:
                        valueholder = dict.items()[i]
                        checkarray2 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
                        for i in range(36):
                            if holdinghold[i] != checkhold[i] and checkhold[i] == "X":
                                checkcheckhold = i
                            if isValidMove(holdinghold, i, "X"):
                                checkarray2[i] = True
                        for i in range(len(valueholder)):
                            if valueholder[i] == checkcheckhold:
                                valueholder[i] = str(float(valueholder[i]) * 1.5)
                                holding.append(float(valueholder[i]) * 1.5 - float(valueholder[i]))
                        dict.update({holdinghold: holding})
                    if check != True:
                        hol = []
                        dict.update({holdinghold: holdinghold})
                        counter = 0.0
                        for i in range(36):
                            if isValidMove(holdinghold, i, "X"):
                                counter += 1
                        for i in range(36):
                            if isValidMove(holdinghold, i, "X"):
                                hol.append(str(i))
                                hol.append(str(float(1/counter)))
                        dict.update({holdinghold: hol})

            else:
                while (len(hold) > 0):
                    opposite = len(hold)
                    holdinghold = hold.pop()
                    holdcounter -= 1
                    if holdcounter < 0:
                        checkhold = "--------------XO----OX--------------"
                    else:
                        checkhold = hold[holdcounter]
                    placeholder = dict.items()
                    checkcheckhold = -1
                    check = False
                    holding = []
                    if checkhold in dict:
                        valueholder = dict[checkhold]
                        helpcount = 0
                        checkarray2 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
                        for i in range(36):
                            if holdinghold[i] == "O" and checkhold[i] == "-":
                                checkcheckhold = i
                            if isValidMove(checkhold, i, "O"):
                                checkarray2[i] = True
                                helpcount += 1
                        for i in range(len(valueholder)):
                            holder = 0.0
                            if opposite < 0:
                                break
                                # print(holdcounter)
                                # print(numofmoves)
                            #print("close")
                            for k in range(36):
                                difference = 0.0
                                if k == checkcheckhold:
                                # print(valueholder[n])
                                # print(k)
                                    if str(valueholder[i]) == str(k) and i != checkcheckhold:
                                        #print("learned")
                                        holder = float(valueholder[i+1])
                                        holder = holder * (1.0 + (opposite * 0.05))
                                        if holder > 1.0:
                                            difference = holder - 1.0
                                            holder = 1.0
                                        valueholder[i+1] = holder
                                        holding.append(k)
                                        holding.append(str(float(valueholder[i+1])))
                                # print(valueholder[n])
                                # print(k)
                                elif str(valueholder[i]) == str(k) and i != checkcheckhold:
                                    #print("learned2")
                                    #print(valueholder[n+1])
                                    holder = float(valueholder[i+1])
                                    holder = difference + holder - holder * (1.0 + (opposite * 0.05))
                                    valueholder[i+1] = float(valueholder[i+1]) + holder/numofmoves
                                    holding.append(k)
                                    holding.append(valueholder[i+1])
                            #print("Opposite " + str(opposite))
                        #print(checkhold)
                        #print(holding)
                            dict.update({checkhold: holding})
                    else:
                        hol = []
                        dict.update({checkhold: checkhold})
                        counter = 0.0
                        for i in range(36):
                            if isValidMove(checkhold, i, "O"):
                                counter += 1
                        for i in range(36):
                            if isValidMove(checkhold, i, "O"):
                                hol.append(str(i))
                                hol.append(str(float(1/counter)))
                        dict.update({checkhold: hol})

        elif status == -1:
            if self.symbol == "X":
                while (len(hold) > 0):
                    holdinghold = hold.pop()
                    holdcounter -= 1
                    if holdcounter < 0:
                        checkhold = "--------------XO----OX--------------"
                        placeholder = dict.items()
                        checkcheckhold = -1
                        check = False
                        holding = []
                        if checkhold in dict:
                            valueholder = dict.items()[i]
                            checkarray2 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
                            for i in range(36):
                                if holdinghold[i] != checkhold[i] and checkhold[i] == "X":
                                    checkcheckhold = i
                                if isValidMove(checkhold, i, "X"):
                                    checkarray2[i] = True
                            for i in range(len(valueholder)):
                                if valueholder[i] == checkcheckhold:
                                    valueholder[i] = str(float(valueholder[i]) * 1.5)
                                    holding.append(float(valueholder[i]) * 1.5 - float(valueholder[i]))
                            dict.update({checkhold: holding})
                        else:
                            hol = []
                            dict.update({checkhold: checkhold})
                            counter = 0.0
                            for i in range(36):
                                if isValidMove(checkhold, i, "X"):
                                    counter += 1
                            for i in range(36):
                                if isValidMove(checkhold, i, "X"):
                                    hol.append(str(i))
                                    hol.append(str(float(1/counter)))
                            dict.update({checkhold: hol})
                    else:
                        checkhold = hold[holdcounter]
                    placeholder = dict.items()
                    checkcheckhold = -1
                    check = False
                    holding = []
                    for i in range(len(placeholder)):
                        if holdinghold == placeholder[i][0]:
                            valueholder = dict.items()[i]
                            checkarray2 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
                            for i in range(36):
                                if holdinghold[i] != checkhold[i] and checkhold[i] == "X":
                                    checkcheckhold = i
                                if isValidMove(holdinghold, i, "X"):
                                    checkarray2[i] = True
                            for i in range(len(valueholder)):
                                if valueholder[i] == checkcheckhold:
                                    valueholder[i] = str(float(valueholder[i]) * 1.5)
                                    holding.append(float(valueholder[i]) * 1.5 - float(valueholder[i]))
                            dict.update({holdinghold: holding})
                    if check != True:
                        hol = []
                        dict.update({holdinghold: holdinghold})
                        counter = 0.0
                        for i in range(36):
                            if isValidMove(holdinghold, i, "X"):
                                counter += 1
                        for i in range(36):
                            if isValidMove(holdinghold, i, "X"):
                                hol.append(str(i))
                                hol.append(str(float(1/counter)))
                        dict.update({holdinghold: hol})

            else:
                while (len(hold) > 0):
                    opposite = len(hold)
                    holdinghold = hold.pop()
                    holdcounter -= 1
                    #print(holdcounter)
                    if holdcounter < 0:
                        checkhold = "--------------XO----OX--------------"
                    else:
                        checkhold = hold[holdcounter]
                        #print(checkhold)

                    placeholder = dict.items()
                    checkcheckhold = -1
                    check = False
                    holding = []
                    if checkhold in dict:
                        valueholder = dict[checkhold]
                        helpcount = 0
                        checkarray2 = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
                        for i in range(36):
                            if holdinghold[i] == "O" and checkhold[i] == "-":
                                checkcheckhold = i
                            if isValidMove(checkhold, i, "O"):
                                checkarray2[i] = True
                                helpcount += 1
                        for i in range(len(valueholder)):
                            holder = 0.0
                            if opposite < 0:
                                break
                                # print(holdcounter)
                                # print(numofmoves)
                            #print("close")
                            for k in range(36):
                                difference = 0.0
                                if k == checkcheckhold:
                                # print(valueholder[n])
                                # print(k)
                                    if str(valueholder[i]) == str(k) and i != checkcheckhold:
                                        #print("learned")
                                        holder = float(valueholder[i+1])
                                        holder = holder - holder - holder * (1.0 - (opposite * 0.05))
                                        if holder < 0.0:
                                            difference = holder
                                            holder = 0.0
                                        opposite += 1
                                        valueholder[i+1] = holder
                                        holding.append(k)
                                        holding.append(str(float(valueholder[i+1])))
                                # print(valueholder[n])
                                # print(k)
                                elif str(valueholder[i]) == str(k) and i != checkcheckhold:
                                    #print("learned2")
                                    #print(valueholder[n+1])
                                    holder = float(valueholder[i+1])
                                    holder = (difference * -1) + holder - holder * (1.0 - (opposite * 0.05))
                                    valueholder[i+1] = float(valueholder[i+1]) + holder/numofmoves
                                    #print(valueholder[i+1])
                                    holding.append(k)
                                    holding.append(valueholder[i+1])
                            #print(checkhold)
                        #print(holding)
                            dict.update({checkhold: holding})
                    else:
                        hol = []
                        dict.update({checkhold: checkhold})
                        counter = 0.0
                        for i in range(36):
                            if isValidMove(checkhold, i, "O"):
                                counter += 1
                        for i in range(36):
                            if isValidMove(checkhold, i, "O"):
                                hol.append(str(i))
                                hol.append(str(float(1/counter)))
                        dict.update({checkhold: hol})

        else: # status == 0
            # no winner
            p = 0
        holdcounter = 0
        
    def stopPlaying( self ):
        print("stop playing")
        if self.symbol == "O":
            with open("trainingO.txt", 'w') as file:
                for key, value in dict.items():
                    value_str = ",".join(str(x) for x in value)
                    file.write("{}, {}\n".format(key, value_str))
        if self.symbol == "X":
            with open("trainingX.txt", 'w+') as f:
                keys = dict.keys()
                vals = dict.values()
                st = ""
                for n in range(len(keys)):
                    st = st + (str(keys[n]))
                    for i in range(len(vals[n])):
                        st = st + "," + (str(vals[n][i]))
                    st = st + ("\n")
                f.write(st)
                f.close()
        return
