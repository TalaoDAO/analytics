a="5%"
b="5"
c=5
def transformer(num):
    if(type(num)==int):
        return num
    if(num[len(num)-1]=="%"):
        disc=""
        i=0
        while(num[i]!="%"):
            disc=disc+num[i]
            i+=1
            if(i==len(num)-1):
                break
        return int(disc)
    return int(num)
print(type(transformer(a)))
print(type(transformer(b)))
print(type(transformer(c)))