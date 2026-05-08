import turtle as t
import random as r

class Food(t.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)
        self.refresh() # Start at a random spot

    def refresh(self):
        # Simplified the math to ensure it stays on the grid
        foodX = r.randint(-14, 14) * 20
        foodY = r.randint(-14, 14) * 20
        self.goto(foodX, foodY)
        return foodX,foodY
