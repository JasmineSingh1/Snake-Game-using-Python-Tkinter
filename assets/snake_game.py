import tkinter as tk
from PIL import Image, ImageTk
from random import randint

root = tk.Tk()
root.resizable(0,0)

# creating snake class
class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(root,
                         width = 600,
                         height=600,
                         background = '#000000',
                         highlightthickness = 0)
        self.load_images()
        self.score = 0
        self.snake_positions = [(200,100), (180,100), (160,100)]
        self.food_position = self.new_food_position()
        self.direction ='Right'
        self.insert_objects()
        self.bind_all('<Key>', self.on_key_press)
        self.perform_action()
        
        self.pack() 

    # creating load image function
    def load_images(self):
        self.food_image_photo = Image.open('Snake-Game-using-Python-Tkinter/assets/purple_food.jpg')
        self.food_image = ImageTk.PhotoImage(self.food_image_photo)
        
        self.snake_image_photo = Image.open('Snake-Game-using-Python-Tkinter/assets/green_snake.jpg')
        self.snake_image = ImageTk.PhotoImage(self.snake_image_photo)

    # creating insert objects function
    def insert_objects(self):
        self.create_text(40, 7, text = f"Score:{self.score}",fill='#ffffff', font=10, tags='text')
        self.create_rectangle(5,21,595,595, outline='#ffffff', tags='rect')
        self.create_image(self.food_position[0], self.food_position[1], image = self.food_image, tags='food')
        
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image = self.snake_image, tags='snake')

    # creating move snake function
    def move_snake(self):
        if self.direction=='Right':
            new_head_x_position = self.snake_positions[0][0]+20
            new_head_y_position = self.snake_positions[0][1]

        elif self.direction=='Left':
            new_head_x_position = self.snake_positions[0][0]-20
            new_head_y_position = self.snake_positions[0][1]

        elif self.direction=='Up':
            new_head_x_position = self.snake_positions[0][0]
            new_head_y_position = self.snake_positions[0][1]-20

        elif self.direction=='Down':
            new_head_x_position = self.snake_positions[0][0]
            new_head_y_position = self.snake_positions[0][1]+20
        
        self.snake_positions = [(new_head_x_position, new_head_y_position)]+self.snake_positions[:-1]

        snakes = self.find_withtag('snake')
        for snake, position in zip(snakes, self.snake_positions):
            self.coords(snake, position[0], position[1])

    def check_collision(self):
        head_x, head_y = self.snake_positions[0]
        if (head_x in (0,600)) or (head_y in (20,600)) or ((head_x, head_y) in self.snake_positions[1:]):
            return True
        return False
    
    def on_key_press(self, event):
        all_directions = ('Right', 'Left', 'Up', 'Down')
        opposite_directions = [{'Up','Down'},{'Right','Left'}]
        new_direction = event.keysym
        if (new_direction in all_directions) and ({self.direction, new_direction} not in opposite_directions):
            self.direction = new_direction

    def new_food_position(self):
        while True:
            food_x = randint(1, 29) * 20
            food_y = randint(3, 30) * 20

            if ((food_x, food_y) not in self.snake_positions):
                return (food_x, food_y)

    def food_collision(self):
        head_x, head_y = self.snake_positions[0]
        if (head_x, head_y) == self.food_position:
            self.score += 1
            self.itemconfigure(self.find_withtag('text'), text=f"Score: {self.score}")

            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1], image = self.snake_image, tags='snake')

            self.food_position = self.new_food_position()
            self.coords(self.find_withtag('food'), *self.food_position)
    
    def perform_action(self):
        if self.check_collision():
            self.end_game()
            return
        if self.food_collision():
            return
        self.move_snake()
        self.after(100, self.perform_action)

    def end_game(self):
        self.create_text(self.winfo_width()/2, self.winfo_width()/2, text = f"Game Over\nYour score is:{self.score}",fill='red', font=10, tags='end_game_text')
    
        self.restart_button = tk.Button(
            root,
            text="Restart Game",
            bg="green",
            fg="white",
            font=("Times New Roman", 14, "bold"),
            command=self.restart_game
        )
        self.restart_button.pack(pady=10)

    def restart_game(self):
        self.start_new_game()

    def start_new_game(self):
        self.score = 0
        self.direction = 'Right'
        self.snake_positions = [(200,100),(180,100), (160,100)]
        self.food_position = self.new_food_position()

        self.delete('all')

        if hasattr(self, "restart_button"):
            self.restart_button.destroy()
        
        # Draw objects
        self.insert_objects()

        # Restart movement 
        self.perform_action()

board = Snake()

root.mainloop()