import arcade
import arcade.camera
import arcade.draw
import arcade.tilemap

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SCALING = 1.5
PLAYER_SCALING = 2.5
PLAYER_SPEED = 5
MAP_PATH = "TILED_tsx/game.tmj"

PLAYER_TEXTURES = {
    "up": "personagens/tile_0106.png",
    "down": "personagens/tile_0105.png",
    "right": "personagens/tile_0107.png",
    "left": "personagens/tile_0104.png"

}
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(PLAYER_TEXTURES["down"], PLAYER_SCALING)
        self.change_x = 0
        self.change_y = 0
        self.textures = {
            "up": arcade.load_texture(PLAYER_TEXTURES["up"]),
            "down": arcade.load_texture(PLAYER_TEXTURES["down"]),
            "right": arcade.load_texture(PLAYER_TEXTURES["right"]),
            "left": arcade.load_texture(PLAYER_TEXTURES["left"]),
        }

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def update_direction(self, direction):
        self.texture = self.textures[direction]


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Fazendinha do distrito", resizable=False)
        arcade.set_background_color((0, 149, 233))
        self.scene = arcade.Scene()
        self.player = None
        self.camera = arcade.Camera2D()
        self.wall_list = arcade.SpriteList()

    def setup(self):
        try:
            tile_map = arcade.load_tilemap(MAP_PATH, scaling=TILE_SCALING)
            self.scene = arcade.Scene.from_tilemap(tile_map)
            try:
                self.wall_list = self.scene.get_sprite_list("Walls")
            except KeyError:
                print("Camada 'houses' não encontrada.")
                self.wall_list = arcade.SpriteList()
        except Exception as e:
            print(f"Erro ao carregar o mapa: {e}")
            self.scene = arcade.Scene()
            self.wall_list = arcade.SpriteList()

        self.player = Player()
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.scene.add_sprite("Player", self.player)

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.scene.draw()

    def on_update(self, delta_time):
        old_position = self.player.position
        self.player.update()

        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.position = old_position

        target = (
            max(self.player.center_x - SCREEN_WIDTH // 10, 0),
            max(self.player.center_y - SCREEN_HEIGHT // 10, 0),
        )
        self.camera.position = arcade.math.lerp_2d(self.camera.position, target, 0.2)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
            self.player.update_direction("up")
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED
            self.player.update_direction("down")
        elif key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
            self.player.update_direction("left")
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED
            self.player.update_direction("right")

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0

if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()
