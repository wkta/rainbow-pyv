from ... import _hub

pygame = _hub.pygame


def clip(surf, x, y, x_size, y_size):
    # WTF bro? Part of original code commented:
    # handle_surf = surf.copy()
    clip_r = pygame.Rect(x, y, x_size, y_size)
    # handle_surf.set_clip(clipR)
    image = surf.subsurface(clip_r)  # handle_surf.get_clip())

    # pr port ca vers Web Ctx
    # ya donc que 2 operations a emuler convenablement: .subsurface & .copy
    return image.copy()


def swap_color(img, old_c, new_c):
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img, (0, 0))
    return surf


def load_font_img(path, font_color):
    fg_color = (255, 0, 0)
    bg_color = (0, 0, 0)
    font_img = pygame.image.load(path).convert()

    # N.B. theres a BUG when interactin with KataSDK, thats why I have
    # commetend the line below.
    # Hence ktg-webapp does not crash but it cannot swap color.
    # TODO: fix the bug Asap!

    # font_img = swap_color(font_img, fg_color, font_color)
    last_x = 0
    letters = []
    letter_spacing = []
    for x in range(font_img.get_width()):
        colorinfos = font_img.get_at((x, 0))
        if colorinfos[0] == 127:
            tmpw = x - last_x
            tmph = font_img.get_height()
            letters.append([last_x, 0, tmpw, tmph])
            # letters.append(
            #     clip(font_img, last_x, 0, tmpw, tmph)
            # )
            letter_spacing.append(tmpw)
            last_x = x + 1
        x += 1
    #for letter in letters:
    #    letter.set_colorkey(bg_color)
    card_l = len(letters)
    print('*debug ImgBasedText*')
    print(f' ... source={path}')
    print(f' ... num of letters={card_l}')
    print(f' ... letter_spacings {letter_spacing}')
    return letters, letter_spacing, font_img.get_height()


class ImgBasedFont:
    NO_CK_MODE = False  # this is a hotfix for the webctx where on needs to not use colorkey val

    def __init__(self, path, color):
        self._spr_sheet_like = pygame.image.load(path)

        self.letters_rects, self.letter_spacing, self.line_height = load_font_img(path, color)
        self.font_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-',
                           ',', ':', '+', '\'', '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')',
                           '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';', '#', '$', '%', '@', '{', '}', '`',
                           '~']
        self.space_width = self.letter_spacing[self.font_order.index('_')]
        self.base_spacing = 1
        self.line_spacing = 2

    def get_linesize(self):  # stick to pygame interface
        return 11  # TODO implement properly plz! 11 is hardset comes from 11px the PNG height gibson0_font

    def size(self, sample_txt):  # stick to pygame interface
        return self.width(sample_txt), self.get_linesize()

    def width(self, text):
        text_width = 0
        for char in text:
            if char == ' ':
                text_width += self.space_width + self.base_spacing
            else:
                try:
                    idx = self.font_order.index(char)
                except ValueError:
                    # generic char
                    print('cannot comp width for: ', char)
                    idx = self.font_order.index('_')
                text_width += self.letter_spacing[idx] + self.base_spacing

        return text_width

    # --add-on to stick to pygame interface
    def render(self, gtext, antialias, color, bgcolor=None):
        rez = pygame.Surface((self.width(gtext), self.get_linesize()), pygame.SRCALPHA)
        if not self.NO_CK_MODE:
            upink = (255, 0, 255)  # ugly pink
            rez.fill(upink)
        self._xrender(gtext, rez, (0, 0))
        if not self.NO_CK_MODE:
            rez.set_colorkey(upink)
        return rez

    def _xrender(self, text, surf, loc, line_width=0):

        x_offset = 0
        y_offset = 0
        if line_width != 0:
            spaces = []
            x = 0
            for i, char in enumerate(text):
                if char == ' ':
                    spaces.append((x, i))
                    x += self.space_width + self.base_spacing
                else:
                    x += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
            line_offset = 0
            for i, space in enumerate(spaces):
                if (space[0] - line_offset) > line_width:
                    line_offset += spaces[i - 1][0] - line_offset
                    if i != 0:
                        text = text[:spaces[i - 1][1]] + '\n' + text[spaces[i - 1][1] + 1:]

        escaped_chars = ['\n', ' ', '\r']
        for char in text:
            if char not in escaped_chars:
                #surf.blit(self.letters[self.font_order.index(char)], (loc[0] + x_offset, loc[1] + y_offset))
                destpos = (loc[0] + x_offset, loc[1] + y_offset)
                surf.blit(self._spr_sheet_like, destpos, area=self.letters_rects[self.font_order.index(char)] )
                x_offset += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
                continue
            if char == ' ':
                x_offset += self.space_width + self.base_spacing
            elif char == '\n':
                y_offset += self.line_spacing + self.line_height
                x_offset = 0
