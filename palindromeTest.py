def makeValid(s):
    validString = ""
    for char in s:
        if char in 'abcdefghijklmnopqrstuvwxyz':
            validString += char
    return validString

def isPalindrome(s):
    if len(s) <= 1:
        return True
    return ((s[0] == s[-1]) and isPalindrome(s[1:-1])) #short circuit the test and stop the recursion if false

string = input("please enter a word: ")
string.lower
string = makeValid(string)
print(isPalindrome(string))

