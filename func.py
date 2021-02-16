def function(**kwargs): 
    for args in kwargs:
        print(args)


args = {
    "name": "test", 
    "require": True, 
    "helps": "it's okay"
}


function(**args)

def multiply(*args): 
    total = 1 
    for arg in args: 
        total *= arg
    
    return total



tups = (7,8,9,10)
print(multiply(*tups))
print(multiply(1,2,3,4))
