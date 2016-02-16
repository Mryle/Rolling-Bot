import random #dla losowania liczb
import re #regular expression, dla grupowania

#zwrocenie losowej liczby
def onedice(i):
   return random.randint(1,i)

#Wylosowanie kilku liczb
def manydice(k,i):
   linList = []
   for p in xrange(k):
      linList.append(dice(k))
   return linList

#
def dice(s):
    return sum(diceTerm(x) for x in s.split('+'))

#
def diceTerm(t):
    p = t.split('*')
    return diceFactor(p[0]) if len(p)==1 else diceFactor(p[0])*diceFactor(p[1])

#
def diceFactor(f):
    p = f.split('d')
    if len(p)==1:
        return int(f)
    return sum(random.randint(1, int(p[1]) if p[1] else 6) for \
               i in range(int(p[0]) if p[0] else 1))
#
def roll(name,r):
   return name + ' just rolled ' + str(dice(r))

def _initialize(exp):
   token_map = {'+':'ADD', '-':'ADD', '*':'MUL', '/':'MUL',
          '(':'LPAR', ')':'RPAR', 'd':'DICE'}
   #dividing into groups
   split_expr = re.findall('[\d.]+|[%s]' % ''.join(token_map), exp)
   #evaluating as tokens
   tokens = [(token_map.get(x, 'NUM'), x) for x in split_expr]
   #appending end tokens
   expr = tokens
   expr.append(('END',0))
   expr.append(('END',0))
   print("Parsed: ", expr)
   return expr

#funkcje zwracaja (wynik i iterator)
#number zbiera nastepna liczbe i stara sie sprawdzic priorytet
def _number(exp,val,i):
   while exp[i][0]=='LPAR' or exp[i][0]=='RPAR':
      val = 0
      i += 1
   if exp[i][0]<>'NUM': return (0,i)
   l1 = int(exp[i][1])
   i += 1
   return _prioritize(l1, exp, val, i)

#prioritize patrzac na val sprawdza czy nastepne dzialanie bedzie nastepne
#w kolejnosci, czy tez powinno sie zwijac
def _prioritize(l1, exp, val, i):
   #Dbanie o kolejnosc dzialan   
   #wykonuje sie dopoki nastepne dzialania maja nie nizszy priorytet niz aktualne
   while True:
      if exp[i][0] == 'END':
         return (l1,i)
      if exp[i][0] == 'RPAR':
         return (l1,i+1)
      if exp[i][0] == 'ADD' and val>=10:
         return (l1,i) 
      if exp[i][0] == 'MUL' and val>=20:
         return (l1,i)
      ret = _eval(l1,exp,i)
      l1 = ret[0]
      i = ret[1]
      
#eval wylicza pojedyncze wyrazenie
def _eval(l1,exp,i):
      
   #znalezienie operacji do wykonania
   e = exp[i] #znak dzialania
   val = 0
   if e[0]=='END': return (l1, i)
   if e[0]=='RPAR': return (l1,i+1)
   if e[0]=='ADD': val = 10
   if e[0]=='MUL': val = 20
   
   ret = _number(exp,val, i + 1)
   l2 = ret[0]
   
   l3 = _oper(l1,e[1],l2)
   
   print '%d%c%d=%d'%(l1,e[1],l2,l3)

   #zwrocenie jakos wyniku operacji w postaci tekstu
   return (l3,ret[1])   
   
#pojedyncza operacja
def _oper(v1,e,v2):
   if e == '+': return v1 + v2
   elif e == '-': return v1 - v2
   elif e == '*': return v1 * v2
   elif e == '/': return v1 / v2
   else: return 0

def _parse(exp):
   ret = _number(exp,0,0)
   l1 = ret[0]
   i = ret[1]
   while exp[i][0]<>'END':
      ret = _eval(l1,exp,i)
      l1 = ret[0]
      i = ret[1]
   return l1

def parse(exp):
   return _parse(_initialize(exp))


#(23+7)-8(5-4/2*8)
