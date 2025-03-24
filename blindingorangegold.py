##
## this code is extremely ugly, but that seems kind of appropriate
##
##

import pygame as pg
import pygame.freetype
import textwrap
import math
from script import scriptdata, prayscriptdata
import sys, os

os.chdir(sys._MEIPASS)

class Game:
    def __init__(self, script):
        pg.init()
        self.script = script
        self.dialogue_font = pg.freetype.Font('assets/fonts/Freeride.otf', 30)
        self.speaker_font = pg.freetype.Font('assets/fonts/Freeride.otf', 35)
        self.dialogue_box = pg.Surface((0,0))
        self.dialogue_textsfc = pg.Surface((0,0))
        self.dialogue_speaker = pg.Surface((0,0))
        self.dialogue_options = []
        self.outside = False
        self.god_image = pg.image.load("assets/god.png") # idolatry? :p
        self.god_selected_image = pg.image.load("assets/god_selected.png")
        self.other_script = False
        self.prayer_counter = 0
        self.textwidth = 50
    def run(self):
        screen = pg.display.set_mode((640,640))
        clock = pg.time.Clock()
        pg.display.set_caption('blinding orange-gold')
        pg.mixer.music.load('assets/music/thememusic.mp3')
        pg.mixer.music.set_volume(0.05)
        pg.mixer.music.play(-1)
        scene = Scene(self.script.scene_bg, self.script.scene_fg, self.script.scene_pxgetter)
        changed = True
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return True
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_s:
                        # skip to next menu
                        while not isinstance(self.script.current_dialogue, list):
                            try_advance = self.script.advance()
                            if not try_advance:
                                if self.other_script:
                                    self.script = self.other_script
                                    self.other_script = False
                                else:
                                    exit() # done
                            scene.set_bg(self.script.scene_bg)
                            scene.set_fg(self.script.scene_fg)
                            scene.set_pxgetter(self.script.scene_pxgetter)
                            if self.script.settings_change is not None:
                                self.update_settings(self.script.settings_change, scene)
                                self.script.settings_change = None
                        changed = True
                elif event.type == pg.MOUSEBUTTONUP:
                    if self.outside and event.pos[1] < 150 and not self.other_script:
                        self.other_script = self.script
                        self.script = Script(prayscriptdata)
                        self.script.scene_bg = self.other_script.scene_bg
                        self.script.scene_fg = self.other_script.scene_fg
                        self.script.scene_pxgetter = self.other_script.scene_pxgetter
                        self.script.advance()
                        self.prayer_counter += 1
                    elif isinstance(self.script.current_dialogue, list):
                        for i in range(len(self.dialogue_options)):
                            if self.dialogue_options[i][1].collidepoint(event.pos):
                                try_advance = self.script.advance(choice = i)
                                if not try_advance:
                                    if self.other_script:
                                        self.script = self.other_script
                                        self.other_script = False
                                    else:
                                        exit() # done
                    else:
                        try_advance = self.script.advance()
                        if not try_advance:
                            if self.other_script:
                                self.script = self.other_script
                                self.other_script = False
                            else:
                                exit() # done
                    scene.set_bg(self.script.scene_bg)
                    scene.set_fg(self.script.scene_fg)
                    scene.set_pxgetter(self.script.scene_pxgetter)
                    if self.script.settings_change is not None:
                        self.update_settings(self.script.settings_change, scene)
                        self.script.settings_change = None
                    changed = True
            for i in range(5000):
                scene.render_next()
            scene.update_params()
            screen.blit(scene.result_image, (0,0))
            if self.outside:
                if pg.mouse.get_pos()[1] < 150 or self.other_script:
                    screen.blit(self.god_selected_image, (0,0))
                else:
                    screen.blit(self.god_image, (0,0))
            if isinstance(self.script.current_dialogue, list):
                mousepos = pg.mouse.get_pos()
                if changed:
                    self.render_dialogueoptions(screen, self.script)
                for option in self.dialogue_options:
                    screen.blit(option[0], (option[1].x + (20 if option[1].collidepoint(mousepos) else 0), option[1].y))
            else: # if it's a string
                if changed:
                    self.render_dialoguebox(screen, self.script)
                screen.blit(self.dialogue_box, (0, 620-(self.dialogue_speaker.get_rect().h+self.dialogue_textsfc.get_rect().h)))
                screen.blit(self.dialogue_speaker, (10, 625-(self.dialogue_speaker.get_rect().h+self.dialogue_textsfc.get_rect().h)))
                screen.blit(self.dialogue_textsfc, (10, 630-self.dialogue_textsfc.get_rect().h))
            pg.display.flip()
            clock.tick(60)
            changed = False
    def update_settings(self, settings, scene):
        if settings["clearer font"]:
            self.dialogue_font = pg.freetype.Font('assets/fonts/Lexend-VariableFont_wght.ttf', 27)
            self.speaker_font = pg.freetype.Font('assets/fonts/Lexend-VariableFont_wght.ttf', 32)
            self.textwidth = 40
        else:
            self.dialogue_font = pg.freetype.Font('assets/fonts/Freeride.otf', 30)
            self.speaker_font = pg.freetype.Font('assets/fonts/Freeride.otf', 35)
            self.textwidth = 50
        if settings["effects off"]:
            scene.params_scale = 0
        elif settings["low intensity effects"]:
            scene.params_scale = 0.25
        else:
            scene.params_scale = 1
        pg.mixer.music.set_volume(settings["volume"])
        if settings["outside"]:
            self.outside = True
        else:
            self.outside = False
    def render_dialoguebox(self, screen, script):
        self.dialogue_speaker, speaker_rect = self.speaker_font.render(script.current_speaker[0], fgcolor = script.current_speaker[1])
        self.dialogue_textsfc, dia_rect = render_multiline(self.dialogue_font, textwrap.fill(script.current_dialogue, self.textwidth, replace_whitespace=False), (255,255,255))
        self.dialogue_box = pg.Surface((640, speaker_rect.h+dia_rect.h+30))
        self.dialogue_box.fill((0,0,0))
        self.dialogue_box.set_alpha(220)
    def render_dialogueoptions(self, screen, script):
        options = []
        height = 0
        for option in script.current_dialogue:
            new_option, new_option_rect = render_multiline(self.dialogue_font, textwrap.fill(option, self.textwidth-10, replace_whitespace=False), fgcolour=(255,255,255,255))
            new_option_box = pg.Surface((new_option_rect.w + 20, new_option_rect.h + 20))
            new_option_box.set_alpha(220)
            new_option_box.blit(new_option, (10,10))
            height += new_option_rect.h + 20
            options.append([new_option_box, new_option_box.get_rect()])
        position = 320 - int((10*len(options))+(height/2))
        for option, option_rect in options:
            option_rect.x = 320 - int(option_rect.w/2)
            option_rect.y = position
            position += option_rect.h + 20
        self.dialogue_options = options
        
            
        
def render_multiline(font, text, fgcolour=None, bgcolour=None):
    text = text.split('\n')
    lines = []
    for line in text:
        lines.append(font.render(line, fgcolor=fgcolour, bgcolor=bgcolour))
    width = 0
    height = 0
    for line in lines:
        if line[1].w > width:
            width = line[1].w
        height += line[1].h
    bb = pg.Surface((width, height), pg.SRCALPHA)
    cursor = 0
    for line in lines:
        bb.blit(line[0], (0,cursor))
        cursor += line[1].h
    return bb, bb.get_rect()

class Script:
    def __init__(self, scriptgenerator):
        self.scene_bg = "assets/black.png"
        self.scene_fg = "assets/transparent.png"
        self.scene_pxgetter = pixel_getter_passthrough
        self.current_dialogue = ""
        self.current_speaker = ("", (255,255,255))
        self.settings_change = None
        self.scriptgenerator = scriptgenerator()
        self.advance()
    def advance(self, choice = None):
        changes = next(self.scriptgenerator) if choice is None else self.scriptgenerator.send(choice)
        if changes:
            new_dialogue, new_speaker, new_bg, new_fg, new_pxg, new_settings = changes
            if new_settings:
                self.settings_change = new_settings
            if new_bg:
                self.scene_bg = new_bg
            if new_fg:
                self.scene_fg = new_fg
            if new_pxg:
                self.scene_pxgetter = new_pxg
            if new_dialogue:
                self.current_dialogue = new_dialogue
            if new_speaker:
                self.current_speaker = new_speaker
            return True
        else:
            return False # finished script

class Scene:
    def __init__(self, background_image, foreground_image, pixel_getter):
        self.background_image = pg.image.load(background_image).convert_alpha()
        self.foreground_image = pg.image.load(foreground_image).convert_alpha()
        self.pixel_getter = pixel_getter
        self.result_image = pg.Surface((640,640))
        self.x = 0
        self.y = 0
        self.params = [0,0,0]
        self.t = 0
        self.params_scale = 1
    def set_bg(self, bg):
        self.background_image = pg.image.load(bg).convert_alpha()
    def set_fg(self, fg):
        self.foreground_image = pg.image.load(fg).convert_alpha()
    def set_pxgetter(self, pxg):
        self.pixel_getter = pxg
    def render_next(self):
        self.result_image.set_at((self.x, self.y), self.pixel_getter(self.x, self.y, self.background_image, self.foreground_image, self.params))
        self.x += 1
        if self.x >= 640:
            self.x = 0
            self.y += 1
            if self.y >= 640:
                self.y = 0
    def update_params(self):
        for i in range(3):
            self.params[i] = math.sin(self.t/(i+1)) * self.params_scale
        self.t += 1/8
        if self.t >= 6 * math.pi:
            self.t = 0

def pixel_getter_passthrough(x, y, background, foreground, params):
    bg_px = background.get_at((int(x/640) * background.get_rect()[2], int((y/640) * background.get_rect()[3])))
    fg_px = foreground.get_at((int(x/640) * foreground.get_rect()[2], int((y/640) * foreground.get_rect()[3])))
    fg_a = fg_px[3]
    bg_r = bg_px[0]/256
    bg_g = bg_px[1]/256
    bg_b = bg_px[2]/256
    fg_r = fg_px[0]/256
    fg_g = fg_px[1]/256
    fg_b = fg_px[2]/256
    return (int((bg_r * (255-fg_a)) + (fg_r * fg_a)), int((bg_g * (255-fg_a)) + (fg_g * fg_a)), int((bg_b * (255-fg_a)) + (fg_b * fg_a)), 255)

game = Game(Script(scriptdata))
game.run()
