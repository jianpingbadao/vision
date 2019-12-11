from random import randint
import time


class Car:

    def __init__(self, i, xi, yi, max_age):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0, 255)
        self.G = randint(0, 255)
        self.B = randint(0, 255)
        self.done = False  # it is not used yet; can be used in going_UP()/going_DONW()
        self.state = '0'  # '0': not count yet; '1': already count; TODO: it is redundent with self.dir
        self.age = 0
        self.max_age = max_age
        self.dir = None

    def getRGB(self):  # For the RGB colour
        return (self.R, self.G, self.B)

    def getTracks(self):
        return self.tracks

    def getId(self):  # For the ID
        return self.i

    def getState(self):
        return self.state

    def getDir(self):
        return self.dir

    def getX(self):  # for x coordinate
        return self.x

    def getY(self):  # for y coordinate
        return self.y

    def updateCoords(self, xn, yn):
        """
        update the coordinates of the vehicle, and add the previous coordinates
        into its tracks

        Parameters
        ----------
        xn : int
            The current x location of the vehicle
        yn : int
            The current y location of the vehicle
        """
        self.age = 0
        self.tracks.append([self.x, self.y])
        self.x = xn
        self.y = yn

    def setDone(self):
        self.done = True

    def timedOut(self):
        return self.done

    def going_UP(self, mid_line):
        if self.dir:
            return False

        if len(self.tracks) >= 2:
            if self.state == '0':
                # TODO: This probably is not suitable for low frame rate video
                # consider to change to directly compare the consecutive two coordinates
                # i.e.
                # if self.tracks[-1][1] < self.tracks[-2][1]:
                if self.tracks[-1][1] < mid_line and self.tracks[-2][1] >= mid_line:
                    self.state = '1'
                    self.dir = 'up'
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def going_DOWN(self, mid_line):
        if self.dir:
            return False

        if len(self.tracks) >= 2:
            if self.state == '0':
                # TODO: The same change goes here as with going_UP()
                # if self.tracks[-1][1] > self.tracks[-2][1]:
                if self.tracks[-1][1] > mid_line and self.tracks[-2][1] <= mid_line:
                    self.state = '1'
                    self.dir = 'down'
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True


# Class2

class MultiCar:
    def __init__(self, cars, xi, yi):
        self.cars = cars
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0, 255)
        self.G = randint(0, 255)
        self.B = randint(0, 255)
        self.done = False
