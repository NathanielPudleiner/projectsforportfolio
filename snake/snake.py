import turtle as t

class Snake:
    def __init__(self):
        self.head = t.Turtle(shape="square")
        self.head.penup()
        self.head.speed(0)
        self.head.direction = "stop"
        self.body_parts = []
        
    def move(self):
        # Move the head based on current direction
        if self.head.direction == "up":
            self.head.sety(self.head.ycor() + 20)
        elif self.head.direction == "down":
            self.head.sety(self.head.ycor() - 20)
        elif self.head.direction == "left":
            self.head.setx(self.head.xcor() - 20)
        elif self.head.direction == "right":
            self.head.setx(self.head.xcor() + 20)

    # Corrected method syntax
    def up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    def right(self):
        if self.head.direction != "left":
            self.head.direction = "right"
    
