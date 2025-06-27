import arcade
import arcade.tilemap

# Configurações gerais
WIDTH = 800
HEIGHT = 600
TILE_SCALING = 1.9
PLAYER_SPEED = 5

class Player(arcade.Sprite):
    """Classe para o jogador com movimentação livre."""
    def __init__(self, image_path, scale):
        super().__init__(image_path, scale)
        self.change_x = 0
        self.change_y = 0

    def update(self):
        """Atualiza a posição do jogador."""
        self.center_x += self.change_x
        self.center_y += self.change_y

    def on_key_press(self, key):
        """Movimenta o jogador nas quatro direções."""
        if key == arcade.key.UP:
            self.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT:
            self.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.change_x = PLAYER_SPEED

    def on_key_release(self, key):
        """Para o movimento ao soltar a tecla."""
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.change_x = 0

class MyGame(arcade.Window):
    """Classe principal do jogo."""
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Meu Jogo 2D Top-Down")
        self.scene = None
        self.player = None
        self.camera = arcade.Camera2D()

    def setup(self):
        """Configura o jogo."""
        try:
            tile_map = arcade.load_tilemap("./mapasTILED/game.tmj", scaling=TILE_SCALING)
            self.scene = arcade.Scene.from_tilemap(tile_map)
        except Exception as e:
            print(f"Erro ao carregar o mapa: {e}")
            self.scene = arcade.Scene()

        # Criar o jogador
        self.player = Player("./TILED_tsx/urban/kenney_rpg-urban-pack/Tiles/tile_0105.png", 2.5)
        self.player.center_x = WIDTH // 2
        self.player.center_y = HEIGHT // 2

        # Criar uma SpriteList para o jogador
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)

    def on_draw(self):
        """Desenha a cena."""
        self.clear()
        with self.camera.activate():
            self.scene.draw()

    def on_key_press(self, key, modifiers):
        """Controla as teclas pressionadas."""
        self.player.on_key_press(key)

    def on_key_release(self, key, modifiers):
        """Controla as teclas soltas."""
        self.player.on_key_release(key)

    def update(self, delta_time):
        """Atualiza a posição do jogador e a câmera."""
        self.scene.update()  # Agora a cena atualiza o player corretamente

        # Calcula o novo centro da câmera baseado na posição do jogador
        target_x = max(self.player.center_x - WIDTH // 2, 0)
        target_y = max(self.player.center_y - HEIGHT // 2, 0)

        # Faz interpolação suave da posição da câmera
        self.camera.position = arcade.math.lerp_2d(self.camera.position, (target_x, target_y), 0.2)

# Rodar o jogo
if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()
