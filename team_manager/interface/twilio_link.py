#!/bin/env python3

import os
from datetime import datetime
import csv
import config

#os.environ[""]

def get_date():
    date = datetime.now()
    #print("date: ",date)
    return date

def get_user(number):
    # From the phone number, function will return user line with no,name,number,position
    player = "unfound"
    with open('player.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if number == row['number']:
                player_row = row
                return player_row
                break

    if player == "unfound":
        print("No player found, exiting")

    elif player != "unfound":
        print("Player found, %s." %(player_row['name']))

    print(player_row['name'])
    return player_row


def get_next_game():
    date = get_date()
    next_game = "unfound"
    with open('games.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            row_date = datetime.strptime(row['date'],'%Y-%m-%d')
            if row_date > date:
                next_game = row

                return next_game
                break

        if next_game == "unfound":
            print("No next game found, exiting")

        elif next_game != "unfound":
            print("Game found, next one on: %s" %(next_game)) 

        print(next_game)
    return next_game


def get_raw_msg():
    return user_number, raw_msg


def get_function(raw_msg):
    if raw_msg == 'abscent':
        function = "abscent"

    elif raw_msg == 'present':
        function = 'present'
    else:
        function = 'unknown'

    return function

def analyse_function(function):
    date = get_date()
    next_game = get_next_game()
    msg = ""
    if function == 'unknown':
        msg = "Commande non comprise, utiliser present ou abscent pour indiquer votre presende a la prochaine partie."

    elif function == 'abscent' or 'present':
        msg = "Merci, je vous met %s pour la prochaine partie du %s, a l'arena: %s" % (function, next_game['date'], next_game['arena'])
    # print(msg)
    return msg

def send_msg(msg,):
    return


def get_number():
    return


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


def pushover(msg, user):
    # Your Account Sid and Auth Token from twilio.com/console

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]

   
    numbers = config.NUMBERS
    client = Client(account_sid, auth_token)


    for number in numbers:
        message = client.api.account.messages.create(
                            body=msg,
                            from_=config.FROM_NUMBER,
                            to=number)
        print(message.sid)
        sleep(2)

if __name__ == "__main__":
    msg = analyse_function('abscent')
    print(msg)
