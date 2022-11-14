import chess, chess.svg, chess.pgn
import subprocess
import io
import json
import re
import urllib.request
import bs4
import discord
import time
import difflib

client_id = '753855401895919626'
client_secret = 'NyxaSs86PQY1OCLi_7TpqM_htdn9CxSS'
token = 'NzUzODU1NDAxODk1OTE5NjI2.X1sQjQ.3ANIvrqzwINjZBSi3sBpKuI1F8I'
base_authorization_url = 'https://discord.com/api/oauth2/authorize'
token_url = 'https://discord.com/api/oauth2/token'
revocation_url = 'https://discord.com/api/oauth2/token/revoke'

inkscape_path = 'inkscape/bin/inkscape' #no .exe
eco_path = 'eco.json'
ffmepg_path = 'ffmpeg.exe'
random_puzzle_url = 'https://api.chess.com/pub/puzzle/random'
daily_puzzle_url = 'https://api.chess.com/pub/puzzle'
start_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

class Opening:

    def __init__(self, json):
        self.name = json['name']
        self.eco = json['eco']
        self.fen = json['fen']
        self.moves = json['moves']

    def __str__(self):
        return '%s: %s\n%s' % (
            self.eco, self.name, self.moves)

class Puzzle:

    CORRECT = 0
    INCORRECT = 1
    DIFFERENT_RESPONSE = 2
    UNSOLVED = 3
    UNSOLVED_VARIANT = 4

    def __init__(self, json):
        self.title = json['title']
        self.comments = '' if not 'comments' in json else json['comments']
        self.url = json['url']
        self.publish_time = json['publish_time']
        self.fen = json['fen']
        self.pgn = json['pgn']
        self.image = json['image']
        self.moves = self.pgn[self.pgn.index('1.'):-2]
        self.moves = self.moves.strip().split()
        i = 0
        while i < len(self.moves):
            if '.' in self.moves[i]:
                del self.moves[i]
                continue
            i += 1
        self.white_to_play = 'w' in self.fen

    def submit_moves(self, moves):
        moves = moves.strip().split()
        i = 0
        while i < len(moves):
            if '.' in moves[i]:
                del moves[i]
                continue
            try:
                int(moves[i])
                del moves[i]
                continue
            except ValueError:
                pass
            i += 1
        if moves == self.moves:
            return (Puzzle.CORRECT, None, None)
        i = 0
        delimiter = '[+#x!?]'
        while i < min(len(moves), len(self.moves)):
            if re.sub(delimiter, '', moves[i]) != re.sub(
                    delimiter, '', self.moves[i]):
                if i % 2 == 1:
                    return (Puzzle.DIFFERENT_RESPONSE, i + 1, self.moves[i])
                else:
                    return (Puzzle.INCORRECT, i + 1, moves[i])
            i += 1
        if i < len(self.moves):
            if i % 2 == 0 and self.white_to_play:
                return (Puzzle.UNSOLVED_VARIANT, None, None)
            else:
                return (Puzzle.UNSOLVED, i + 1, self.moves[i])
        return (Puzzle.CORRECT, None, None)

def render(board, dest = 'default.png'):
    svg = chess.svg.board(board)
    with open('default.svg', 'w+') as file:
        file.write(svg)
    #could add -w {width}
    s = '"%s" -o "%s" "%s"' % (
        inkscape_path, dest, 'default.svg')
    subprocess.call(s)
    return dest

class MyApp(discord.Client):

    def __init__(self):
        super().__init__()
        self.puzzle = None

    async def on_message(self, message):
        global last_message
        last_message = message
        if message.author == self.user:
            return
        if message.content.startswith('.pgn'):
            await self.do_pgn(message)
        elif message.content.startswith('.fen'):
            await self.do_fen(message)
        elif message.content.startswith('.opening'):
            await self.do_opening(message)
        elif message.content == '.puzzle':
            await self.do_puzzle(message)
        elif message.content == '.daily':
            await self.do_daily(message)
        elif message.content.startswith('.solve'):
            await self.do_solve(message)
        elif message.content.startswith('.game'):
            await self.do_game(message)
        elif message.content == '.answer':
            await message.channel.send('||' + ' '.join(self.puzzle.moves) + '||')
            self.puzzle = None
        elif message.content == '.help':
            await message.channel.send('''
commands:
.help - displays this message
.jargon - for when you don't know what SAN or FEN mean.
.pgn [moves] - displays a board from SAN.
.fen [fen] - displays a board from FEN.
.opening [name/eco] - displays the name, opening moves, and diagram from the name or ECO code.
.game [lichess_url] - displays a gif of the game.
.puzzle - random chess.com daily puzzle. Solve it with .solve
.daily - today's chess.com daily puzzle. Solve it with .solve
.solve [moves] - try to solve the current puzzle using SAN.
.answer - for when you give up on the puzzle.
'''.strip())
        elif message.content == '.jargon':
            await message.channel.send('''
jargon:
SAN - Standard Algebraic Notation. How you write chess moves. - https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
Practice the coordinates for SAN here: https://lichess.org/training/coordinate
FEN - Forsyth-Edwards Notation. How you notate the whole board. - https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
Elo - Your chess rating used by USCF. - https://en.wikipedia.org/wiki/Elo_rating_system
Glicko - A different rating system used by Lichess - https://en.wikipedia.org/wiki/Glicko_rating_system
USCF - United States Chess Federation - https://en.wikipedia.org/wiki/United_States_Chess_Federation
FIDE - Fédération Internationale des Échecs - https://en.wikipedia.org/wiki/FIDE
Rank - A row. They have numbers.
File - A column. They have letters.
En Passant / e.p. - the French phrase for "in passing" which is a rule some people don't know - https://lichess.org/learn#/15
Stalemate - the opponent has no legal moves and the game is a draw - https://lichess.org/learn#/16
'''.strip())

    async def on_ready(self):
        print('Logged in as:\n%s\n%s\n-----' % (
            self.user.name, self.user.id))

    async def do_pgn(self, message):
        cmd, pgn = message.content.split(maxsplit = 1)
        game = chess.pgn.read_game(io.StringIO(pgn))
        file_url = render(game.end().board())
        await message.channel.send(
            file = discord.File(file_url,
            filename = 'board.png'))

    async def do_fen(self, message):
        cmd, fen = message.content.split(maxsplit = 1)
        file_url = render(chess.Board(fen))
        await message.channel.send(
            file = discord.File(file_url,
            filename = 'board.png'))

    async def do_puzzle(self, message):
        if self.puzzle is not None:
            await message.channel.send('Solve the one I gave you first!')
            return
        try:
            response = urllib.request.urlopen(random_puzzle_url)
        except urllib.error.URLError as e:
            print(e)
            await message.channel.send(
                'There was an issue fetching the puzzle.')
            return
        self.puzzle = Puzzle(json.loads(response.read().decode()))
        s = 'chess.com random Daily Puzzle: %s\n%s to play.' % (
            self.puzzle.title, 'White' if 'w' in self.puzzle.fen else 'Black')
        await message.channel.send(s)
        await message.channel.send(self.puzzle.image)
        self.puzzle.time = time.time()

    async def do_daily(self, message):
        if self.puzzle is not None:
            await message.channel.send('Solve the one I gave you first!')
        try:
            response = urllib.request.urlopen(daily_puzzle_url)
        except urllib.error.URLError as e:
            print(e)
            await message.channel.send(
                'There was an issue fetching the puzzle.')
            return
        self.puzzle = Puzzle(json.loads(response.read().decode()))
        s = 'chess.com Daily Puzzle: %s\n%s to play.' % (
            self.puzzle.title, 'White' if 'w' in self.puzzle.fen else 'Black')
        await message.channel.send(s)
        await message.channel.send(self.puzzle.image)
        self.puzzle.time = time.time()

    async def do_solve(self, message):
        if self.puzzle is None:
            await message.channel.send('There is no puzzle in progress.')
            return
        cmd, moves = message.content.split(maxsplit = 1)
        response, ply, move = self.puzzle.submit_moves(moves)
        if response == Puzzle.CORRECT:
            await message.channel.send(
                'Correct! %s got it!\nTime: %0.2fs' % (
                message.author.mention, time.time() - self.puzzle.time))
            self.puzzle = None
        elif response == Puzzle.INCORRECT:
            await message.channel.send(
                '%s (ply %d) is incorrect.' % (move, ply))
        elif response == Puzzle.DIFFERENT_RESPONSE:
            await message.channel.send(
                "%s's move is %s on ply %d." % (
                'Black' if self.puzzle.white_to_play else 'White',
                move, ply))
        elif response == Puzzle.UNSOLVED:
            await message.channel.send(
                "%s's next move is %s. (ply %d)" % (
                'Black' if self.puzzle.white_to_play else 'White',
                move, ply))
        elif response == Puzzle.UNSOLVED_VARIANT:
            await message.channel.send("You're missing a move.")

    async def do_opening(self, message):
        cmd, opening = message.content.split(maxsplit = 1)
        if len(opening) == 3:
            for o in openings:
                if o.eco == opening:
                    file_url = render(chess.Board(o.fen))
                    await message.channel.send(str(o),
                        file = discord.File(file_url))
                    return
        elif len(opening) < 1000:
            similarity_max = 0
            max_opening = openings[0]
            delimiter = '[^a-zA-Z0-9 ]'
            opening_sub = re.sub(delimiter, '', opening).lower()
            for o in openings:
                o_sub = re.sub(delimiter, '', o.name).lower()
                similarity = difflib.SequenceMatcher(None, opening_sub, o_sub).ratio()
                if similarity > similarity_max:
                    similarity_max = similarity
                    max_opening = o
                if similarity == 1:
                    break
            o = max_opening
            file_url = render(chess.Board(o.fen))
            await message.channel.send(str(o),
                file = discord.File(file_url))

    async def do_game(self, message):
        cmd, url = message.content.split(maxsplit = 1)
        if url.startswith('https://lichess.org/'):
            #20 == len('https://lichess.org/')
            part = url[20:]
            if '#' in part:
                part = part[:part.index('#')]
            if part.endswith('/black'):
                white = False
                #6 == len('/black')
                part = part[:-6]
            else:
                white = True
            if len(part) == 12:
                part = part[:8]
            gif_url = 'https://lichess1.org/game/export/gif/'
            gif_url += ('' if white else 'black/') + part + '.gif'
            await message.channel.send(gif_url)
        elif url.startswith('https://www.chess.com'):
            pass
        else:
            pass

with open(eco_path) as eco_file:
    openings = [Opening(i) for i in json.load(eco_file)]

client = MyApp()
client.run(token)
