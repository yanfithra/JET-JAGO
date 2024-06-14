from ursina import *
import random

FONT = "gui_assets/font/04B.ttf"

app = Ursina()

# Inisialisasi variabel global di luar fungsi
bg = None
misil_list = []
to_destroy = []
game_over = False
game_over_texture = None
game_over_aksi = None
speed = 2
pesawat = None
speed_fly = 2
fly = None
engine_sound = None

def update():
    if game_over:
        return

    global speed, to_destroy

    # Kontrol pesawat
    if held_keys['up arrow']:
        pesawat.y += time.dt * speed
    if held_keys['down arrow']:
        pesawat.y -= time.dt * speed
    if held_keys['left arrow']:
        pesawat.x -= time.dt * speed
    if held_keys['right arrow']:
        pesawat.x += time.dt * speed
    if held_keys['escape']:
        application.quit()
    
    # Gerakan fly
    if fly:
        fly.x -= time.dt * speed_fly
    
        # Jika fly mendekati batas kiri layar
        if fly.x < -8:
            to_destroy.append(fly)
            muncul_fly()

        # Deteksi tabrakan antara misil dan fly
        for misil in misil_list:
            if misil.intersects(fly).hit:
                to_destroy.append(misil)
                misil_list.remove(misil)
                to_destroy.append(fly)
                muncul_fly()

        # Deteksi tabrakan antara pesawat dan fly
        if pesawat.intersects(fly).hit:
            game_over_function()

    # Hapus entitas yang telah ditandai
    for entity in to_destroy:
        destroy(entity)
    to_destroy.clear()

def muncul_fly():
    global fly
    fly = Entity(
        model='quad',
        texture='assets/bee.png',
        position=(8 + random.uniform(0.5, 1.5), random.uniform(-2, 2), 0),
        scale=(1, 1, 1),
        collider='quad'
    )

def game_over_function():
    global game_over
    game_over = True
    game_over_aksi.enabled = True
    engine_sound.stop()

class HomePage(Entity):
    def __init__(self):
        super().__init__()
        
        print("page berhasil tampil")
        self.main_menu = Entity(
            parent=self,
            enabled=True
        )
        
        Entity(
            model='quad',
            parent=self.main_menu,
            position=(0.15, -1, 0.02),
            scale=(200 / 12, 141 / 12),
            texture='assets/BG.png'
        )
        
        Entity(
            model="quad",
            parent=self.main_menu,
            position=(0, 1, 0.01),
            scale=(850 / 100, 800 / 100),
            texture="assets/jj2.png"
        )
        
        self.start_button = Button(
            font = FONT,
            text='START',
            color=color.rgba(1,1,1,0.8),
            scale=(3,1),
            position=(0, -2, 0.01),
            parent=self.main_menu,
            radius=0.40,
            highlight_color= color.rgba(0, 0, 255, 0.62)
        )
        
        self.start_button.text_entity.font = FONT
        self.start_button.text_entity.color = color.rgba(0, 0, 0, 1)
        self.start_button.on_click = self.start_game

    def start_game(self):
        self.main_menu.enabled = False
        initialize_game()

def initialize_game():
    global bg, misil_list, to_destroy, game_over, game_over_texture, game_over_aksi
    global speed, pesawat, speed_fly, fly, engine_sound

    bg = Entity(model='quad', texture='assets/BG.png', scale=20, z=7)
    misil_list = []
    to_destroy = []
    game_over = False
    game_over_texture = 'assets/gover.png'

    game_over_aksi = Entity(
        model='quad',
        texture=game_over_texture,
        position=(0, 0, -0.02),
        scale=(10, 10, 10),
        enabled=False
    )

    speed = 2
    pesawat = Entity(
        model='quad',
        texture='assets/player.png',
        position=(0, 0, 0),
        scale=(2, 2, 2),
        collider='box'
    )

    speed_fly = 2
    fly = Entity(
        model='quad',
        texture='assets/bee.png',
        position=(6 + random.uniform(0.5, 1.5), random.uniform(-2, 2), 0),
        scale=(1, 1, 1),
        collider='quad'
    )

    engine_sound = Audio('assets/engine1.wav', autoplay=True, loop=True)

def input(key):
    if game_over:
        if key == 'escape':
            application.quit()
        return
    
    if key == 'space':
        misil = Entity(
            y=pesawat.y,
            x=pesawat.x + 1,
            model='quad',
            scale=1,
            texture='assets/misil1.png',
            collider='box'
        )
        misil.animate_x(300, duration=50, curve=curve.linear)
        misil_list.append(misil)
        invoke(check_and_destroy_misil, misil, delay=2)
        Audio('assets/efek1.wav', autoplay=True)

def check_and_destroy_misil(misil):
    if misil in misil_list:
        misil_list.remove(misil)
        destroy(misil)

# Menginstansiasi objek dari kelas HomePage
home_page = HomePage()

EditorCamera()

app.run()
