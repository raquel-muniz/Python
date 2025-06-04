"""
Loading screen
"""
import arcade
from pages.draw_bar import draw_bar
from pages.load_game_map import load_maps
from pages.views.battle_view import BattleView
from pages.views.game_view import GameView
from pages.views.inventory_view import InventoryView
from pages.views.main_menu_view import MainMenuView
from pages.views.settings_view import SettingsView


class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        self.progress = 0
        self.map_list = None
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Loading...",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        self.started = True
        draw_bar(
            current_amount=self.progress,
            max_amount=100,
            center_x=self.window.width / 2,
            center_y=20,
            width=self.window.width,
            height=10,
            color_a=arcade.color.BLACK,
            color_b=arcade.color.WHITE,
        )

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        # Dictionary to hold all our maps
        if self.started:
            done, self.progress, self.map_list = load_maps()
            if done:
                self.window.views["game"] = GameView(self.map_list)
                self.window.views["game"].setup()
                self.window.views["inventory"] = InventoryView()
                self.window.views["inventory"].setup()
                self.window.views["main_menu"] = MainMenuView()
                self.window.views["settings"] = SettingsView()
                self.window.views["settings"].setup()
                self.window.views["battle"] = BattleView()
                self.window.views["battle"].setup()

                self.window.show_view(self.window.views["game"])
