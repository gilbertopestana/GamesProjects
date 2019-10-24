from user301_dZJL5znAdk_0 import Vector

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# --------------Globals------------------
ball = simplegui.load_image(
    'https://gallery.yopriceville.com/var/albums/Free-Clipart-Pictures/Sport-PNG/Football_Transparent_PNG_Clipart.png?m=1434276657')
chickenHead = simplegui.load_image(
    'https://vignette.wikia.nocookie.net/hotline-miami/images/f/f1/Untitled-3.png/revision/latest?cb=20150310222805')
bg2 = simplegui.load_image('https://img00.deviantart.net/0d1b/i/2009/102/a/0/football_pitch_by_haqn.png')
imageEnd = simplegui.load_image('https://ak9.picdn.net/shutterstock/videos/1010606219/thumb/1.jpg')

WIDTH = 800  # for the frame
HEIGHT = 400

playing = True  # bool for the game in play
endScreen = False  # bool for when endScreen is shown
endFrame = False  # checks if players have pressed 'start'at the endScreen point


# ~~~~~~~~CLASSES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Player:  # to create instances of the player
    def __init__(self, name, vel, pos, radius=50):
        self.name = name  # name of player
        self.pos = pos  # position of player
        self.vel = vel  # velocity of player
        self.image = chickenHead
        self.imageWidth = self.image.get_width()
        self.imageHeight = self.image.get_height()
        self.dimX = 50  # dimentions of image on canvas
        self.dimY = 50
        self.speed = 0.45  # multiplier of players speed
        self.radius = 20
        self.border = 2  # border of circle underneath player sprite
        self.acc = Vector()  # acceleration

    def restart(self):
        self.vel = Vector()  # restart position for players, when scored
        self.acc = Vector()  # similar for acceleration

    def outX(self):  # checking if the players are wanting to go out of bound in the x axis
        if self.name == 1:
            return (
                        self.pos.x < WIDTH / 2 + self.radius or self.pos.x > WIDTH - self.radius)  # checks if position of ball is outside canvas
        return (self.pos.x < 0 + self.radius or self.pos.x > WIDTH / 2 - self.radius)

    def outY(self):  # checking if players go out of bount y axis
        return (self.pos.y - self.radius < 0 or self.pos.y + self.radius > HEIGHT)

    def draw(self, canvas):

        canvas.draw_circle(self.pos.getP(), self.radius, self.border,
                           'Red')  # drawing a circle underneath sprite which actually does the colisions

        canvas.draw_image(self.image, (self.imageWidth / 2, self.imageHeight / 2),
                          # drawing sprite of players, centre source
                          (self.imageWidth, self.imageHeight),  # width hight source
                          (self.pos.x, self.pos.y),  # centre destination
                          (self.dimX, self.dimY))  # width- height destination

    def positionUpdate(self, keyboard):  # allowing player moveent using keyboard class
        if self.name == 1:
            if keyboard.right and self.pos.getP()[0] < (
                    WIDTH - self.radius):  # checks to see player isn't out of bounds on far right x axis
                self.vel.add(Vector(1, 0) * self.speed)  # add to velcoity vector to go to the right
            if keyboard.left and self.pos.getP()[0] > (
                    WIDTH / 2 + self.radius):  # only does as long as it is not off bound left xaxis
                self.vel.add(Vector(-1, 0) * self.speed)  # goes 1 position to the left
            if keyboard.up and self.pos.getP()[1] > (0 + self.radius):  # won't pass vector if player is on edge top
                self.vel.add(Vector(0, -1) * self.speed)  # goes up
            if keyboard.down and self.pos.getP()[1] < (
                    HEIGHT - self.radius):  # won't pass vector if going off screen bottom
                self.vel.add(Vector(0, 1) * self.speed)  # goes down
        else:  # for player 2, similar method but for its buttons
            if keyboard.right2 and self.pos.getP()[0] < (WIDTH / 2 - self.radius):
                self.vel.add(Vector(1, 0) * self.speed)
            if keyboard.left2 and self.pos.getP()[0] > (0 + self.radius):
                self.vel.add(Vector(-1, 0) * self.speed)
            if keyboard.up2 and self.pos.getP()[1] > (0 + self.radius):
                self.vel.add(Vector(0, -1) * self.speed)
            if keyboard.down2 and self.pos.getP()[1] < (HEIGHT - self.radius):
                self.vel.add(Vector(0, 1) * self.speed)

    def update(self, keyboard):
        global WIDTH, HEIGHT
        self.positionUpdate(keyboard)
        if self.vel.x > 4:  # 4 is the max velocity allowed, so that players do not go too quick
            self.vel.x = 4
        if self.vel.y > 4:
            self.vel.y = 4
        if self.vel.x < -4:  # likewise, -4 so its not too slow
            self.vel.x = -4
        if self.vel.y < -4:
            self.vel.y = -4
        if self.outX():  # checking for boundries for x axis
            if self.name == 1:  # confining players to their side of their screen
                if self.pos.x < WIDTH / 2 + 20 and self.vel.x < 0:  # player one has the right half
                    self.vel.x = 0  # sets velocity to 0 so they can't move
                if self.pos.x > WIDTH - 40 and self.vel.x > 0:  # so doesn't go off on right ride screen
                    self.vel.x = 0
            else:
                if self.pos.x < 0 + 40 and self.vel.x < 0:  # player 2 has left side
                    self.vel.x = 0
                if self.pos.x > WIDTH / 2 - 20 and self.vel.x > 0:  # doesn't allow to go off screen left
                    self.vel.x = 0

        if self.outY():  # checking likewise for y axis
            if self.pos.y < 50 and self.vel.y < 0:  # 50 (2*radius + extra so doesn't glitch)
                self.vel.y = 0
            if self.pos.y > HEIGHT - 40 and self.vel.y > 0:
                self.vel.y = 0
        if self.name == 1:
            if keyboard.pressed1 == 0:
                self.vel = self.vel.subtract(self.vel)
        else:
            if keyboard.pressed2 == 0:
                self.vel = Vector()

        self.pos.add(self.vel)  # adding keyboard velocity to chicken

    def collides(self, other):  # checking if two balls passed together are in colision
        return ((self.pos - other.pos).length()
                <= (self.radius + self.border) + (other.radius + other.border))  # border being the border of circles


class Ball:
    def __init__(self, pos, name, radius=25):  # making the football
        self.pos = pos
        self.radius = radius
        self.vel = Vector()
        self.border = 2
        self.name = name
        self.bouncing = False
        self.image = ball
        self.imageWidth = self.image.get_width()
        self.imageHeight = self.image.get_height()
        self.dimX = 60  # dimentions of image on canvas
        self.dimY = 60

    def outX(self):  # checking to see if ball is out of bounds x axis
        return (
                    self.pos.x - self.radius < 0 or self.pos.x + self.radius > WIDTH)  # checks if position of ball is outside canvas

    def outY(self):  # checking to see if ball is out of bounds y axis
        return (self.pos.y - self.radius < 0 or self.pos.y + self.radius > HEIGHT)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.getP(), self.radius, self.border, 'Blue',
                           'Blue')  # draws blue ball which handles colisions

        canvas.draw_image(self.image, (self.imageWidth / 2, self.imageHeight / 2),  # draw football centre source
                          (self.imageWidth, self.imageHeight),  # width hight source
                          (self.pos.x, self.pos.y),  # centre destination
                          (self.dimX, self.dimY))  # width- height destination

    def bounce(self, normal):
        self.vel.reflect(normal)

    def update(self):
        self.pos.add(self.vel)  # updates velocity of ball

        if self.outY() and not self.bouncing:  # bouncing from walls (only on top and bottom)
            self.bouncing = True  # boolean to make sure it doesn't get stuck bouncing with the wall
            self.vel.y *= -0.85  # so that it does not keep gaining speed when bouncing
        else:
            self.bouncing = False

    def collides(self, other):  # checking it is coliding with anything else
        return ((self.pos - other.pos).length()
                <= (self.radius + self.border) + (other.radius + other.border))  # border being the border of circles

    def contains(self, other):  # to avoid sticky balls/ merging with players
        return ((self.pos - other.pos).length() < (self.border + self.radius + other.radius + other.border))


class Score():
    def __init__(self):
        self.hitScore = 0  # score for player 1
        self.hitScore2 = 0  # player 2 score

    def draw(self, canvas):  # drawing scroes on screen
        canvas.draw_text("Score", [255, 20], 20, "White")
        canvas.draw_text("Score", [465, 20], 20, "White")
        canvas.draw_text(str(self.hitScore), [320, 20], 20, "White")
        canvas.draw_text(str(self.hitScore2), [530, 20], 20, "White")

    def hit_score(self):  # method called when player 1 scores
        self.hitScore += 1

    def hit_score2(self):  # method called when player 2 scores
        self.hitScore2 += 1

    def restart(self):  # for when the game is restarted, if they decide to play again, score needs to be reset
        self.hitScore = 0
        self.hitScore2 = 0


class Interaction:
    global score

    def __init__(self, kbd):  # instaciating the plaers and ball, as well as keyboard
        self.kbd = kbd
        self.chicken = Player(1, Vector(), Vector(WIDTH - 50, HEIGHT / 2), 20)
        self.chicken2 = Player(2, Vector(), Vector(0 + 50, HEIGHT / 2), 20)
        self.ball = Ball(Vector(WIDTH / 2, HEIGHT / 2), 5)
        self.objects = [self.chicken, self.chicken2, self.ball]  # put the players and ball in an array
        self.inCollision = set()  # a set to handle anything in collision

    def reset(self):  # restarting these when replaying
        self.chicken.restart()
        self.chicken2.restart()

    def draw(self, canvas):  # drawing players, ball and score
        self.chicken.draw(canvas)
        self.chicken2.draw(canvas)
        self.ball.draw(canvas)
        score.draw(canvas)

    def update(self):
        for object in self.objects:  # goes through the array of players and ball updating
            if object.name == 5:  # checks if it is the ball and updates it
                object.update()
            else:
                object.update(self.kbd)  # update players with keyboard input being recieved

        for o1 in self.objects:  # goes through array to check collisions
            for o2 in self.objects:
                if o1.collides(o2) and o1 != o2:  # for different players hitting ball

                    if (o1.name + o2.name) not in self.inCollision:
                        self.inCollision.add(
                            o1.name + o2.name)  # when coliding add to set inCollision so only handled once when interacting
                        n = (o1.pos - o2.pos).normalize()  # normalise the vector position between ball and player
                        delta = n * (o1.vel - o2.vel).dot(n)  # get dot product of normal and velocity
                        o1.vel.subtract(delta)  # make them opose, and going in different directions
                        o2.vel.add(delta)
                else:
                    self.inCollision.discard(o1.name + o2.name)  # if not coliding

        if self.ball.pos.x < 0:  # checking ball position if it has touched/ gone past goals, and resets position and velcoity
            score.hit_score2()  # adds score to player 2
            self.ball.vel = Vector()
            self.ball.pos = Vector(WIDTH / 2, HEIGHT / 2)
            self.chicken.pos = Vector(WIDTH - 50, HEIGHT / 2)
            self.chicken2.pos = Vector(0 + 50, HEIGHT / 2)
        elif self.ball.pos.x > WIDTH:
            score.hit_score()  # adds score to player 1
            self.ball.vel = Vector()
            self.ball.pos = Vector(WIDTH / 2, HEIGHT / 2)
            self.chicken.pos = Vector(WIDTH - 50, HEIGHT / 2)
            self.chicken2.pos = Vector(0 + 50, HEIGHT / 2)


class Keyboard:
    def __init__(self):  # initialise all buttons pressed to false
        self.pause = False
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.space = False
        self.right2 = False
        self.left2 = False
        self.up2 = False
        self.down2 = False
        self.space2 = False
        self.pressed1 = 0  # increceased and decreased everytime a button is pressed, effect the velocity
        self.pressed2 = 0  # for player 2

    def reset(self):  # when reset
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.space = False
        self.right2 = False
        self.left2 = False
        self.up2 = False
        self.down2 = False
        self.space2 = False
        self.pause = False
        self.pressed1 = 0
        self.pressed2 = 0

    def keyDown(self, key):  # make true for when pressed down
        if key == simplegui.KEY_MAP['space']:  # this set is for player 1
            self.space = True
            self.pressed1 += 1  #
        if key == simplegui.KEY_MAP['right']:
            self.right = True
            self.pressed1 += 1
        if key == simplegui.KEY_MAP['left']:
            self.left = True
            self.pressed1 += 1
        if key == simplegui.KEY_MAP['up']:
            self.up = True
            self.pressed1 += 1
        if key == simplegui.KEY_MAP['down']:
            self.down = True
            self.pressed1 += 1

        if key == simplegui.KEY_MAP['q']:  # this set is for player 2
            self.space2 = True
            self.pressed2 += 1
        if key == simplegui.KEY_MAP['d']:
            self.right2 = True
            self.pressed2 += 1
        if key == simplegui.KEY_MAP['a']:
            self.left2 = True
            self.pressed2 += 1
        if key == simplegui.KEY_MAP['w']:
            self.up2 = True
            self.pressed2 += 1
        if key == simplegui.KEY_MAP['s']:
            self.down2 = True
            self.pressed2 += 1

        if key == simplegui.KEY_MAP['p']:
            self.pause = True

    def keyUp(self, key):  # when not pressed, it is false, and pressed1-=1
        if key == simplegui.KEY_MAP['space']:  # for player 1
            self.space = False
            self.pressed1 -= 1
        if key == simplegui.KEY_MAP['right']:
            self.right = False
            self.pressed1 -= 1
        if key == simplegui.KEY_MAP['left']:
            self.left = False
            self.pressed1 -= 1
        if key == simplegui.KEY_MAP['up']:
            self.up = False
            self.pressed1 -= 1
        if key == simplegui.KEY_MAP['down']:
            self.down = False
            self.pressed1 -= 1

        if key == simplegui.KEY_MAP['q']:  # for player 2
            self.space2 = False
            self.pressed2 -= 1
        if key == simplegui.KEY_MAP['d']:
            self.right2 = False
            self.pressed2 -= 1
        if key == simplegui.KEY_MAP['a']:
            self.left2 = False
            self.pressed2 -= 1
        if key == simplegui.KEY_MAP['w']:
            self.up2 = False
            self.pressed2 -= 1
        if key == simplegui.KEY_MAP['s']:
            self.down2 = False
            self.pressed2 -= 1

        if key == simplegui.KEY_MAP['p']:
            self.pause = False


# ------------------------------------------------------------------------
#####################PROGRAM START#######################################
# ------------------------------------------------------------------------

kbd = Keyboard()  # putting keyboard class in variable so it is easeir to call
interaction = Interaction(kbd)  # likewise for interactions where the keyboard is passed in
score = Score()


def drawGoal(canvas):  # draws the red line of the goal
    canvas.draw_line((0, 0), (0, HEIGHT), 15, 'Red')
    canvas.draw_line((WIDTH, 0), (WIDTH, HEIGHT), 15, 'Red')


def drawBackground2(canvas):  # draws background football pitch image
    image = bg2
    imgW = image.get_width()
    imgH = image.get_height()
    canvas.draw_image(image, (imgW / 2, imgH / 2), (imgW, imgH), (WIDTH / 2, HEIGHT / 2),
                      (WIDTH, HEIGHT))  # draws the background


def endScreen2(canvas):  # drawing the end screen for game 2
    global score, playing, kbd  # taking these gloabl variables
    imgW = imageEnd.get_width()
    imgH = imageEnd.get_height()
    canvas.draw_image(imageEnd, (imgW / 2, imgH / 2), (imgW, imgH), (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_polygon([(320, 70), (320, 110), (500, 110), (500, 70)], 2,
                        'Green')  # drawing a box around that start button

    canvas.draw_text("Start Again", [340, 100], 30, "Grey")
    canvas.draw_text("Start Again", [338, 98], 30, "White")

    if (score.hitScore > score.hitScore2):  # to show who won the match
        canvas.draw_text("Player 1 wins!", [300, 250], 40, "Cyan")
    else:
        canvas.draw_text("Player 2 wins!", [290, 260], 40, "Cyan")

    canvas.draw_text("Player1 Score:", [80, 330], 25, "Grey")  # drawing the scores in anyway
    canvas.draw_text("Player1 Score:", [78, 328], 25, "White")
    canvas.draw_text(str(score.hitScore), [235, 330], 25, "Grey")
    canvas.draw_text(str(score.hitScore), [232, 328], 25, "White")

    canvas.draw_text("Player2 Score:", [470, 330], 25, "Grey")
    canvas.draw_text("Player2 Score:", [468, 328], 25, "White")
    canvas.draw_text(str(score.hitScore2), [625, 330], 25, "Grey")
    canvas.draw_text(str(score.hitScore2), [622, 328], 25, "White")


def click(pos):  # a click method to check for when players press start again button
    global playing, endFrame
    if endScreen:
        if pos[0] > 320 and pos[0] < 500 and pos[1] > 70 and pos[1] < 110:  # click start again
            score.restart()  # reset everything before going to main menu
            interaction.reset()
            kbd.reset()
            endFrame = True
            playing = False


def drawGame2(canvas):  # main draw handler for game 2
    global score, playing, endScreen
    if (score.hitScore == 5 or score.hitScore2 == 5):  # first to 5 goals wins, so draw end screen
        endScreen2(canvas)
        endScreen = True

    else:  # draw the game
        drawBackground2(canvas)
        drawGoal(canvas)  # updating and drawing everything in the game
        interaction.draw(canvas)
        interaction.update()
