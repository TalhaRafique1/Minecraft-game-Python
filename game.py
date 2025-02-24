from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Load all assets
textures = {
    1: load_texture("Assets/Textures/Grass.png"),
    2: load_texture("Assets/Textures/Dirt.png"),
    3: load_texture("Assets/Textures/Brick.png"),
    4: load_texture("Assets/Textures/Wood.png"),
    5: load_texture("Assets/Textures/Stone.png"),
}

sky_bg = load_texture("Assets/Textures/Sky.png")
build_sound = Audio("Assets/SFX/Build_Sound.wav", loop=False, autoplay=False)

block_pick = 1  # Default block type
blocks = []  # List to keep track of all blocks

class Block(Button):
    def __init__(self, position=(0, 0, 0), texture=textures[1], breakable=True):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Block.obj",
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color=color.light_gray,
            scale=0.5
        )
        self.breakable = breakable
        blocks.append(self)  # Add block to the global list

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                build_sound.play()
                new_block = Block(position=self.position + mouse.normal, texture=textures[block_pick])
            elif key == "right mouse down" and self.breakable:
                build_sound.play()
                blocks.remove(self)  # Remove block from the global list
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=sky_bg,
            scale=150,
            double_sided=True
        )


class Tree(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Lowpoly_tree_sample.obj",
            scale=(0.6, 0.6, 0.6),
            collider="mesh"
        )


def generate_trees(num_trees=3, terrain_size=20):
    for _ in range(num_trees):
        x = random.randint(0, terrain_size - 1)
        z = random.randint(0, terrain_size - 1)
        y = get_terrain_height(x, z)  # Place trees on the terrain surface
        Tree(position=(x, y, z))


def generate_terrain():
    height = 5  # Base height of the terrain
    for z in range(20):
        for x in range(20):
            for y in range(height):
                if y == height - 1:
                    Block(position=(x, y, z), texture=textures[1])  # Grass on top
                elif y >= height - 3:
                    Block(position=(x, y, z), texture=textures[2])  # Dirt below grass
                else:
                    Block(position=(x, y, z), texture=textures[5])  # Stone deeper down

            # Create an unbreakable bedrock layer
            Block(position=(x, -1, z), texture=textures[5], breakable=False)


def get_terrain_height(x, z):
    # Placeholder function to get the terrain height at (x, z)
    # You can replace this with a noise function for more varied terrain
    return 0  # Flat terrain for now


def update():
    global block_pick

    # Change block type with number keys
    for i in range(1, 6):
        if held_keys[str(i)]:
            block_pick = i
            break

    # Quit the game on escape key
    if held_keys["escape"]:
        application.quit()

    # Reset player position if they fall off the map
    if player.y <= -5:
        player.position = (10, 10, 10)


# Initialize the game
player = FirstPersonController(position=(10, 10, 10))
player.cursor.visible = False
sky = Sky()
generate_trees()
generate_terrain()

if __name__ == "__main__":
    app.run()