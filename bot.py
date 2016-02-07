import discord
import random

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

#Procedura logowania
mail = raw_input('Enter e-mail adress: ')
passwd = raw_input('Enter password: ')

restrict = False
restrictedChannel = ''

def isAllowed(channel):
   return restrictedChannel == channel if restrict else true

client = discord.Client()
client.login(mail, passwd)


@client.event
def on_message(message):
    #if message.author.id != client.user.id:
    #    client.send_message(message.channel, message.content)
    print(message.author.name + ': ' + message.content)
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

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()
