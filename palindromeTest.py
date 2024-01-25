#checks if an inputed string is a palindrome or not ignoring all spaces, punctuation and non letter characters
    
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

string = input("please enter a string: ")
lstring = string.lower()
lstring = makeValid(lstring)
if isPalindrome(lstring):
    print(string, "is a palindrome.")
else:
    print(string, "is not a palindrome.")

print("finished")
