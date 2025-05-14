"""
Script for pre-loading all images used in Ransack
"""
import os

import pyved_engine as pyv

from .spritesheet import spritesheet
from ..UTIL import const, load_image


editorImages = list(range(7))

mHeroImages = list(range(18))
fHeroImages = list(range(18))
accessories = list(range(18))

mapImages = list(range(264))


def preload_all():
    mapSpriteSheet = spritesheet('mastersheet.bmp')
    for i in range(128):
        mapImages[i] = mapSpriteSheet.image_at(((i * const.blocksize) % 240,
                                                (i // 8) * const.blocksize,
                                                const.blocksize,
                                                const.blocksize),
                                               1)

    for i in range(128, 256):
        # print (i*const.blocksize)%240 + 240
        mapImages[i] = mapSpriteSheet.image_at(((i * const.blocksize) % 240 + 240,
                                                ((i - 128) // 8) * const.blocksize,
                                                const.blocksize,
                                                const.blocksize),
                                               1)

    # permet de peupler : mapImages (dans un 1er temps) puis
    # accesories[i], 0<=i<=17
    siteImgs = [
        'itemSh.bmp', 'mShop.bmp', 'bSmith.bmp', 'armry.bmp', 'tavrn.bmp', 'townhall.bmp', 'house1.bmp', 'tower1.bmp'
    ]
    for i in range(256, 264):
        mapImages[i], r = load_image.load_image(os.path.join('EXT', siteImgs[i - 256]), 1)
    for i in range(18):
        accessories[i] = pyv.pygame.Surface((15, 10))
        accessories[i].set_colorkey([255, 128, 128], pyv.pygame.RLEACCEL)
        accessories[i].blit(
            mapImages[242 + int(i / 6)], (((i % 6) / 3) * -15, (i % 3) * -10)
        )

    # permet de peupler : mHeroImages[i ], 0<=i<=17
    mHeroSpriteSheet = spritesheet(os.path.join('CHAR', 'mherosheet.bmp'))
    for i in range(18):
        mHeroImages[i] = mHeroSpriteSheet.image_at(((i * const.blocksize) % 270,
                                                    (i // 8) * const.blocksize,
                                                    const.blocksize,
                                                    const.blocksize), -1)

    # permet de peupler : fHeroImages[i], 0<=i<=17
    fHeroSpriteSheet = spritesheet(os.path.join('CHAR', 'fherosheet.bmp'))
    for i in range(18):
        fHeroImages[i] = fHeroSpriteSheet.image_at(((i * const.blocksize) % 270,
                                                    (i // 8) * const.blocksize,
                                                    const.blocksize,
                                                    const.blocksize), -1)


def load_npc(file):
    npcSS = spritesheet(os.path.join('CHAR', file))
    npcImages = list(range(18))
    for i in range(18):
        npcImages[i] = npcSS.image_at(((i * const.blocksize) % 270,
                                       (i // 8) * const.blocksize,
                                       const.blocksize,
                                       const.blocksize), -1)
    return npcImages
