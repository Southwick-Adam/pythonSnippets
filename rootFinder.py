num = float(input("please enter a number: "))
exact = int(input("how many decimals of precision do you want?: "))

if num < 0:
    print("Error: must be positive.")
    exit()

calcs = 0 #just to see how efficient teh program is running
stepMagnitude = 0
step = 1

#we can make it scale much more efficiently by testing the magnitude of the first step
#before running the for loop
while step ** 2 < num:
    stepMagnitude += 1
    calcs += 1
    step = 10 ** stepMagnitude

step /= 10
i = 0
for k in range(0,exact + stepMagnitude + 1):
    while i ** 2 < num:
        i += step
        calcs += 1
    if i ** 2 == num:
        print(num,"is exactly",i,"squared")
        print(calcs)
        sys.exit()
    if k == exact + stepMagnitude:
        print("the square root of",num,"is approx", round(i,exact))
        print(calcs)
        sys.exit()
    #if were looping, take i back a step and reduce the step size 
    i -= step
    step /= 10
    