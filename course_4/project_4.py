VOWEL_COST = 250
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS = 'AEIOU'


# Write the WOFPlayer class definition (part A) here
class WOFPlayer:
    def __init__(self, name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []

    def __str__(self):
        return "{0} (${1})".format(self.name, self.prizeMoney)

    def addMoney(self, amt):
        self.prizeMoney += amt

    def addPrize(self, prize):
        self.prizes.append(prize)

    def goBankrupt(self):
        self.prizeMoney = 0


# Write the WOFHumanPlayer class definition (part B) here
class WOFHumanPlayer(WOFPlayer):
    def __init__(self, name):
        WOFPlayer.__init__(self, name)

    def getMove(self, category, obscuredPhrase, guessed):
        print("{0} has ${1}".format(self.name, self.prizeMoney))
        print("")
        print("Category: {0}".format(category))
        print("Phrase: {0}".format(obscuredPhrase))
        print("Guessed: {0}".format(guessed))
        print("")
        print("Guess a letter, phrase, or type 'exit' or 'pass':")
        return input()


# Write the WOFComputerPlayer class definition (part C) here
class WOFComputerPlayer(WOFPlayer):
    SORTED_FREQUENCIES = "ZQXJKVBPYGFWMUCLDRHSNIOATE"

    def __init__(self, name, difficulty):
        WOFPlayer.__init__(self, name)
        self.difficulty = difficulty

    def smartCoinFlip(self):
        return random.randint(1, 10) > self.difficulty

    def getPossibleLetters(self, guessed):
        possible = LETTERS[:]
        for guess in guessed:
            possible.replace(guess, "")
        if self.prizeMoney < VOWEL_COST:
            for vowel in VOWELS:
                possible.replace(vowel, "")
        return possible

    def getMove(self, category, obscuredPhrase, guessed):
        possible = getPossibleLetters(guessed)
        if not possible:
            return "pass"
        move = None
        if self.smartCoinFlip():
            # make good move
            for guess in SORTED_FREQUENCIES:
                if guess in possible:
                    move = guess
        else:
            # make bad move
            move = random.choice(possible)
        return move

mcp = WOFComputerPlayer("Master Compute Program", 3)
possible = mcp.getPossibleLetters("BILKO")
print(possible)
