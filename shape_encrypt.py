def plus(x,i,j):
    x[i]=(x[i]+x[j])&4294967295

def rrot(x,i,j,k):
    x[i]=((x[j]^x[i])<<k&4294967295)|((x[i]^x[j])>>(32-k))

def encrypt(key,inp,iv1,iv2, s1, s2):
    k=[[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15],[0,5,10,15],[1,6,11,12],[2,7,8,13],[3,4,9,14]]
    l=[16,12,8,7]
    y=s1+key+[0,0,iv1,iv2]
    v1=s2
    out=[]
    inpl=len(inp)
    while len(out)<inpl:
        y[12]=v1&4294967295
        y[13]=int(v1/4294967296)
        x=y[::]
        for i in range(0,8):
            for p in k:
                for i in range(0,4):
                    plus(x,p[2*i%4],p[2*i%4+1])
                    rrot(x,p[(2*i+3)%4],p[2*i%4],l[i%4])
        for i in range(0,16):
            x[i]=(x[i]+y[i])&4294967295
        z=[]
        for p in x:
            z.append(p&255)
            z.append((p>>8)&255)
            z.append((p>>16)&255)
            z.append((p>>24)&255)
        while len(out)<inpl and len(z)>0:
            out.append(inp[len(out)]^z.pop(0))
        v1=(v1+1)%9007199254740992
    return out
