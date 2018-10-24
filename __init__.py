
SPACES = ['\f','\n','\r','\t','\v',' ']

def get_headers(filename, lines):
    '''
    Generates headers in format:
    line_index, header_level, header_text
    '''
    status=''
    z=[]
    coords=(0,0)
    x=0
    y=-1
    now,nowword,currtag='','',''
    while True:
        y+=1
        if y==len(lines[x]):
            if nowword!='':
                currtag+=nowword+' '
            nowword=''
            y=0
            x+=1
            if x==len(lines):
                break
            f=False
            while 0==len(lines[x]):
                x+=1
                if x==len(lines):
                    f=True
                    break
            if f:
                break
        now=lines[x][y]
        if now in SPACES:
            if nowword!='':
                currtag+=nowword+' '
            nowword=''
        else:
            nowword+=now
            
        if status=='<':
            if nowword=='!--' and currtag=='':
                status,nowword='<!--',''
            elif now=='>':
                currtag=currtag+nowword[:-1]
                z.append((currtag,coords))
                status,nowword='',''
            elif now in ["'",'"']:
                status=now
        elif status=='<!--':
            if nowword.endswith('-->'):
                status,nowword='',''
        elif status in ["'",'"'] and now==status:
            status='<'
        else:
            if now=='<':
                status,nowword,currtag,coords='<','','',x
    zz=[]
    stack=[0]
    z.reverse()
    for i in z:
        if i[0]=='':
            continue
        if i[0][0]=='/':
            stack.append(i[0][1:])
        else:
            if stack[-1]==i[0].split(maxsplit=1)[0]:
                stack.pop()
            zz.append((i[1],len(stack),i[0],0))
    zz.reverse()
    return zz

if __name__=="__main__":
    import os
    for file in os.listdir("tests"):
        if file.endswith(".xml") or file.endswith(".html"):
            print()
            print('test',file)
            ss=open(os.path.join("tests",file),encoding='utf-8').read().split('\n')
            for i in get_headers('',ss):
                print(i)
            break
