import pygame
# to display the key press window that will use for movements...like a keyboard UI
def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))

def getKey(keyName):
    ans=False

    for eve in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))

    if keyInput[myKey]:
        ans = True
    pygame.display.update()

    return ans

def main():
    if getKey("q"):
        print("drone has landed")
    if getKey("e"):
        print("drone has taken off")

    if getKey("LEFT"):
        print("drone moved left")
    if getKey("RIGHT"):
        print("drone moved right")
    if getKey("UP"):
        print("drone moved forward")
    if getKey("DOWN"):
        print("drone moved backward")
    if getKey("w"):
        print("drone went higher")
    if getKey("s"):
        print("drone went lower")
    if getKey("a"):
        print("drone moved clockwise")
    if getKey("d"):
        print("drone moved anticlockwise")



# logs in key strokes

if __name__ == '__main__':
    init()
    while True:
        main()
