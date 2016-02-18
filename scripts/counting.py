import random #dla losowania liczb
import re #regular expression, dla grupowania

#zwrocenie losowej liczby
def onedice(i):
   return random.randint(1,i)

#Wylosowanie kilku liczb
def manydice(k,i):
   linList = []
   for p in xrange(k):
      linList.append(onedice(i))
   return linList

def dice(l1,l2):
   lis = manydice(l1,l2)
   sm=0
   for k in lis:
      sm += k
   return sm

class parser:
   output = ''
   
   def __init__(self):
      output = ''
   
   def _initialize(self,exp):
      token_map = {'+':'ADD', '-':'ADD', '*':'MUL', 'x':'MUL', '/':'MUL',
             '(':'LPAR', ')':'RPAR', 'd':'DICE'}
      #dividing into groups
      split_expr = re.findall('[\d.]+|[%s]' % ''.join(token_map), exp)
      #evaluating as tokens
      tokens = [(token_map.get(x, 'NUM'), x) for x in split_expr]
      #appending end tokens
      expr = tokens
      expr.append(('END',0))
      expr.append(('END',0))
      #print("Parsed: ", expr)
      return expr

   #funkcje zwracaja (wynik i iterator)
   #number zbiera nastepna liczbe i stara sie sprawdzic priorytet
   def _number(self,exp,val,i):
      #na wypadek nawiasu
      if exp[i][0]=='LPAR':
         ret = self._parent(exp,i+1)
         l1 = ret[0]
         i = ret[1]
      #znaleziono liczbe
      elif exp[i][0]=='NUM':
         l1 = int(exp[i][1])
         i += 1
      #cos innego (blad?)
      else: return (0,i)

      return self._prioritize(l1, exp, val, i)
   
   #funkcja sluzy obsluzeniu pojedynczego nawiasu   
   def _parent(self,exp,i):
      ret = self._number(exp,0,i)
      l1 = ret[0]
      i = ret[1]
      while exp[i][0]<>'END' and exp[i][0]<>'RPAR':
         ret = self._eval(l1,exp,i)
         l1 = ret[0]
         i = ret[1]
      if exp[i][0]=='RPAR': i+=1

      return (l1,i)

   #prioritize patrzac na val sprawdza czy nastepne dzialanie bedzie nastepne
   #w kolejnosci, czy tez powinno sie zwijac
   def _prioritize(self,l1, exp, val, i):
      #Dbanie o kolejnosc dzialan   
      #wykonuje sie dopoki nastepne dzialania maja nie nizszy priorytet niz aktualne
      while True:
         if exp[i][0] == 'END':
            return (l1,i)
         if exp[i][0] == 'RPAR':
            return (l1,i)
         if exp[i][0] == 'ADD' and val>=10:
            return (l1,i) 
         if exp[i][0] == 'MUL' and val>=20:
            return (l1,i)
         #if exp[i][0] == 'DICE' and val>=30:
         #   return (l1,i)
         ret = self._eval(l1,exp,i)
         l1 = ret[0]
         i = ret[1]
         
   #eval wylicza pojedyncze wyrazenie
   def _eval(self,l1,exp,i):
         
      #znalezienie operacji do wykonania
      e = exp[i] #znak dzialania
      val = 0
      if e[0]=='END': return (l1, i)
      if e[0]=='RPAR': return (l1, i)
      if e[0]=='ADD': val = 10
      if e[0]=='MUL': val = 20
      if e[0]=='DICE': val = 30
      
      ret = self._number(exp,val, i + 1)
      l2 = ret[0]
      
      l3 = self._oper(l1,e[1],l2)
      
      #print '%d%c%d=%d'%(l1,e[1],l2,l3)
      self.output+='%d%c%d=%d'%(l1,e[1],l2,l3) + '\n'

      #zwrocenie jakos wyniku operacji w postaci tekstu
      return (l3,ret[1])   
      
   #pojedyncza operacja
   def _oper(self,v1,e,v2):
      if e == '+': return v1 + v2
      elif e == '-': return v1 - v2
      elif e == '*': return v1 * v2
      elif e == 'x': return v1 * v2
      elif e == '/': return v1 / v2
      elif e == 'd': return dice(v1,v2)
      else: return 0

   def _parse(self,exp):
      ret = self._parent(exp,0)
      return ret[0]

   def parse(self,exp):
      return self._parse(self._initialize(exp))
   
   def dparse(self,exp):
      ret = self._parse(self._initialize(exp))
      print(self.output)
      self.output=''
      return ret

#(23+7)-8(5-4/2*8)
#/eval (4d(5/3)+2d5/8d11)*5
# 3d(5/5)+5
#nie dzialaja wyrazenia nawiasowe


