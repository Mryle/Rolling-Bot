import discord
import asyncio
import random
from scripts import counting as ct

#wyliczenie wartosci w notacji kostkowej
#TODO: Dodac funkcjonalnosci
def dice(s):
    return sum(diceTerm(x) for x in s.split('+'))

def diceTerm(t):
    p = t.split('*')
    return diceFactor(p[0]) if len(p)==1 else diceFactor(p[0])*diceFactor(p[1])

def diceFactor(f):
    p = f.split('d')
    if len(p)==1:
        return int(f)
    return sum(random.randint(1, int(p[1]) if p[1] else 6) for \
               i in range(int(p[0]) if p[0] else 1))

def roll(name,r):
   return name + ' just rolled ' + str(dice(r))

def isAllowed(channel):
   return restrictedChannel == channel if restrict else True

#Procedura logowania
mail = input('Enter e-mail adress: ')
passwd = input('Enter password: ')

restrict = False
restrictedChannel = ''

client = discord.Client()
pars = ct.parser()

@client.event
@asyncio.coroutine
def on_message(message):
    #if message.author.id != client.user.id:
    #    client.send_message(message.channel, message.content)
    print(message.author.name + ': ' + message.content)
    for attach in message.attachments:
       print("Attachments:" + str(attach['url']))
    if message.author.id != client.user.id:
        s = message.content.split(' ')
        if s[0]=='/restrict':
            restrict = True
            restrictedChannel = message.channel
        if s[0]=='/unrestrict':
            restrict = False
        if isAllowed(message.channel):
            if s[0]=='/roll' and len(s)==2:
                client.send_message(message.channel, roll(message.author.name,s[1]))
            if s[0]=='/eval' and len(s)==2:
                result = pars.parse(s[1])
                client.send_message(message.channel, pars.output)
                pars.output = ''  
            if s[0]=='/card' and len(s)==1:
                client.send_message(message.channel,"http://www.myth-weavers.com/sheet.html#id=694115 - Radi ' Gui-don Elf")  
                client.send_message(message.channel,"http://www.myth-weavers.com/sheet.html#id=711046 - Sowa ' Taedhwen Changeling") 
                client.send_message(message.channel,"http://www.myth-weavers.com/sheet.html#id=720569 - Rodez ' Rognar Ork") 


@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
client.run(mail, passwd)
