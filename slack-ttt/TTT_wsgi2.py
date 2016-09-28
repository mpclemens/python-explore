#!/usr/bin/env python2
"""App caller for TTT module, for Slack integration"""

import cgi
import json
import httplib
import urllib

from flask import Response

from TTT2  import TTT, NotYourTurnError, InvalidLocationError, InvalidUserError
from User2 import User
from Channel2 import Channel

###

class Slack_TTT():

    # To talk with Slack
    #
    APP_TOKEN  = ''
    AUTH_TOKEN = ''

    def __init__(self,request):
        self.form = request.form
        self.token = self.form.get("token", default=None)
        self.command = self.form.get("text", default=None)

        self.channel = Channel(self.form.get("team_id"),
                               self.form.get("channel_id"))

        self.user = User(user_id = request.form.get("user_id"),
                         user_name = request.form.get("user_name"))

        self.users = None  # filled in later by init_users()
        self.output = {}

    #

    def dispatch(self):
        """Process the received /ttt subcommand and arguments"""

        if self.token not in (Slack_TTT.APP_TOKEN, Slack_TTT.AUTH_TOKEN):
            raise httplib.HTTPException, httplib.UNAUTHORIZED

        if self.command is None:
            command = ""
            args = []
        elif len(self.command):
            parts = self.command.split()
            command, args = parts[0].lower(), parts[1:]

        if command in ("","help","?"):
            self.show_help()
        elif command in ("play","show"):
            self.show_board()
        elif command[0] == "@":
            # Pass the stripped username for lookup and matching (no @)
            self.challenge_user(command[1:])
        elif command.isdigit() and int(command) in range(1,10):
            self.make_move(int(command))
        elif command == "quit":
            self.quit_game()
        elif 0 and command == "debug": # remove "0 and" during development
            self.debug()
        else:
            self.output["text"] = "Sorry, I didn't understand that :turkey:\nTry: /ttt help"

        return Response(json.dumps(self.output),
                        mimetype='application/json')

    ### COMMAND HANDLERS

    #
    def show_help(self):
        """Output how-to information about the command"""
        self.output["text"] = """Tic-Tac-Toe for two players"""
        self.output["attachments"] = []
        self.output["attachments"].append({});
        attach = self.output["attachments"][0]

        attach["text"] = """
/ttt [command]

help : this message
show : show the game in the current channel
@someone : start a new game with @someone
1-9  : place an X or O during your turn
quit : drop out of any game you're in
"""

    #
    def show_board(self):
        """Display the current channel's game board, if any"""

        ttt = TTT(self.channel, None, None)
        ttt.load()

        self.output["attachments"] = []
        self.output["attachments"].append({})
        attach = self.output["attachments"][0]

        if ttt and not ttt.game_over and ttt.next_turn:
            self.output["text"] = "The game so far:\n"

            if self.user == ttt.next_turn:
                the_board = "```{}```\nIt's your turn\nTry: /ttt [1-9] to play".format(ttt.get_board(show_labels=True))
                attach["text"] = '@{} is playing "X"\n@{} is playing "O"'.format(ttt.player_X.name, ttt.player_O.name)
            else:
                the_board = "```{}```\nWaiting on @{} to move".format(ttt.get_board(), ttt.next_turn.name)
                attach["text"] = '@{} is playing "X"\n@{} is playing "O"'.format(ttt.player_X.name, ttt.player_O.name)
            self.output["text"] += the_board

        else:
            self.output["text"] = "There's no active game in this channel"
            attach["text"] = "To play a game, try:\n/ttt @someone"

    #
    def challenge_user(self, username):
        """Start a new game in the current channel, if none is running"""

        ttt = TTT(self.channel, None, None)
        ttt.load()

        self.output["attachments"] = []
        self.output["attachments"].append({})
        attach = self.output["attachments"][0]

        if ttt.next_turn and not ttt.game_over:
            self.output["text"] = "There's an active game in this channel, sorry"
            attach["text"] = "To watch, try:\n/ttt show"
        else:
            # Look up the challenged user id, given their @-name
            self.init_users()

            opponent = None

            if len(self.users):
                opponent = filter(lambda u: u.name == username, self.users)
                if len(opponent):
                    opponent = opponent[0] # because filter() returns a list

                    if opponent == self.user:
                        self.output["text"] = "Sorry, this is a two-player game\nTry: /ttt @someone"
                    else:
                        # start a game
                        ttt = TTT(channel = self.channel,
                                  player_X = self.user,
                                  player_O = opponent)
                        ttt.save()
                        self.output["text"] = "Started a game with @{}\n```{}```".format(username, ttt.get_board(show_labels=True))
                        attach["text"] = """
Type /ttt [1-9] to play
You are playing "X"
@{} is playing "O" """.format(username)
            else:
                self.output["text"] = "Sorry, I can't find @"+username

    #
    def make_move(self,location):
        """Allow the next player (only!) to take a turn"""

        ttt = TTT(self.channel, None, None)
        ttt.load()

        self.output["attachments"] = []
        self.output["attachments"].append({})
        attach = self.output["attachments"][0]

        try:
            ttt.play_at(self.user, location)
            ttt.save()
        except InvalidUserError:
            self.output["text"] = "Sorry, @{} and @{} are playing right now".format(ttt.player_X.name, ttt.player_O.name)
            attach["text"] = "I'm wating on @{} to take a turn\nWatch their game: /ttt show".format(ttt.next_turn.name)
        except NotYourTurnError:
            self.output["text"] = "It's not your turn, you need to wait on @{} to play".format(ttt.next_turn.name)
        except InvalidLocationError:
            self.output["text"] = "That space is taken, try another\n```{}```".format(ttt.get_board(show_labels=True))
            attach["text"] = "To make a move, type:\n/ttt [1-9]"
        else:
            self.output["response_type"] = "in_channel"
            if ttt.game_over:
                if ttt.winner:
                    self.output["text"] = "Congratulations @{}, you won! :clap:\n```{}```".format(ttt.winner.name, ttt.get_board())
                else:
                    self.output["text"] = "Sorry, the game ended in a tie :turkey:\n```{}```".format(ttt.get_board())
                    attach["text"] = "Go for a rematch! Try:\n/ttt @someone"
            else:
                self.output["text"] = "@{} just made a move\n```{}```".format(self.user.name, ttt.get_board())
                attach["text"] = "Now it's @{}'s turn".format(ttt.next_turn.name)

    #
    def quit_game(self):
        """If the current user is one of the players, stop the game in progress"""

        ttt = TTT(self.channel, None, None)
        ttt.load()

        self.output["attachments"] = []
        self.output["attachments"].append({})
        attach = self.output["attachments"][0]

        if not ttt.game_over:
            if self.user in (ttt.player_X, ttt.player_O):
                self.output["response_type"] = "in_channel"
                self.output["text"] = "@{} is a quitter!".format(self.user.name)
                ttt.game_over = True
                ttt.winner    = None
                ttt.save()
                self.output["text"] += "```{}```\nGAME OVER".format(ttt.get_board())
                attach["text"] = "Try: /ttt @someone for a new game"
            else:
                self.output["text"] = "Only @{} or @{} can quit the current game".format(ttt.player_X.name, ttt.player_O.name)
        else:
            self.output["text"] = "There's no active game in this channel to quit"
            attach["text"] = "To play a game, try:\n/ttt @someone"

    #
    def debug(self):

        ttt = TTT(self.channel, None, None)

        try:
            ttt.load()
            loaded = True
        except:
            loaded = False

        self.output["text"] = """
DEBUG
team/chan {}/{}
loaded? {}
```{}```""".format(self.channel.team_id, self.channel.channel_id,
                   loaded,
                   ttt.get_board())

        self.output["attachments"] = []
        self.output["attachments"].append({})
        attach = self.output["attachments"][0]

        if loaded:
            attachment = """

U: {}.{}

X: {}.{}
O: {}.{}

Over? {}""".format(self.user.id, self.user.name,
                   ttt.player_X.id, ttt.player_X.name,
                   ttt.player_O.id, ttt.player_O.name,
                   ttt.game_over)

            if ttt.next_turn:
                attachment += """
N: {}.{}
N == U? {}
N != U? {}""".format(ttt.next_turn.id, ttt.next_turn.name,
                     ttt.next_turn == self.user,
                     ttt.next_turn != self.user)


            attach["text"] = attachment

    ### HELPERS

    def init_users(self):
        query = urllib.urlencode({ "token" : Slack_TTT.AUTH_TOKEN })
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        connect = httplib.HTTPSConnection("slack.com")
        connect.request("POST","/api/users.list",query,headers)
        response = connect.getresponse()
        raw_users = json.loads(response.read())

        self.users = []

        if raw_users["ok"]:
            for member in raw_users["members"]:
                self.users.append(User(user_id = member["id"], user_name = member["name"]))

###

if __name__ == '__main__':
    handler = Slack_TTT()
    handler.dispatch()
