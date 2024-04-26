from pygame import mixer

# Sounds
mixer.init()
mixer.music.load('audio/ufo.wav')

all_sfx: dict[str, mixer.Sound] = {
    'alien_explode': mixer.Sound('audio/alien_explode.wav'),
    'ship_explode': mixer.Sound('audio/ship_explode.wav'),
    'shoot_laser': mixer.Sound('audio/shoot_laser.wav'),
    'alien_1': mixer.Sound('audio/alien_1.wav'),
    'alien_2': mixer.Sound('audio/alien_2.wav'),
    'alien_3': mixer.Sound('audio/alien_3.wav'),
    'alien_4': mixer.Sound('audio/alien_4.wav')
}


def play_sound(sfx: str):
    sound = all_sfx[sfx]
    sound.play()


def play_ufo_sound(on: bool = True):
    if on:
        mixer.music.play(-1)
    else:
        mixer.music.stop()
