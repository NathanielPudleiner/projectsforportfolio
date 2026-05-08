import turtle as t

class Snakebot:
    def __init__(self):
        self.head = t.Turtle(shape="square")
        self.head.penup()
        self.head.speed(0)
        self.head.direction = "UP"
        self.body_parts = []
        
    # Python helper NotebookLM assistance with bot snake movement logic 
    # Instance method to decide movement toward food
    def update_direction(self):
        x,y = self.head.pos()
        if x < self.fx:
            self.head.direction == "RIGHT"
            self.head.setx(self.head.xcor() + 20)
        elif y < self.fy:
            self.head.direction == "UP"
            self.head.sety(self.head.ycor() + 20)
        elif x > self.fx:
            self.head.direction == "LEFT"
            self.head.setx(self.head.xcor() - 20)
        elif y > self.fy:
            self.head.direction == "DOWN"
            self.head.sety(self.head.ycor() - 20)
        print(self.head.direction,x,y)
