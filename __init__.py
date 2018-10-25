
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
                if currtag.startswith('script'):
                    status='</script>'
                elif currtag.startswith('style'):
                    status='</style>'
                else:
                    status=''
                z.append((currtag,coords))
                nowword=''
            elif now in ["'",'"']:
                status=now
        elif status=='<!--':
            if nowword.endswith('-->'):
                status,nowword='',''
        elif status in ["'",'"'] and now==status:
            status='<'
        if status in['</script>','</style>']and now=='<':
            if lines[x][y:].startswith(status):
                status=''
        else:
            if now=='<':
                status,nowword,coords='<','',x
                if y+1!=len(lines[x])and lines[x][y+1]in SPACES:
                    currtag=' '
                else:
                    currtag=''
    zz=[]
    stack=[0]
    z.reverse()
    for i in z:
        if i[0]=='':
            continue
        if i[0][-1]=='/':
            zz.append((i[1],len(stack),i[0][:-1],0))   
            continue         
        if i[0][0]=='/':
            stack.append(i[0][1:])
        else:
            if i[0][0] ==' ':
                continue
            temp=i[0].split(maxsplit=1)[0]
            if stack[-1]==temp:
                stack.pop()
            if not(temp.lower()in['?php','?xml','!doctype']):
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
