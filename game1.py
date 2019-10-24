from user301_dZJL5znAdk_0 import Vector  # given vector class

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pyga

import random, math

# --------------GLOBALS--------------------

# ----images-----

imageWelcome = simplegui.load_image('https://bastois.tk/gameassets/homescreenNew.png')
imageEnd = simplegui.load_image('https://ak9.picdn.net/shutterstock/videos/1010606219/thumb/1.jpg')

imageFox = simplegui.load_image('https://bastois.tk/foxSprite.png')

blackChicken = simplegui.load_image('https://bastois.tk/gameassets/BlackChick.png')
brownChicken = simplegui.load_image('https://bastois.tk/gameassets/BrownChick.png')
darkBrownChicken = simplegui.load_image('https://bastois.tk/gameassets/DarkBrownchick.png')
lightGreenChicken = simplegui.load_image('https://bastois.tk/gameassets/GreenChicken.png')
greyChicken = simplegui.load_image('https://bastois.tk/gameassets/GreyChick.png')
whiteChicken = simplegui.load_image('https://bastois.tk/gameassets/WhiteChicken.png')
greenChicken = simplegui.load_image('https://bastois.tk/gameassets/greenchick.png')
orangeChicken = simplegui.load_image('https://bastois.tk/gameassets/lightBrownChicken.png')

skins = [blackChicken, brownChicken, darkBrownChicken, lightGreenChicken, greyChicken, whiteChicken, greenChicken,
         orangeChicken]
# skins is needed in order to allow user to choose the skin of their chicken player
player1Index = 5  # index in skins for player 1s sprite
player2Index = 1  # index in skins for player 2s sprite

goldenEgg = simplegui.load_image('https://bastois.tk/gameassets/PowerUpEgg.png')
heartImage = simplegui.load_image('https://ya-webdesign.com/images/heart-sprite-png.png')

oneHeart = simplegui.load_image('https://bastois.tk/gameassets/heart1.png')

purpleC = simplegui.load_image("https://openclipart.org/image/2400px/svg_to_png/190173/SimplePurpleCarTopView.png")
redC = simplegui.load_image(
    "https://b.kisscc0.com/20180705/elq/kisscc0-sports-car-bmw-z-auto-racing-download-red-racing-car-top-view-5b3dedf3f2f7c7.3560132915307852679952.png")
greenC = simplegui.load_image("https://openclipart.org/image/2400px/svg_to_png/190176/SimpleGreenCarTopView.png")
blueC = simplegui.load_image("https://openclipart.org/image/2400px/svg_to_png/190177/SimpleDarkBlueCarTopView.png")
yellowC = simplegui.load_image("https://requestreduce.org/images/car-clipart-sprite-sheet-1.jpg")

road = simplegui.load_image('https://bastois.tk/background3.jpg')

genericEgg = simplegui.load_image('https://bastois.tk/gameassets/genericegg.png')

boom = simplegui.load_image('http://hasgraphics.com/wp-content/uploads/2010/08/spritesheet3.png')

# ---------------

WIDTH = 500
HEIGHT = 500  # width and height of canvas
time = 1  # game timmer used for score

isMultiplayer = False  # used to check if the game is single or multiplayer later in code

# -----GLOBAL VARIABLES FOR CANVAS MENU----------------------------------
w1, w2, w3, w4 = 15, 245, 285, 485
h1, h2, h3, h4 = 80, 115, 130, 160
s1, s2, s3, s4 = 210, 310, 180, 215
e1, e2, e3, e4 = 200, 300, 60, 120
c1, c2, c3, c4, c5 = 'Red', 'Green', 'Red', 'Green', 'Green'
currentState = 'welcome'  # the state game1 is in
screen = 1  # the current screen (game1 or game2)
desiredScreen = 1  # the screen needed
pause = False


# -----------------------------------------------------------------------

# ~~~~~~~~CLASSES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Player:  # class for player sprites
    def __init__(self, name, pos, image, radius=50):  # player takes a name, starting position, image and radius
        self.name = name
        self.pos = pos
        self.vel = Vector()
        self.image = image
        self.imageWidth = self.image.get_width()
        self.imageHeight = self.image.get_height()

        # ----------variables to go thorugh frames---------------------------

        self.columns = 3  # how many images along
        self.rows = 4  # how many images down
        self.i = 0
        self.j = 0  # indicies of tuple
        self.frameIndex = (self.i, self.j)  # tuple of which frame to go to
        self.frameHeight = self.imageHeight / self.rows
        self.frameWidth = self.imageWidth / self.columns
        self.frameCentreY = self.frameHeight / 2
        self.frameCentreX = self.frameWidth / 2
        self.dimX = 50  # dimentions of image on canvas
        self.dimY = 50
        self.x = self.frameWidth * self.frameIndex[
            0] + self.frameCentreX  # centre of sprite image in each position of sheet
        self.y = self.frameHeight * self.frameIndex[1] + self.frameCentreY

        # ---------------------------------------

        self.speed = 4
        self.alive = True  # used to check if player is dead

        self.hearts = Hearts(self.name)  # players health bar
        self.hearts.addLife(3)  # start with 4 lives (starts with 0)

        # --------used these to draw square around player for testing purposes--------
        self.foxWidth, self.foxHeight = self.dimX / 2, self.dimY / 2
        # self.UL = Vector(-self.foxWidth,-self.foxHeight)
        # self.UR = Vector(self.foxWidth,-self.foxHeight)
        # self.DL = Vector(-self.foxWidth,self.foxHeight)
        # self.DR = Vector(self.foxWidth,self.foxHeight)
        # self.points = (self.UL,self.UR,self.DL,self.DR)
        self.radius = self.foxWidth

    def draw(self, canvas):  # player draw method
        self.hearts.draw(canvas)  # draws health bar
        if self.alive:  # if player is still alive
            canvas.draw_image(  # draw the sprite
                self.image,
                (self.x, self.y),  # centre source
                (self.frameWidth, self.frameHeight),  # width hight source
                (self.pos.getP()[0], self.pos.getP()[1]),  # centre destination
                (self.dimX, self.dimY)  # width- height destination
            )

        # --------used these to draw square around player for testing purposes--------
        # if 1==1:
        # canvas.draw_line((self.pos+self.UL).getP(), (self.pos+self.UR).getP(), 2, 'Red')
        # canvas.draw_line((self.pos+self.UR).getP(), (self.pos+self.DR).getP(), 2, 'Red')
        # canvas.draw_line((self.pos+self.DR).getP(), (self.pos+self.DL).getP(), 2, 'Red')
        # canvas.draw_line((self.pos+self.DL).getP(), (self.pos+self.UL).getP(), 2, 'Red')

    def positionUpdate(self, keyboard):  # method used to go through sprite sheet

        newJ = 3  # variable to change row being animated from sprite sheet

        if self.name == "player1":  # for player 1
            if keyboard.right:  # animates different row depending on the key pressed
                newJ = 2
                self.pos.add(Vector(1, 0) * self.speed)
            if keyboard.left:
                newJ = 1
                self.pos.add(Vector(-1, 0) * self.speed)
            if keyboard.up and self.pos.getP()[
                1] > 3 / 5 * HEIGHT:  # also need to check pos[1] because player needs to be confined at bottom of screen
                newJ = 3
                self.pos.add(Vector(0, -1) * self.speed)
            if keyboard.down and self.pos.getP()[1] < HEIGHT:
                newJ = 0
                self.pos.add(Vector(0, 1) * self.speed)

        else:  # same for player2
            if keyboard.right2:
                newJ = 2
                self.pos.add(Vector(1, 0) * self.speed)
            if keyboard.left2:
                newJ = 1
                self.pos.add(Vector(-1, 0) * self.speed)
            if keyboard.up2 and self.pos.getP()[1] > 3 / 5 * HEIGHT:
                newJ = 3
                self.pos.add(Vector(0, -1) * self.speed)
            if keyboard.down2 and self.pos.getP()[1] < HEIGHT:
                newJ = 0
                self.pos.add(Vector(0, 1) * self.speed)

        self.i += 1  # i always increments
        self.j = newJ
        self.x = self.frameWidth * self.frameIndex[0] + self.frameCentreX  # need to reset these
        self.y = self.frameHeight * self.frameIndex[1] + self.frameCentreY

    def update(self, keyboard):  # method to update the player

        self.hearts.update()  # updates health bar

        self.positionUpdate(keyboard)  # updates position/sprite

        if self.alive:  # if player is alive
            self.pos.add(self.vel)  # change position
            self.vel.multiply(0.85)  # regulate veloctiy

            # wraps the player around the screen
            if self.pos.x - self.radius > WIDTH:
                self.pos = Vector(0 - self.radius, self.pos.getP()[1])
            if self.pos.x + self.radius < 0:
                self.pos = Vector(WIDTH + self.radius, self.pos.getP()[1])

            # used for animating sprite
            self.frameIndex = (self.i, self.j)

            if self.i == self.columns:
                self.i = 0
                self.frameIndex = (self.i, self.j)

    def contains(self, other):  # to check if the chicken is touching another object
        return (self.pos - other.pos).length() <= self.radius + other.radius

    def addLife(self, n):  # used to add life to health bar
        self.hearts.addLife(n)

    def removeLife(self):  # used to remove life from health bar
        return self.hearts.removeLife()


class Players:  # class to make list of players, this uses player class
    def __init__(self):
        self.players = []  # list for players
        self.chicken = Player("player1", Vector(WIDTH / 2, HEIGHT - 40), skins[player1Index], 20)  # player1
        self.chicken2 = Player("player2", Vector(WIDTH / 2, HEIGHT - 40), skins[player2Index], 20)  # player2

        if isMultiplayer:
            self.players = [self.chicken, self.chicken2]  # list has both chickens if the user chooses multiplayer
        else:
            self.players = [self.chicken, None]  # list only has one chicken if the user chooses singleplayer

    def draw(self, canvas):  # draw method for players
        for player in self.players:  # for each element of list
            if player != None:
                player.draw(canvas)  # draw if its a player

    def update(self):  # update method for players
        for player in self.players:  # for each element in list
            if player != None:
                player.update()  # update if the element is a player

    def arePlayers(self):  # method to check if there are any players left
        if self.players[0] == None and self.players[1] == None:
            return False  # when both are dead this returns false
        else:
            return True

    def contained(self, player):
        index = self.players.index[player]
        self.players[index] = None  # makes value of player in the list equal to None

    def disappearIfContains(self, others):  # method to check if chicken has been hit by something
        othersContained = []  # list that contains the objects which touched the chicken
        for player in self.players[:]:  # for each element in the list
            def outer():
                if self.players[self.players.index(player)] != None:  # if the element is a player
                    for other in others.getArray():  # for each object in the list of other objects which might have hit it
                        if player.contains(
                                other) and other not in othersContained:  # if it contains it and the other object has not already been checked
                            othersContained.append(other)  # add the object to the list of others
                            if not player.removeLife():  # if a life couldnt be removed becuase there are no lives left
                                player.alive = False  # player is dead
                                self.players[self.players.index(player)] = None  # index of player in list is now None
                                return  # return to the outer loop

            outer()
        return othersContained

    def getArray(self):  # method to return current list of players
        return self.players

    def playerPowerUp(self, ppu):  # method to power the player up
        if ppu[0] in self.players:  # if the player is contained in the list of players who got a power up
            ppu[0].powerUp(ppu[1])  # power up the player with the given power up (either for eggs or hearts)


class Keyboard:  # class to handle keyboard
    def __init__(self):

        # pause
        self.pause = False

        # for player 1
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.space = False

        # for player 2
        self.right2 = False
        self.left2 = False
        self.up2 = False
        self.down2 = False
        self.space2 = False

    def keyDown(self, key):  # method for key down handler

        # setting the booleans for player 1 depending on the key pressed
        if key == simplegui.KEY_MAP['space']:
            self.space = True
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True
        if key == simplegui.KEY_MAP['down']:
            self.down = True

        # setting the booleans for player 2 depending on the key pressed
        if key == simplegui.KEY_MAP['q']:
            self.space2 = True
        if key == simplegui.KEY_MAP['d']:
            self.right2 = True
        if key == simplegui.KEY_MAP['a']:
            self.left2 = True
        if key == simplegui.KEY_MAP['w']:
            self.up2 = True
        if key == simplegui.KEY_MAP['s']:
            self.down2 = True

        if key == simplegui.KEY_MAP['p']:
            self.pause = True

    def keyUp(self, key):  # method for key up handler

        # setting the booleans for player 1 depending on the key unpressed
        if key == simplegui.KEY_MAP['space']:
            self.space = False
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['up']:
            self.up = False
        if key == simplegui.KEY_MAP['down']:
            self.down = False

        # setting the booleans for player 2 depending on the key unpressed
        if key == simplegui.KEY_MAP['q']:
            self.space2 = False
        if key == simplegui.KEY_MAP['d']:
            self.right2 = False
        if key == simplegui.KEY_MAP['a']:
            self.left2 = False
        if key == simplegui.KEY_MAP['w']:
            self.up2 = False
        if key == simplegui.KEY_MAP['s']:
            self.down2 = False

        if key == simplegui.KEY_MAP['p']:
            self.pause = False


class Car:  # class for the cars

    def __init__(self, pos, vel, img):
        self.img = img

        # --variables to draw cars--
        self.imageWidth = self.img.get_width()
        self.imageHeight = self.img.get_height()
        self.centerW = self.imageWidth / 2
        self.centerH = self.imageHeight / 2
        self.pos = pos
        self.vel = vel
        self.border = 1
        # --------------------------
        self.isHit = False  # checks if cars are hit

        self.dimX, self.dimY = 100, 50
        self.carWidth, self.carHeight = self.dimY / 2, self.dimX / 2

        # self.UL = Vector(-self.carWidth,-self.carHeight)
        # self.UR = Vector(self.carWidth,-self.carHeight)
        # self.DL = Vector(-self.carWidth,self.carHeight)
        # self.DR = Vector(self.carWidth,self.carHeight)
        # self.points = (self.UL,self.UR,self.DL,self.DR)

        self.radius = self.carWidth  # ((383/3)+40)/2

    def contains(self, other):  # checks if someting has touched the cars
        return (self.pos - other.pos).length() <= self.radius + other.radius

    def update(self):  # updates the cars' positions
        self.pos.add(self.vel)

    def draw(self, canvas):  # draw method for cars

        canvas.draw_image(self.img, (self.centerW, self.centerH),  # draw car sprites
                          (self.imageWidth, self.imageHeight),
                          (self.pos.x, self.pos.y),
                          (self.dimX, self.dimY),
                          3.14 / 2)

        # used to draw box around cars for testig purposes
        # canvas.draw_line((self.pos+self.UL).getP(), (self.pos+self.UR).getP(), 2, 'Red')
        # canvas.draw_line((self.pos+self.UR).getP(), (self.pos+self.DR).getP(), 2, 'Red')
        # canvas.draw_line((self.pos+self.DR).getP(), (self.pos+self.DL).getP(), 2, 'Red')
        # canvas.draw_line((self.pos+self.DL).getP(), (self.pos+self.UL).getP(), 2, 'Red')


class Cars:  # class that uses car class to make a list of cars
    def __init__(self, vel=Vector(0, 10), border=1):
        self.explosions = Explosions()
        self.allCars = (purpleC, redC, greenC, blueC, yellowC)  # list of car images
        self.cars = []  # list of cars on screen
        self.counter = 0
        self.numberOfLines = 4  # for road lanes
        self.appearanceRate = 30  # how often the cars appear
        self.velocityOfCar = 10  # speed of cars
        self.widthOfLine = (WIDTH - 70) / self.numberOfLines  # for lanes
        self.centerOfLine = self.widthOfLine / 2  # for lanes/where to draw each car

    def draw(self, canvas):
        self.explosions.draw(canvas)  # if a car is due to explode, it wil
        for car in self.cars:
            car.draw(canvas)  # draw each car in list

    def update(self):
        self.explosions.update()  # update any explosions thatre due
        for car in self.cars:
            self.velocityOfCar *= 1.00009  # as game goes along the cars go faster
            car.update()  # update each car
            if car.pos.y - 100 > HEIGHT:  # if a car has gone off screen
                self.cars.remove(car)  # remove it from the list
        if self.counter < self.appearanceRate:  # add to counter
            self.counter += 1
        else:
            self.cars.append(Car(Vector(random.randint(0, 3) * self.widthOfLine + WIDTH // 8 + 35, -300),
                                 Vector(0, self.velocityOfCar),
                                 random.choice(self.allCars))
                             )  # add new car to list at end of each appearance rate interval
            self.counter = 0  # reset the counter

    def removeCar(self, car):  # to remove a car from the list
        self.cars.remove(car)

    def listOfCars(self):  # return the current list of cars
        return self.cars

    def getArray(self):  # return the current list of cars
        return self.cars

    def contained(self, car):  # remove car if contained
        self.removeCar(car)

    def disappearIfContains(self, others):  # method to check if chicken has been hit by something
        othersContained = []  # list of objects touching a car
        for car in self.cars[:]:  # for each car
            for other in others.getArray():  # for each other object
                if car in self.cars and car.contains(
                        other) and other not in othersContained:  # if theyre touching and other object not checked already
                    othersContained.append(other)  # add car to list
                    self.explosions.addExplosion(
                        car.pos)  # add to the list of explosions (cars disappear if theyre hit by egg or fox
                    self.removeCar(car)  # car removed from list
        return othersContained


class Road:  # class for the road on which the chicken is running
    def __init__(self):
        self.img = road
        self.imageWidth = self.img.get_width()
        self.imageHeight = self.img.get_height()
        self.start = -3600 / 2 + 500  # start of image
        self.end = 3600 / 2 + 500  # end of image
        self.pos = Vector(self.imageWidth / 2, self.start)
        self.vel = Vector(0, 5)

    def draw(self, canvas):  # to draw the road
        canvas.draw_image(
            self.img,
            (self.imageWidth / 2, self.imageHeight / 2),  # centre source
            (self.imageWidth, self.imageHeight),  # width hight source
            self.pos.getP(),  # centre destination
            (self.imageWidth, self.imageHeight)  # width- height destination
        )
        canvas.draw_image(
            self.img,
            (self.imageWidth / 2, self.imageHeight / 2),  # centre source
            (self.imageWidth, self.imageHeight),  # width hight source
            (self.pos.getP()[0], self.pos.getP()[1] - 3600),  # centre destination
            (self.imageWidth, self.imageHeight)  # width- height destination
        )

    def update(self):
        self.pos.add(self.vel)
        if self.pos.getP()[1] >= self.end:  # once it reaches the end of the image
            self.pos = Vector(self.imageWidth / 2, self.start)  # starts from the top of the image again

    def increaseSpeed(self, increaser):  # method used to slowly increase speed of road to make game pace faster
        self.vel.multiply(increaser)


class Fox:  # class for the fox enemy
    def __init__(self, pos, radius=25):
        self.vel = Vector(0, 1)
        self.pos = pos
        self.image = imageFox
        # -----variables to go through sprite sheet-------
        self.imageWidth = self.image.get_width()
        self.imageHeight = self.image.get_height()
        self.columns = 8
        self.rows = 2
        self.i = 0
        self.j = 0
        self.frameIndex = (self.i, self.j)
        self.frameHeight = self.imageHeight / self.rows
        self.frameWidth = self.imageWidth / self.columns
        self.frameCentreY = self.frameHeight / 2
        self.frameCentreX = self.frameWidth / 2
        self.dimX = self.frameWidth * 4 / 3  # dimentions of image on canvas
        self.dimY = self.frameHeight * 4 / 3
        self.x = self.frameWidth * self.frameIndex[
            0] + self.frameCentreX  # centre of sprite image in each position of sheet
        self.y = self.frameHeight * self.frameIndex[1] + self.frameCentreY
        # -------------------------------------------------
        self.fps = 0  # used to slow down the sprite sheet animations
        self.health = 3  # foxes health bar
        self.speedLevel = 2
        self.angle = 0  # angle which the fox image should be drawn at
        self.isAlive = True  # used to check if its dead

        # variables used to gravitate and rotate the fox
        self.oldVel = self.vel.copy()
        # used to draw box around fox for testing purposes
        self.foxWidth, self.foxHeight = self.dimX / 5, self.dimY * 2 / 5
        self.UL = Vector(-self.foxWidth, -self.foxHeight)
        self.UR = Vector(self.foxWidth, -self.foxHeight)
        self.DL = Vector(-self.foxWidth, self.foxHeight)
        self.DR = Vector(self.foxWidth, self.foxHeight)
        self.points = (self.UL, self.UR, self.DL, self.DR)
        ##
        self.radius = max(radius, 10)

    def decreaseHealth(self):  # used to decrease the foxes health
        self.health -= 1
        if self.health == 0:
            self.isAlive = False  # it diesonce its lives reach 0
        return self.isAlive  # returns boolean saying if its dead

    def gravitate1(self, chickens):  # method to make fox follow chicken
        if chickens[0] == None:
            if chickens[1] == None:  # if there are no chickens left
                self.vel = Vector(0, 0.000000001)  # fox will barely move
            else:
                newVelocity = chickens[1].pos - self.pos  # if only player 2 is alive
                self.vel = newVelocity.normalize().multiply(self.speedLevel)  # follows player 2
        else:
            if chickens[1] == None:  # if only player 1 is alive
                newVelocity = chickens[0].pos - self.pos
                self.vel = newVelocity.normalize().multiply(self.speedLevel)  # follows player 1
            else:
                chicken = self.closest1(chickens)  # if theyre both alive, follow the chicken thats closer
                newVelocity = chicken.pos - self.pos
                self.vel = newVelocity.normalize().multiply(self.speedLevel)

    def closest1(self, chickens):  # method to check which player is closer to the chicken
        if (chickens[0].pos - self.pos).length() <= (chickens[1].pos - self.pos).length():
            return chickens[0]
        else:
            return chickens[1]

    def contains(self, chicken):  # use to see if fox is touching any objects
        return (self.pos - chicken.pos).length() <= self.radius + chicken.radius + 25

    def draw(self, canvas):
        if self.isAlive:

            # ---variables used to draw box around fox for testing purposes--------
            x, y = self.vel.getP()[0], self.vel.getP()[1]
            foxWidth, foxHeight = self.dimX / 5, self.dimY * 2 / 5

            # canvas.draw_line((self.pos+self.UL).getP(), (self.pos+self.UR).getP(), 2, 'Red')
            # canvas.draw_line((self.pos+self.UR).getP(), (self.pos+self.DR).getP(), 2, 'Red')
            # canvas.draw_line((self.pos+self.DR).getP(), (self.pos+self.DL).getP(), 2, 'Red')
            # canvas.draw_line((self.pos+self.DL).getP(), (self.pos+self.UL).getP(), 2, 'Red')

            # -------------------------------------------------------------------------

            canvas.draw_image(self.image,
                              (self.x, self.y),  # centre source
                              (self.frameWidth, self.frameHeight),  # width hight source
                              (self.pos.getP()[0], self.pos.getP()[1]),  # centre destination
                              (self.dimX, self.dimY),  # width- height destination
                              self.angle)  # rotate the image

            self.fps += 1
            if self.fps % 10 == 0:
                self.nextFrame()  # animate sprite every 10 frames

    def update(self):
        if self.isAlive:  # if the fox is alive
            self.pos.add(self.vel)

            # ---draws fox in the direction of the chicken (so as chicken moves, fox rotates)----
            self.angle = math.atan2(self.vel.y, self.vel.x)
            self.angle = self.angle - (3.14 / 2)

            oldAngle = self.oldVel.angle(Vector(1, 0))
            newAngle = self.vel.copy().angle(Vector(1, 0))

            if self.oldVel.y < 0:
                oldAngle = 2 * math.pi - oldAngle
            if self.vel.y < 0:
                newAngle = 2 * math.pi - newAngle

            for dot in self.points:
                angle = newAngle - oldAngle
                if angle > 0.001 or angle < -0.001:
                    dot.rotateRad(angle)
            # --------------------------------------------------------------------------------------

    def nextFrame(self):  # method to go through the sprite sheet
        if self.i < self.columns:  # to go through row have to get to end of columns
            self.i += 1
            self.frameIndex = (self.i, self.j)
            self.x = self.frameWidth * self.frameIndex[
                0] + self.frameCentreX  # centre of sprite image in each position of sheet
            self.y = self.frameHeight * self.frameIndex[1] + self.frameCentreY
            if self.i == self.columns:  # when u get to end of columns
                self.i = 0  # go back to start of row
                self.frameIndex = (self.i, self.j)
                self.x = self.frameWidth * self.frameIndex[
                    0] + self.frameCentreX  # centre of sprite image in each position of sheet
                self.y = self.frameHeight * self.frameIndex[1] + self.frameCentreY


class Foxes:  # class to make lots of foxes
    def __init__(self):
        self.foxes = []  # list of foxes
        self.counter = 1  # counter to check when a new fox should appear

    def addFox(self):
        self.foxes.append(Fox(Vector(random.choice(range(WIDTH)), -65), 25))  # adds fox to list

    def update(self):
        for fox in self.foxes:
            fox.update()  # update each fox on screen
        if self.counter % 500 == 0:  # add a fox every 500 frames
            self.addFox()
            self.counter = 1  # reset counter once fox added
        else:
            self.counter += 1

    def draw(self, canvas):
        for fox in self.foxes:
            fox.draw(canvas)  # draw each fox

    def gravitate(self, chickens):
        for fox in self.foxes:
            fox.gravitate1(chickens)  # make each fox gravitate to the players

    def disappearIfContains(self, objects):  # method to check if chicken has been hit by something
        objectsContained = []  # list of objects that have touched fox
        for fox in self.foxes[:]:  # for each fox
            def outer():
                for object in objects.getArray():  # for each other object
                    if fox.contains(object):  # and object not in objectsContained:
                        objectsContained.append(object)  # add object to list
                        if not fox.decreaseHealth():  # if foxes health couldnt be decreased because its dead
                            self.removefox(fox)  # remove the fox
                            return  # go around the outer loop again

            outer()
        return objectsContained

    def getArray(self):  # returns list of current foxes
        return self.foxes

    def contained(self, fox):  # remove fox contained by any object later in code
        self.foxes.remove(fox)

    def tick(self):  # tick method to increase counter of fox as the timer goes on
        self.counter += 1

    def removefox(self, fox):
        self.foxes.remove(fox)  # remove fox from list


class Heart:  # class for players lives
    def __init__(self, pos, img):
        self.pos = pos
        self.img = img
        # ---variables to draw hearts--------------------
        self.imageWidth = self.img.get_width()
        self.imageHeight = self.img.get_height()
        self.columns = 3
        self.rows = 1
        self.frameW = self.imageWidth / self.columns
        self.frameH = self.imageHeight / self.rows
        self.i = 0
        self.j = 0
        self.frameIndex = (self.i, self.j)
        self.frameCentreY = self.frameH / 2
        self.frameCentreX = self.frameW / 2
        self.dimX = 25  # dimentions of image on canvas
        self.dimY = 25
        self.x = self.frameW * self.frameIndex[
            0] + self.frameCentreX  # centre of sprite image in each position of sheet
        self.y = self.frameH * self.frameIndex[1] + self.frameCentreY
        # ----------------------------------------------------
        self.currentStage = "empty"  # they can be "full" "half" "empty"
        self.desireStage = "full"

    def draw(self, canvas):  # draws hearts
        canvas.draw_image(self.img,
                          (self.x, self.y),  # centre source
                          (self.frameW, self.frameH),  # width hight source
                          (self.pos.getP()[0], self.pos.getP()[1]),  # centre destination
                          (self.dimX, self.dimY))  # width- height destination

    def update(self):
        if self.currentStage != self.desireStage:  # if current stage isnt full
            if self.currentStage == "half":  # if its half
                self.currentStage = self.desireStage  # make it equal to full
            else:  # otherwise make it equal to half
                self.currentStage = "half"

        if self.currentStage == "full":  # draws hearts at certain stages
            self.i = 0
        elif self.currentStage == "half":
            self.i = 1
        else:
            self.i = 2

        self.frameIndex = (self.i, self.j)  # update sprite
        self.x = self.frameW * self.frameIndex[0] + self.frameCentreX

    def removeLife(self):  # means that the heart is gone
        self.desireStage = "empty"

    def restoreLife(self):  # adds a life
        self.desireStage = "full"


class Hearts:  # uses heart class to make health bar with many hearts
    def __init__(self, name):
        self.pos = Vector(450, 15)  # where the hearts start
        self.name = name
        self.img = heartImage
        self.imageWidth = self.img.get_width()
        self.columns = 3
        self.frameW = self.imageWidth / self.columns
        self.frameCenter = self.frameW / 2
        self.wait = False  # used to make sure that there are a few seconds after a life is lost in which other cant be lost immediately after
        self.counter = 0
        self.heartSeparation = 25  # separation between hearts

        if self.name == "player2":  # changed
            self.heartSeparation *= -1  # if its player 1 it draws the lives at the top right, for player 2 it draws them in the top left
            self.pos = Vector(50, 15)  # has a different starting position

        self.hearts = [Heart(self.pos, self.img)]  # list of hearts

    def draw(self, canvas):
        for heart in self.hearts:
            heart.update()
            heart.draw(canvas)  # draws hearts

        if self.counter < 120:  # counts time between which hearts can be reomved after a life has been removed
            self.counter += 1
        else:
            self.counter = 0
            self.wait = False

    def update(self):
        for heart in self.hearts:  # update each heart
            heart.update()

    def removeLife(self):
        if self.wait == True:
            return True
        for heart in self.hearts[:][::-1]:  # for each heart
            if heart.desireStage == "full":  # if theyre fully drawn
                heart.desireStage = "empty"  # make them disappear
                self.wait = True  # wait a few seconds until the
                return True
        return False  # return false if no lives were left to be removed

    def addLife(self, numberoflife):
        numberOfLife = numberoflife
        for heart in self.hearts:  # for each heart
            if numberOfLife > 0:  # if there are lives
                if heart.desireStage == "empty":  # if a life has gone
                    heart.restoreLife()  # add it back
                    numberOfLife -= 1  # decrease lives needed to be added
            else:
                break  # if no lives, nothing
        for i in range(numberOfLife):  # add rest of hearts needed to be added
            self.hearts.append(Heart(self.pos + Vector(-self.heartSeparation * len(self.hearts), 0), self.img))


class Egg:  # class for egg bullets
    def __init__(self, pos, img, vel, radius=20):
        self.pos = pos
        self.vel = vel
        self.speed = 6
        self.imageSize = max(radius, 20)
        self.radius = self.imageSize / 2
        self.colour = 'Red'
        self.image = img

    def draw(self, canvas):
        canvas.draw_image(self.image,  # draws eggs
                          (self.image.get_width() // 2, self.image.get_height() // 2),
                          (self.image.get_width(), self.image.get_height()),
                          self.pos.getP(),
                          (self.imageSize, self.imageSize))

        # used to draw circles around eggs for testing purposes
        # if 1==1:
        #   canvas.draw_circle(self.pos.getP(), self.radius, 1, 'Red')

    def contains(self, other):  # use to see if a fox or car has been shot
        return ((self.pos - other.pos).length() <= self.radius + other.radius)

    def update(self):  # updates egg
        self.pos.add(self.vel * self.speed)


class Eggs:  # lots of egg bullets that use egg class
    def __init__(self):
        self.radius = 20
        self.colour = 'Red'
        self.image = genericEgg
        self.counter = 0
        self.poweredShoots = 0  # when egg power up is had by player, egg shots are powered up

        self.eggs = []  # list of eggs

    def addEgg(self, pos):
        direction = Vector(0, -1)
        if self.counter >= 20:
            if self.poweredShoots > 0:  # if a powerup is had
                self.poweredShoots -= 1
                self.eggs.append(Egg(pos.copy(), self.image,
                                     direction.copy().rotate(-25)))  # eggs that go at angles to the centre bullet
                self.eggs.append(Egg(pos.copy(), self.image, direction.copy().rotate(25)))
            self.counter = 0  # reset the counter
            self.eggs.append(Egg(pos.copy(), self.image, direction))  # add the egg being shot in the middle

    def removeEgg(self, egg):  # remove an egg
        self.eggs.remove(egg)

    def update(self):
        self.counter += 1
        for egg in self.eggs:  # update each egg
            if (egg.pos.x > WIDTH + egg.radius) or (egg.pos.x < -egg.radius) or (egg.pos.y > HEIGHT + egg.radius) or (
                    egg.pos.y < -egg.radius):
                self.eggs.remove(egg)  # remove eggs once theyre off screen
            egg.update()

    def draw(self, canvas):
        for egg in self.eggs:
            egg.draw(canvas)  # draw each egg

    def disappearIfContains(self, objects):  # method to check if egg has hit an object
        objectsContained = []  # the objects hit
        eggsContained = []  # the eggs that have hit something
        for egg in self.eggs[:]:  # for each egg
            for object in objects.getArray():  # for each object
                if egg.contains(
                        object) and object not in objectsContained:  # if egg is touching object and object is not already contained
                    objectsContained.append(object)  # add it to list
                    if egg not in eggsContained:  # if the egg is not checked already
                        eggsContained.append(egg)  # add it to the egg list
        for egg in eggsContained:
            self.removeEgg(egg)  # remove the eggs that have hit something
        return objectsContained

    def contained(self, egg):  # removes egg depending on if contained
        self.eggs.remove(egg)

    def getArray(self):  # returns current list of eggs
        return self.eggs

    def powerUp(self):  # if a player gets a golden egg power up, they have 3 multibullet/multidirectional shots
        self.poweredShoots += 10


class Score:  # class which keeps score
    def __init__(self):

        # scores for player 1
        self.timeScore = 0
        self.hitScore = 0

        # scores for player 2
        self.timeScore2 = 0
        self.hitScore2 = 0

    def draw(self, canvas):
        canvas.draw_text("Score", [388, 48], 20, "Grey")  # draws scores for player 1
        canvas.draw_text("Score", [390, 50], 20, "White")
        canvas.draw_text(str(self.hitScore), [448, 48], 20, "Grey")
        canvas.draw_text(str(self.hitScore), [450, 50], 20, "White")
        canvas.draw_text("Timer", [388, 88], 20, "Grey")
        canvas.draw_text("Timer", [390, 90], 20, "White")
        canvas.draw_text(str(self.timeScore), [448, 88], 20, "Grey")
        canvas.draw_text(str(self.timeScore), [450, 90], 20, "White")

        if isMultiplayer:  # draws scores for player 2
            canvas.draw_text("Score", [43, 48], 20, "Grey")
            canvas.draw_text("Score", [45, 50], 20, "White")
            canvas.draw_text(str(self.hitScore2), [103, 48], 20, "Grey")
            canvas.draw_text(str(self.hitScore2), [105, 50], 20, "White")
            canvas.draw_text("Timer", [43, 88], 20, "Grey")
            canvas.draw_text("Timer", [45, 90], 20, "White")
            canvas.draw_text(str(self.timeScore2), [103, 88], 20, "Grey")
            canvas.draw_text(str(self.timeScore2), [105, 90], 20, "White")

    def tick(self):
        global timer
        if interaction.chickens.getArray()[0] != None:
            self.timeScore += 1  # if player1 is still alive, update its time score
        if interaction.chickens.getArray()[1] != None:
            self.timeScore2 += 1  # if player2 is still alive, update its time score

    def hit_score(self):  # method to be called if player1 has hit an object
        self.hitScore += 1

    def hit_score2(self):  # method to be called if player2 has hit an object
        self.hitScore2 += 1


class Explosion:  # explosions needed to appear when cars are destoryed
    def __init__(self, pos):
        self.image = boom

        # ------------variables used to draw explosion------------------
        self.imageWidth = self.image.get_width()
        self.imageHeight = self.image.get_height()
        self.columns = 6
        self.rows = 6
        self.i = 0
        self.j = 0
        self.frameIndex = (self.i, self.j)
        self.frameHeight = self.imageHeight / self.rows
        self.frameWidth = self.imageWidth / self.columns
        self.frameCentreY = self.frameHeight / 2
        self.frameCentreX = self.frameWidth / 2
        self.dimX = 100  # dimentions of image on canvas
        self.dimY = 100
        self.x = self.frameWidth * self.frameIndex[
            0] + self.frameCentreX  # centre of sprite image in each position of sheet
        self.y = self.frameHeight * self.frameIndex[1] + self.frameCentreY
        # ------------------------------------------------------------------
        self.pos = pos

    def draw(self, canvas):
        canvas.draw_image(  # draw the image
            self.image,
            (self.x, self.y),  # centre source
            (100, 100),  # width hight source
            (self.pos.getP()),  # centre destination
            (self.dimX, self.dimY))  # width- height destination
        self.nextFrame()  # animate the explosion

    def nextFrame(self):  # method to go through frames of explosion sprite sheet
        if self.i < self.columns:
            self.i += 1
            self.frameIndex = (self.i, self.j)
            self.x = self.frameWidth * self.frameIndex[0] + self.frameCentreX
            self.y = self.frameHeight * self.frameIndex[1] + self.frameCentreY
            if self.i == self.columns:
                self.j += 1
                self.i = 0
                self.frameIndex = (self.i, self.j)
                self.x = self.frameWidth * self.frameIndex[0] + self.frameCentreX
                self.y = self.frameHeight * self.frameIndex[1] + self.frameCentreY
                if self.j == self.rows and self.i == self.columns / 2:
                    self.i = 0
                    self.j = 0
                    self.frameIndex = (self.i, self.j)
                    self.x = self.frameWidth * self.frameIndex[0] + self.frameCentreX
                    self.y = self.frameHeight * self.frameIndex[1] + self.frameCentreY


class Explosions:  # class for list of explosions
    def __init__(self):
        self.explosions = []  # list of explosions

    def draw(self, canvas):
        for explosion in self.explosions:
            explosion.draw(canvas)  # draw each explosion

    def update(self):
        for explosion in self.explosions:  # removes explosion from list once its done going through the sprite sheet
            if explosion.j == explosion.rows and explosion.i == explosion.columns / 2:
                self.explosions.remove(explosion)

    def addExplosion(self, pos):
        self.explosions.append(Explosion(pos))  # add explosion to list


class PowerUp:
    def __init__(self, pos, vel, img):
        self.img = img  # takes different image depending on the power up

        # ----variables to draw power up------
        self.imageWidth = self.img.get_width()
        self.imageHeight = self.img.get_height()
        self.centerW = self.imageWidth / 2
        self.centerH = self.imageHeight / 2
        # ------------------------------------
        self.pos = pos
        self.vel = vel
        self.radius = 20

    def contains(self, other):  # checks if power up is touching another object
        return (self.pos - other.pos).length() <= self.radius + other.radius

    def update(self):  # makes power up move down canvas
        self.pos.add(self.vel)

    def draw(self, canvas):
        # draws power up
        canvas.draw_image(self.img, (self.centerW, self.centerH),
                          (self.imageWidth, self.imageHeight),
                          (self.pos.x, self.pos.y),
                          (40, 40))


class PowerUps:  # list of power ups
    def __init__(self, vel=Vector(0, 10), border=1):
        # the different images----
        self.imageEgg = goldenEgg
        self.heartImage = oneHeart
        # ------------------------
        self.powerUps = []  # list of power ups
        self.images = [[self.imageEgg, 0], [self.heartImage, 1]]  # list of images and their ids
        self.counter = 0  # counter for how often power ups should appear
        self.appearanceRate = 800  # ^^^same
        self.velocityOfGoldEgg = 5  # speed of the powerups down the screen
        self.numberOfLines = 4  # lanes in road
        self.widthOfLine = (WIDTH - 70) / self.numberOfLines
        self.centerOfLine = self.widthOfLine / 2

    def draw(self, canvas):
        for powerUp in self.powerUps:  # draw each image
            powerUp[0].draw(canvas)

    def update(self):

        selectedPower = random.choice(self.images)  # a random power p appears after each appearance rate is done

        if self.counter < self.appearanceRate:
            self.counter += 1  # keep increasing counter until its equal to aR
        else:
            self.powerUps.append([PowerUp(Vector(random.randint(0, 3) * self.widthOfLine + WIDTH // 8 + 35, -300),
                                          Vector(0, self.velocityOfGoldEgg), selectedPower[0]), selectedPower[1]])
            self.counter = 0  # once theyre equal reset the counter and add a power up

        for powerUp in self.powerUps:  # for each power up
            powerUp[0].update()  # update each one
            if powerUp[0].pos.y - 100 > HEIGHT:  # if its gone out of the frame, remove it from the list
                self.powerUps.remove(powerUp)

    def removePowerUp(self, powerUp):
        self.powerUps.remove(powerUp)  # to remove power up from list

    def getEggArray(self):
        return self.powerUp  # returns current list of power ups

    def contained(self, powerUp):
        self.removePowerUp(powerUp)  # remove power up if contained in any situation

    def disappearIfContains(self, players):  # method to check if power up has been taken bby a player
        playersContained = []  # list of players which took the power up
        for powerUp in self.powerUps[:]:  # for each powerup
            for player in players.getArray():  # for each player
                if player != None and powerUp in self.powerUps and powerUp[0].contains(
                        player) and player not in playersContained:
                    # if the player is alive and the power up hasnt been taken already and theyre touching
                    playersContained.append(
                        [player, powerUp[1]])  # add the player to the list along with the power up id
                    self.removePowerUp(powerUp)  # remove the power up from the list
        return playersContained


class Interaction:  # handling interactions between players
    def __init__(self, kbd):  # takes a keyboard
        self.kbd = kbd
        self.chickens = Players()  # need to make players
        self.eggArray = Eggs()  # since eggs arent attached to players from within, each player needs their own egg list
        self.eggArray2 = Eggs()
        self.road = Road()  # need a road and cars that appear at their appearance rate
        self.cars = Cars()
        # self.explosions = Explosions()
        self.foxes = Foxes()
        self.foxes.addFox()
        self.powerUps = PowerUps()

    def removeEggs(self, eggs, eggArray):  # method to remove eggs that have hit an object
        # method takes an egg list associated with a player and an eggArray of eggs which have hit an object
        global score
        for egg in eggs:  # for each egg
            if egg in eggArray.getArray() and eggArray == self.eggArray:  # if player1 has hit an objectwith their eggs
                eggArray.removeEgg(
                    egg)  # remove an egg
                score.hit_score()  # increase the score of player 1
            elif egg in eggArray.getArray() and eggArray == self.eggArray2:  # if player2 has hit an object with their eggs
                eggArray.removeEgg(egg)  # remove egg
                score.hit_score2()  # increase score of player 2

    def powerUpFilter(self, powerUpArray):  # method to check which power ups go with which player
        for powerUp in powerUpArray:  # for each power up in given array
            if powerUp[1] == 0:  # if the id is equal to 0 (0 is associated with eggs)
                if powerUp[0].name == 'player1':  # if the player to be powered up is 1
                    self.eggArray.powerUp()  # power up the eggs for player 1
                else:
                    self.eggArray2.powerUp()  # otherwise powerup the eggs for player 2
            else:  # the id 1 is associated with heart power ups
                if powerUp[0].name == 'player1' and len(powerUp[
                                                            0].hearts.hearts) < 8:  # even if it gets life and dies at same time, life check will happen first so wont die
                    # if its for player 1 and they havent reached maximum number of lives
                    self.chickens.players[0].addLife(1)  # add a life to player 1s health bar
                elif powerUp[0].name == 'player2' and len(powerUp[0].hearts.hearts) < 8:  # otherwise if its player 2
                    self.chickens.players[1].addLife(1)  # add a life to 2s health bar

    def draw(self, canvas):
        # draw method which draws each necessary object for game 1
        self.road.draw(canvas)
        for chicken in self.chickens.getArray():  # change
            if chicken != None:
                chicken.draw(canvas)
        self.cars.draw(canvas)
        self.foxes.draw(canvas)
        self.eggArray.draw(canvas)
        self.eggArray2.draw(canvas)
        self.powerUps.draw(canvas)

    def update(self):
        global pause
        # update method checks for any collisions between objects and also updates all the relevant objects

        if self.kbd.pause:
            pause = not pause
        if pause:
            print("game is paused")
            return

        if self.kbd.space:  # if player 1 shoots
            if self.chickens.getArray()[0] != None:  # if the player is alive
                self.eggArray.addEgg(
                    Vector(self.chickens.getArray()[0].pos.x, self.chickens.getArray()[0].pos.y))  # fires egg
        if self.kbd.space2:  # if player 2 shoots
            if self.chickens.getArray()[1] != None:  # if the player is alive
                self.eggArray2.addEgg(
                    Vector(self.chickens.getArray()[1].pos.x, self.chickens.getArray()[1].pos.y))  # fires egg

        self.foxes.gravitate(self.chickens.getArray())  # make foxes follow the chickens

        self.powerUpFilter(self.powerUps.disappearIfContains(self.chickens))
        # checks if the power ups have been taken by any player
        # then apply the necessary power up to that player

        self.removeEggs(self.foxes.disappearIfContains(self.eggArray), self.eggArray)
        self.removeEggs(self.foxes.disappearIfContains(self.eggArray2), self.eggArray2)
        # makes foxes lose health or die if they have been hit by any egg

        self.removeEggs(self.cars.disappearIfContains(self.eggArray), self.eggArray)
        self.removeEggs(self.cars.disappearIfContains(self.eggArray2), self.eggArray2)
        # makes cars disappear if hit by eggs and then also makes eggs disappear

        carsFoxes = self.cars.disappearIfContains(self.foxes)
        # checks if foxes are touching a car; if they are, it makes the car disappear

        chickensCars = self.chickens.disappearIfContains(self.cars)  # checks if the players hit by cars
        chickensFoxes = self.chickens.disappearIfContains(self.foxes)  # checks if players hit by foxes

        self.road.update()
        self.road.increaseSpeed(1.0005)
        for chicken in self.chickens.getArray():  # change
            if chicken != None:
                chicken.update(self.kbd)
        self.cars.update()
        self.foxes.update()
        self.eggArray.update()
        self.eggArray2.update()
        self.powerUps.update()


# ------------------------------------------------------------------------
#####################PROGRAM START#######################################
# ------------------------------------------------------------------------
# needed global objects:
kbd = Keyboard()
score = Score()
interaction = Interaction(kbd)


def click(pos):  # method used to handle mouse clicks
    global c1, c2, c3, c4, currentState, isMultiplayer, interaction, score, player1Index, player2Index, screen, desiredScreen

    if (currentState == 'welcome'):  # if user is on welcome screen

        if isMultiplayer:
            # if they have selected multiplayer mode for game1
            # they can choose the skin of their player
            if ((pos[0] > 110 - 25 and pos[0] < 110 + 25 and pos[1] > 380 - 25 and pos[1] < 380 + 25) or (
                    pos[0] > 140 and pos[0] < 252 and pos[1] > 370 and pos[1] < 400)):
                # each time the player clicks the button to change their skin, it goes draws the next image in the skin list
                player1Index += 1
                if player1Index == player2Index:
                    player1Index += 1  # the players will never have the same skin
                if player1Index > len(skins) - 1:
                    player1Index = 0
            if ((pos[0] > 110 - 25 and pos[0] < 110 + 25 and pos[1] > 450 - 25 and pos[1] < 450 + 25) or (
                    pos[0] > 140 and pos[0] < 252 and pos[1] > 440 and pos[1] < 470)):
                player2Index += 1  # same for player 2
                if player1Index == player2Index:
                    player2Index += 1
                if player2Index > len(skins) - 1:
                    player2Index = 0
        else:  # if its single player, it only needs it for player 1
            if ((pos[0] > 110 - 25 and pos[0] < 110 + 25 and pos[1] > 410 - 25 and pos[1] < 410 + 25) or (
                    pos[0] > 140 and pos[0] < 252 and pos[1] > 400 and pos[1] < 430)):
                player1Index += 1
                if player1Index > len(skins) - 1:
                    player1Index = 0

        if (pos[0] > w1 and pos[0] < w2):  # button to make single player
            if (pos[1] > h1 and pos[1] < h2):
                c1 = 'Red'
                c2 = 'Green'
                isMultiplayer = False
            if (pos[1] > h3 and pos[1] < h4):  # button to make game1
                c3 = 'Red'
                c4 = 'Green'
                desiredScreen = 1
        if (pos[0] > w2 and pos[0] < w4):
            if (pos[1] > h1 and pos[1] < h2):  # button to make multiplayer
                c2 = 'Red'
                c1 = 'Green'
                isMultiplayer = True
            if (pos[1] > h3 and pos[1] < h4):  # button to make game 2
                c4 = 'Red'
                c3 = 'Green'
                desiredScreen = 2
        if (pos[0] > s1 and pos[0] < s2):
            if (pos[1] > s3 and pos[1] < s4):  # start button
                if desiredScreen == 1:
                    currentState = 'game1'
                elif desiredScreen == 2:
                    screen = desiredScreen
                    c1 = 'Red'
                    c2 = 'Green'
                    isMultiplayer = False
                    c3 = 'Red'
                    c4 = 'Green'

                    # at the start we need to reset the interaction and score
        interaction = Interaction(kbd)
        score = Score()

    if (currentState == 'endScreen'):  # end of game1
        if (pos[0] > e1 and pos[
            0] < e2):  # if start again button on end screen of game 1 is clicked, it will go to the welcome screen
            if (pos[1] > e3 and pos[1] < e4):
                currentState = 'welcome'


def selector(canvas):  # method to choose draw method which will be used by frame
    # uses currentState to check what needs to be drawn at different stages
    if (currentState == 'welcome'):
        drawWelcome(canvas)
    elif (currentState == 'game1'):
        draw(canvas)
    elif (currentState == 'endScreen'):
        drawEnd(canvas)


def drawWelcome(canvas):
    # method to draw welcome screen

    imgWidth = imageWelcome.get_width()
    imgHeight = imageWelcome.get_height()
    canvas.draw_image(imageWelcome, (imgWidth // 2, imgHeight // 2), (imgWidth, imgWidth), (WIDTH // 2, HEIGHT // 2),
                      (WIDTH, HEIGHT))

    # buttons:
    canvas.draw_polygon([(w1, h1), (w1, h2), (w2, h2), (w2, h1)], 2, c1)
    canvas.draw_polygon([(w3, h1), (w4, h1), (w4, h2), (w3, h2)], 2, c2)
    canvas.draw_polygon([(w1, h3), (w2, h3), (w2, h4), (w1, h4)], 2, c3)
    canvas.draw_polygon([(w3, h3), (w4, h3), (w4, h4), (w3, h4)], 2, c4)
    canvas.draw_polygon([(s1, s3), (s2, s3), (s2, s4), (s1, s4)], 2, c5)

    if isMultiplayer:  # need to draw 2 chickens so that both players can see their skin

        canvas.draw_text("Player 1", [10, 395], 23, "Grey")
        canvas.draw_text("Player 1", [10, 393], 23, "White")

        canvas.draw_text("Player 2", [10, 465], 23, "Grey")
        canvas.draw_text("Player 2", [10, 463], 23, "White")

        canvas.draw_text("Change skin", [140, 395], 23, "Grey")
        canvas.draw_text("Change skin", [138, 393], 23, "White")

        canvas.draw_text("Change skin", [140, 465], 23, "Grey")
        canvas.draw_text("Change skin", [138, 463], 23, "White")

        # used to look at which skin will be used by the user
        canvas.draw_image(skins[player1Index],
                          (skins[player1Index].get_width() / 6, skins[player1Index].get_width() / 8),
                          (skins[player1Index].get_width() / 3, skins[player1Index].get_width() / 4),
                          (110, 380),
                          (50, 50))

        canvas.draw_image(
            skins[player2Index],
            (skins[player2Index].get_width() / 6, skins[player2Index].get_width() / 8),
            (skins[player2Index].get_width() / 3, skins[player2Index].get_width() / 4),
            (110, 450),
            (50, 50))

    else:  # only draws one chicken

        canvas.draw_text("Player 1", [10, 427], 23, "Grey")
        canvas.draw_text("Player 1", [10, 425], 23, "White")

        canvas.draw_text("Change skin", [140, 427], 23, "Grey")
        canvas.draw_text("Change skin", [138, 425], 23, "White")

        canvas.draw_image(
            skins[player1Index],
            (skins[player1Index].get_width() / 6, skins[player1Index].get_width() / 8),
            (skins[player1Index].get_width() / 3, skins[player1Index].get_width() / 4),
            (110, 410),
            (50, 50))


def drawEnd(canvas):
    # method for drawing the end screen for game 1

    imgW = imageEnd.get_width()
    imgH = imageEnd.get_height()
    canvas.draw_image(imageEnd, (imgW / 2, imgH / 2), (imgW, imgH), (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_polygon([(e1, e3), (e2, e3), (e2, e4), (e1, e4)], 2, c5)

    # start again button
    canvas.draw_text("Start Again", [200, 100], 23, "Grey")
    canvas.draw_text("Start Again", [198, 98], 23, "White")

    # player 1 score at the end
    canvas.draw_text("Player 1 score:", [50, 330], 23, "Grey")
    canvas.draw_text("Player 1 score:", [48, 328], 23, "White")
    canvas.draw_text(str(score.hitScore), [200, 330], 23, "Grey")
    canvas.draw_text(str(score.hitScore), [198, 328], 23, "White")
    canvas.draw_text("Player 1 timer:", [50, 370], 23, "Grey")
    canvas.draw_text("Player 1 timer:", [48, 368], 23, "White")
    canvas.draw_text(str(score.timeScore), [200, 370], 20, "Grey")
    canvas.draw_text(str(score.timeScore), [198, 368], 20, "White")

    if isMultiplayer:
        # player 2 score at the end
        canvas.draw_text("Player 2 score:", [280, 330], 23, "Grey")
        canvas.draw_text("Player 2 score:", [278, 330], 23, "White")
        canvas.draw_text(str(score.hitScore2), [430, 330], 23, "Grey")
        canvas.draw_text(str(score.hitScore2), [428, 328], 23, "White")
        canvas.draw_text("Player 2 timer:", [280, 370], 23, "Grey")
        canvas.draw_text("Player 2 timer:", [278, 369], 23, "White")
        canvas.draw_text(str(score.timeScore2), [430, 370], 23, "Grey")
        canvas.draw_text(str(score.timeScore2), [428, 368], 23, "White")


def draw(canvas):
    # draws game 1

    global currentState
    interaction.update()
    interaction.draw(canvas)
    score.draw(canvas)

    if not interaction.chickens.arePlayers():  # if both players are dead, go to end screen
        currentState = 'endScreen'


def tick():  # tick method for our timer, increments score for players
    global timer, time
    time += 1
    score.tick()


timer = simplegui.create_timer(1000, tick)  # timer
timer.start()