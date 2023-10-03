num = float(input("please enter a number: "))
exact = int(input("how many decimals of precision do you want?: "))

def shorten(num):
    return round(num,exact)

if num < 0:
    print("Error: must be positive.")
    exit()
i = 0
step = 1
for k in range(0,exact + 1):
    while i ** 2 < num:
        i += step
    if i ** 2 == num:
        print(num,"is exactly",i,"squared")
        exit()
    if k == exact:
        print("the square root of",num,"is between",shorten(i-step),"and",shorten(i))
        exit()
    #if were looping, take i back a step and reduce the step size 
    i -= step
    step /= 10


    