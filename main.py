# python irc bot
# based on a tutorial from: https://linuxacademy.com/blog/linux-academy/creating-an-irc-bot-with-python3/

import socket
import time
# my files
import getweather
import getdate
import getfortune
import getskdtheme
import random
from getcovid import getCovidData

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net"
channel = "#bot-testing"
# channel = '#sketchdaily'
botnick = "tinjbot"  # The bot's nickname
adminname = "ThereIsNoJustice"  # My IRC nickname - change this to your username
exitcode = "bye " + botnick


def joinchannel(chan):
    ircsock.send(bytes("JOIN " + chan + "\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if (ircmsg.strip() != ""):
            print(ircmsg)
    print(" > > > Channel successfully joined")


def ping():  # respond to server Pings
    ircsock.send(bytes("PONG :pingisn", "UTF-8"))


def sendmsg(msg, target=channel):  # sends messages to the target
    ircsock.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))


def main():
    getfortune.loadfortunes()

    print(" > > > Beginning IRC bot")
    # connect to the server using the port 6667 (the standard IRC port)
    ircsock.connect((server, 6667))
    ircsock.send(bytes("USER " + botnick + " " + botnick +
                       " " + botnick + " " + botnick + "\n", "UTF-8"))
    # assign the nick to the bot
    ircsock.send(bytes("NICK " + botnick + "\n", "UTF-8"))
    print(" > > > Server joined")

    joinchannel(channel)
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if (ircmsg.strip() != ""):
            print(ircmsg)

        # TODO: Use eval('text') to run code as a file that can be stopped without having to rejoin the IRC server

        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!', 1)[0][1:]
            message = ircmsg.split('PRIVMSG', 1)[1].split(':', 1)[1].lower()
            if len(name) < 17:

                # respond to 'hi <botname>'
                if message.find('hi ' + botnick.lower()) != -1 or message.find('hello ' + botnick.lower()) != -1 or message.find('hey ' + botnick.lower()) != -1:
                    sendmsg("Hello " + name + "!")
                elif name.lower() == adminname.lower() and message.rstrip() == exitcode:  # quit with <exitcode>
                    sendmsg("oh...okay. :-/")
                    ircsock.send(bytes("QUIT\n", "UTF-8"))
                    return
                elif message.find(botnick.lower()) != -1:
                    sendmsg("╚═།-◑-▃-◑-།═╝ beep boop")

                # use '.tell' to send someone a message
                if message.find('.tell') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in the format of ‘.tell [target] [message]’ to work properly."
                    sendmsg(message, target)

                # TODO: Make a table of 'name's (usernames) and additional corresponding info?

                if message.find('.date') != -1:
                    print("printing date")
                    sendmsg(getdate.printdaynumber())

                if message.find(".dodongo") != -1:
                    sendmsg("!lol dodongo")

                if message.find(".choose") != -1:
                    msgArrSplit = message.split(' ')
                    if len(msgArrSplit) == 2:
                        msgArrSplit.pop(0)
                        yesNos = ["yeah do it", "well maybe",
                                  "no i don't think so", "it's probably fine"]
                        sendmsg(random.choice(yesNos))
                    elif len(msgArrSplit) > 2:
                        msgArrSplit.pop(0)
                        chosen = random.choice(msgArrSplit)
                        preMsg = random.choice(
                            ["i like this one", "sounds cool", "the best", "be a good human", "embrace obedience to your robot masters"])
                        sendmsg(f"{preMsg}: {chosen}")
                    else:
                        sendmsg("you need to give me choices!!")

                if message.find(".fortune") != -1:
                    print("printing fortune")
                    sendmsg(getfortune.printrandomfortune())

                if message.find('.getskdtheme') != -1:
                    print('printing skd theme')
                    sendmsg(getskdtheme.printskdtheme())

                if message.find('.hotdog') != -1:
                    print('printing a hotdog')
                    sendmsg('( ´∀｀)つ―⊂ZZZ⊃')

                if message.find('.covid') != -1:
                    splitMsg = message.split(' ')
                    if len(splitMsg) > 1:
                        try:
                            zipcode = int(splitMsg[1])
                            reqDict = {"type": "zip", "code": zipcode}
                            sendmsg(getCovidData(reqDict))
                        except:
                            try:
                                countrycode = splitMsg[1].upper()
                                reqDict = {"type": "countrycode",
                                           "code": countrycode}
                                sendmsg(getCovidData(reqDict))
                            except:
                                sendmsg('Something went wrong')
                    else:
                        sendmsg('.covid <zipcode/countrycode>')

                if message.find(".weather") != -1:  # TODO - .weather <place>
                    print("printing weather")
                    splitmsg = message.split(' ')
                    lat = 0
                    lon = 0
                    if len(splitmsg) == 3:
                        try:
                            lat = int(splitmsg[1])
                            lon = int(splitmsg[2])
                            sendmsg(getweather.printweather(lat, lon))
                        except ValueError:
                            sendmsg("I couldn't do that!")
                    else:
                        sendmsg('.weather <latitude> <longitude>')
                # list of commands
                if message.find('.help') != -1:
                    sendmsg("COMMANDS: Hi .date .fortune .getskdtheme .weather")

        else:
            if ircmsg.find("PING :") != -1:
                ping()


main()
