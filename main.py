try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
import user303_wN73qcEAPZ_8 as game1
import user303_114OrRVHvi_32 as game2

game1.screen = 1  # the current screen is 1 to start with
currentFrame = 1  # so if the frame
soundBoolean = True  # used to play music

music = simplegui.load_sound('https://bastois.tk/music.ogg')  # music
musicTimer = 0  # timer for music loop
music.play()  # plays the music
pause = False


class Game:  # this class is used to swap between frames for the 2 different games
    def __init__(self):
        self.frame = None  # the frame is initially None

    def welcomeScreen(self):  # this method creates the frame for the welcome screen, game1 and the end screen for game1
        if self.frame != None:
            self.frame.stop()
        self.frame = simplegui.create_frame("Welcome and game1", game1.WIDTH, game1.HEIGHT)

    def game2(self):  # this method creates the frame for game2 and the end screen for game2
        if self.frame != None:
            self.frame.stop()
        self.frame = simplegui.create_frame("Game2", game2.WIDTH, game2.HEIGHT)

    def run(self):
        self.frame.set_draw_handler(draw)  # sets draw
        self.frame.set_keydown_handler(keyDownSelector())  # sets keyboard
        self.frame.set_keyup_handler(keyUpSelector())

        if game1.screen == 1:  # chooses click method depending on which screen is being used
            self.frame.set_mouseclick_handler(game1.click)
        if game1.screen == 2:
            self.frame.set_mouseclick_handler(game2.click)

        self.frame.add_button('Quit', stop_all)  # add the quit button
        self.frame.add_label('')
        self.frame.add_button('Sound On/Off', switch_sounds)  # add the sound button
        self.frame.add_label('')
        player1KeyInfo = self.frame.add_label('Player 1 Keys:')  # add controls
        player1KeyInfo1 = self.frame.add_label('Up arrow: move up')
        player1KeyInfo2 = self.frame.add_label('Down arrow: move down')
        player1KeyInfo3 = self.frame.add_label('Left arrow: move left')
        player1KeyInfo4 = self.frame.add_label('Right arrow: move right')

        if game1.screen == 1:  # this label is only needed if its game 1 since you cant shoot in game 2
            player1KeyInfo5 = self.frame.add_label('Space arrow: shoot')

        blank2 = self.frame.add_label('')
        player2KeyInfo = self.frame.add_label('Player 2 Keys:')
        player2KeyInfo1 = self.frame.add_label('W button: move up')
        player2KeyInfo2 = self.frame.add_label('S button: move down')
        player2KeyInfo3 = self.frame.add_label('A button: move left')
        player2KeyInfo4 = self.frame.add_label('F button: move right')

        if game1.screen == 1:  # this label is only needed in game1 since you cant shoot in game2
            player2KeyInfo5 = self.frame.add_label('Q button: shoot')

        self.frame.start()  # start the current frame


game = Game()  # game object


def keyUpSelector():  # method to choose keyUp handler depending on the current game
    if game1.screen == 1:
        return game1.kbd.keyUp
    if game1.screen == 2:
        return game2.kbd.keyUp


def keyDownSelector():  # method to chose keyDown handler depending on the current game
    if currentFrame == 1:
        return game1.kbd.keyDown
    if currentFrame == 2:
        return game2.kbd.keyDown


def drawOne(canvas):  # draw method for game1
    global currentFrame

    if currentFrame == 2:  # if the current frame is that of game2
        currentFrame = 1  # current frame must now be 1
        game.welcomeScreen()  # make the game frame equal to the frame for game 1
        game.run()  # start the frame

    game1.selector(canvas)  # draw method for game1, welcome screen and game 1 end screen


def drawTwo(canvas):  # draw method for game 2
    global currentFrame

    if currentFrame == 1:  # if the current frame is that of game1
        currentFrame = 2  # current frame must now be 2
        game.game2()  # make the game frame equal to the frame for game2
        game.run()  # start the frame

    game2.drawGame2(canvas)  # draw method for game 2 and game 2 endscreen


def draw(canvas):  # draw method to be passed into the draw handler of the the frame in the game object
    global musicTimer, soundBoolean
    if soundBoolean:
        music.play()

    musicTimer = musicTimer + 1
    if musicTimer == 10080:  # if the music has been playing for 2:48
        music.rewind()  # rewinds music
        musicTimer = 0  # sets timer back to 0

    if game1.screen == 2:  # if were in game2
        if not game2.playing:  # and if it is not being played
            game2.endFrame = False  # endFrame is reset
            game1.screen = 1  # the screen is 1 so it starts the frame for game 1
            game1.currentState = 'welcome'  # makes the selector(draw) in game1 draw the welcome screen
            game1.desiredScreen = 1  # the screen needed is 1 as well
            game2.playing = True  # playing is reset
        else:
            drawTwo(canvas)  # draw game2 while playing is true and screen is 2
    else:
        drawOne(canvas)  # draw game one if screen is 1


def stop_all():  # Handler function to the Quit button, closes the frame and ends the music
    game.frame.stop()
    music.pause()


def switch_sounds():  # plays music
    global soundBoolean
    soundBoolean = not soundBoolean
    if soundBoolean:
        music.play()
    else:
        music.pause()


game.welcomeScreen()  # need to run the first frame by default
game.run()
