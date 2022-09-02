import pygame
from encryption_setup import *


class Question:
    def __init__(self, question_text):
        self.prompt, self.a, self.p, self.checktype = str(question_text).split("|")
        if len(self.a) > 0:
            self.answers = str(self.a).split(",")
            self.choices = len(self.answers)
        else:
            self.choices = 0
        if len(self.p) > 0:
            self.points = str(self.p).split(",")


class Checkbox:
    def __init__(self, surface, x, y, chk_size, chk_type, id_num, color=WHITE,
                 caption="", outline_color=BLACK, check_color=BLACK,
                 font_size=48, font_color=LIME_GREEN, font_background_color=DARK_GREY,
                 text_offset=(60, 2), font='fonts/consolas.ttf'):
        self.surface = surface
        self.x = x
        self.y = y
        self.size = chk_size
        self.type = bool(int(chk_type))
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.fbc = font_background_color
        self.to = text_offset
        self.ft = font

        # identification for removal and reorganization
        self.idnum = id_num

        # checkbox objects
        self.checkbox_obj = pygame.Rect(self.x, self.y, self.size, self.size)
        self.radiobutton_outline = pygame.draw.ellipse(self.surface, self.oc, self.checkbox_obj, self.size)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

        print("Class init, check type is: " + str(self.type))

    # render draw checkbox text
    def _draw_button_text(self):
        self.font = pygame.font.Font(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc, self.fbc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + self.size / 2 - h / 2 + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    # render checkbox
    def render_checkbox(self):
        pygame.draw.rect(self.surface, DARK_GREY, self.checkbox_obj)
        if self.type:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        else:
            pygame.draw.ellipse(self.surface, self.color, self.checkbox_obj, self.size)
        if self.checked:
            if self.type:
                pygame.draw.line(self.surface, self.cc, (self.x + 2, self.y + 2),
                                 (self.x + self.size - 4, self.y + self.size - 4), int(self.size/3))
                pygame.draw.line(self.surface, self.cc, (self.x + 2, self.y + self.size - 4),
                                 (self.x + self.size - 4, self.y + 2), int(self.size/3))
            else:
                pygame.draw.circle(self.surface, self.cc, (self.x + self.size/2, self.y + self.size/2),
                                   self.size/2 - 2)
        self._draw_button_text()

    # update checkbox based on mouse over and click
    def _update(self):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            # print("box click on box #" + str(self.idnum))
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    # handle checkbox click (mouse down event)
    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            # self.checked = True
            self._update()


def get_agent_file(filename):
    agentFile = open(filename, 'r')
    data = agentFile.read()
    agentFile.close()
    cleanData = '\n'.join(data.split('\n', 4)[:-1])
    name, age, secret, hacked = cleanData.split("\n")
    return name, age, secret, hacked


def write_agent_file(filename, name, age, secret, hack, index):
    agentFile = open(filename, 'w')
    agentFile.write(name + '\n')
    agentFile.write(age + '\n')
    agentFile.write(secret + '\n')
    if index > 0:
        h = list(hack)
        s = list(secret)
        h[index - 1] = s[index - 1]
        hacked = ''.join(h)
    else:
        hacked = hack
    agentFile.write(hacked + '\n')
    agentFile.close()


def show_agent_record(name, age, secret, hacked):
    print("Agent: " + str(name))
    print("Age: " + str(age))
    print("Secret: " + str(secret))
    print("Hacked: " + str(hacked))


def get_agent_level(age):
    print("Agent age is: " + str(age))
    if int(age) < 8:
        level = 1
    elif int(age) < 13:
        level = 2
    else:
        level = 3
    return level


def parse_agent_content(inText, name, age, password):
    stripText = inText.rstrip('\n')
    tempText = stripText.replace('<agent_name>', name)
    tempText = tempText.replace('<password>', password)
    outText = tempText.replace('<age>', age)
    return outText
