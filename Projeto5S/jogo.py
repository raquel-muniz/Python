import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10
BALL_SPEED = 5

class PongGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Pong")
        self.player1_y = SCREEN_HEIGHT // 2
        self.player2_y = SCREEN_HEIGHT // 2
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = BALL_SPEED
        self.ball_dy = BALL_SPEED
        self.player1_score = 0
        self.player2_score = 0
        self.keys_pressed = set()
        self.winning_score = 5
        self.game_over_printed = False

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"Player 1: {self.player1_score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_text(f"Player 2: {self.player2_score}", SCREEN_WIDTH - 140, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_rectangle_filled(PADDLE_WIDTH / 2, self.player1_y, PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.WHITE)
        arcade.draw_rectangle_filled(SCREEN_WIDTH - PADDLE_WIDTH / 2, self.player2_y, PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.WHITE)
        arcade.draw_circle_filled(self.ball_x, self.ball_y, BALL_RADIUS, arcade.color.WHITE)

    def update(self, delta_time):
        if self.player1_score >= self.winning_score or self.player2_score >= self.winning_score:
            return  # Stop updating the game if it's over
        
        self.move_paddles()
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Collision detection with top and bottom walls
        if self.ball_y <= BALL_RADIUS or self.ball_y >= SCREEN_HEIGHT - BALL_RADIUS:
            self.ball_dy *= -1

        # Collision detection with paddles
        if (self.ball_x - BALL_RADIUS <= PADDLE_WIDTH and self.player1_y - PADDLE_HEIGHT / 2 <= self.ball_y <= self.player1_y + PADDLE_HEIGHT / 2) \
                or (self.ball_x + BALL_RADIUS >= SCREEN_WIDTH - PADDLE_WIDTH and self.player2_y - PADDLE_HEIGHT / 2 <= self.ball_y <= self.player2_y + PADDLE_HEIGHT / 2):
            self.ball_dx *= -1

        # Scoring
        if self.ball_x <= 0:
            self.player2_score += 1
            self.reset_ball()
        elif self.ball_x >= SCREEN_WIDTH:
            self.player1_score += 1
            self.reset_ball()

        if self.player1_score >= self.winning_score or self.player2_score >= self.winning_score:
            self.game_over()

    def reset_ball(self):
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = BALL_SPEED
        self.ball_dy = BALL_SPEED

    def move_paddles(self):
        if arcade.key.W in self.keys_pressed:
            self.player1_y += PADDLE_SPEED
        if arcade.key.S in self.keys_pressed:
            self.player1_y -= PADDLE_SPEED
        if arcade.key.UP in self.keys_pressed:
            self.player2_y += PADDLE_SPEED
        if arcade.key.DOWN in self.keys_pressed:
            self.player2_y -= PADDLE_SPEED

    def game_over(self):
        # Determine the winner based on scores
        if self.player1_score > self.player2_score:
            winner = "Player 1"
        elif self.player2_score > self.player1_score:
            winner = "Player 2"
        else:
            winner = "It's a tie"

        # Print the winner
        if not self.game_over_printed:
            print(f"Game Over! {winner} wins!")
            print("Press 'R' to restart the game.")
            self.game_over_printed = True

    def restart_game(self):
        self.player1_y = SCREEN_HEIGHT // 2
        self.player2_y = SCREEN_HEIGHT // 2
        self.player1_score = 0
        self.player2_score = 0
        self.reset_ball()
        self.game_over_printed = False

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if key == arcade.key.R:  # Restart game when 'R' key is pressed
            self.restart_game()

    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key) if key in self.keys_pressed else None

def main():
    game = PongGame()
    arcade.run()

if __name__ == "__main__":
    main()