#!/usr/bin/env python3
from solid import *
from solid.utils import *
import pathlib
import math
from consts import *

SHOW_PARTS = False
# SHOW_PARTS = True

use("clips.scad")
use("mini-outlines-small.scad")
use("mini-outlines-large.scad")
use("MCAD/boxes.scad")

TOTAL_H = LOWER_TRAY_H

MINI_TRAY_H = 12
MINI_PEG_CORNERS = [(5, 5), (195, 5), (195, 195)]
MINI_CLIP_LOCATIONS = [
    (100, CLIP_SOCKET_WALL + CLIP_SOCKET / 2, 0),
    (CLIP_SOCKET_WALL + CLIP_SOCKET / 2, 90, 90),
    (100, 200 - CLIP_SOCKET_WALL - CLIP_SOCKET / 2, 0),
]

Y_OFFSETS_50MM = [70 + 50 / 2, 8 + 50 / 2]
X_OFFSETS_50MM = [5 + 50 / 2, 83 + 50 / 2]


def objsum(objs):
    ret = objs[0]
    for o in objs[1:]:
        ret += o
    return ret


def bases():
    ret = []
    for x, y, _ in OFFSETS_25mm:
        b = translate([x, y, 0])(cylinder(h=TOTAL_H + 6, d=26)).set_modifier("")
        b += translate([x, y, BASE_H])(cylinder(h=TOTAL_H + 6, d=26 + 2))
        # fingergrab(17)
        ret.append(b)

    for x, y, _ in OFFSETS_20mm:
        b += translate([x, y, 0])(cylinder(h=TOTAL_H + 6, d=21))
        b += translate([x, y, BASE_H])(cylinder(h=TOTAL_H + 6, d=21 + 2))
        # fingersize = 30*4+20;
        # translate([-fingersize/2+30, y, -BASE_H]) fingergrab(12, fingersize);
        ret.append(b)

    return objsum(ret).set_modifier("")


def spiderstands():
    slot = up(FLOOR + 26 / 2)(rotate([0, 90, 0])(cylinder(d=26, h=7.5)))
    # cutout form about 1/3 of the way up
    slot += translate([0, -26 / 2, FLOOR + 26 / 3])(cube([9, 26, TOTAL_H]))

    spacing = 9 + 3
    cutouts = []
    for i in range(3):
        x = 128 + spacing * i
        cutouts.append(translate([x, 5 + 26 / 2, 0])(slot))
    return objsum(cutouts).set_modifier("")


def spidertext():
    t = translate([128, 37.5, MINI_TRAY_H - 0.4])(
        linear_extrude(1)(
            text("Spider", size=3, font="Arial:style=Bold", halign="left")
        )
    )
    t += translate([128, 33, MINI_TRAY_H - 0.4])(
        linear_extrude(1)(
            text("Swarms", size=3, font="Arial:style=Bold", halign="left")
        )
    )
    return t.set_modifier("")


def small_minis_tray_obj(h=TOTAL_H, outlineonly=False):
    cutouts = []
    if not outlineonly:
        cutouts.append(spiderstands())
        cutouts.append(up(FLOOR)(bases()))
        cutouts.append(translate([100, 100, BASE_H + FLOOR])(mini_outlines_small(50)))

    # Cut out for upper tray, extend at edges to leave a square edge
    cutouts.append(
        translate([-10, -10, H_FOR_BIG_TRAY])(
            roundedCube([BIG_TRAY_W + 10, BIG_TRAY_D + 10, TOTAL_H], 5, True)
        )
    )

    d = difference()(roundedCube([200, 200, h], 5, True), *cutouts)

    # // Corner peg to hold upper tray
    # translate([-100+5, -100+5, H_FOR_BIG_TRAY-FLOOR-BASE_H]) #union() {
    #     cylinder(d=5, h=3);
    #     translate([0, 0, 3]) sphere(d=5);
    # }
    return d


def gentxt(txt):
    """Generates the object(s) for the given text, up to 3 lines
    """
    LINE_H = 4
    parts = txt.split("\n")
    t = []
    if len(parts) == 1:
        offsets = [0]
    elif len(parts) == 2:
        offsets = [-LINE_H / 2, LINE_H / 2]
    else:
        offsets = [-LINE_H, 0, LINE_H]
    for part in parts:
        t.append(
            translate([0, offsets.pop(), 0])(
                linear_extrude(1)(
                    text(
                        part,
                        size=3,
                        font="Arial:style=Bold",
                        halign="center",
                        valign="center",
                    )
                )
            )
        )
    return objsum(t)


def lower_small_minis_tray(outlineonly=False):
    d = small_minis_tray_obj(MINI_TRAY_H, outlineonly)
    cutouts = []
    for x, y, rot in MINI_CLIP_LOCATIONS:
        cutouts.append(
            translate([x, y, MINI_TRAY_H])(rotate([0, 0, rot])(clipsocket()))
        )
    # Add the text and put in some clip sockets to allow holding on the top if desired
    if not outlineonly:
        for x, y, txt in OFFSETS_25mm:
            cutouts.append(translate([x, y, FLOOR - TEXT_D])(gentxt(txt)))

        for x, y, txt in OFFSETS_20mm:
            cutouts.append(translate([x, y, FLOOR - TEXT_D])(gentxt(txt)))
        cutouts.append(spidertext())
    d = difference()(d, *cutouts)
    # Add a peg in each corner to align things
    for x, y in MINI_PEG_CORNERS:
        d += translate([x, y, MINI_TRAY_H])(peg())

    return d


def upper_small_minis_tray(outlineonly=False):
    d = small_minis_tray_obj(TOTAL_H, outlineonly)
    d -= translate([-1, -1, -1])(cube([200 + 2, 200 + 2, MINI_TRAY_H + 1]))

    # Put in some clip sockets to allow holding on the top if desired
    cutouts = []
    for x, y, rot in MINI_CLIP_LOCATIONS:
        cutouts.append(
            translate([x, y, MINI_TRAY_H])(rotate([180, 0, rot])(clipsocket()))
        )
    # A connector slot to allow connecting the Round tokens tray
    cutouts.append(
        translate(
            [
                CARD_EDGE_WALL + 10,
                LOWER_TRAY_D - CLIP_SOCKET_WALL - CLIP_SOCKET / 2,
                TOTAL_H,
            ]
        )(rotate([0, 0, 0])(clipsocket()))
    )
    cutouts.append(
        translate(
            [
                ROUND_TOKEN_BOX_W - CARD_EDGE_WALL - 10,
                LOWER_TRAY_D - CLIP_SOCKET_WALL - CLIP_SOCKET / 2,
                TOTAL_H,
            ]
        )(rotate([0, 0, 0])(clipsocket()))
    )
    # Connectors for Cavern Edge Tiles
    cutouts.append(
        translate(
            [
                LOWER_TRAY_W - CAVERN_EDGE_BOX_D / 2,
                CLIP_SOCKET_WALL + CLIP_SOCKET / 2,
                TOTAL_H,
            ]
        )(rotate([0, 0, 0])(clipsocket()))
    )

    d = difference()(d, *cutouts)
    # Add a peg hole in each corner to align things
    for x, y in MINI_PEG_CORNERS:
        d -= translate([x, y, MINI_TRAY_H])(peghole())

    # And a peg for the upper tray
    d += translate([5, 5, H_FOR_BIG_TRAY])(peg())

    return d


def bases_50mm():
    ret = []
    fingerd = 31
    for y, yi in zip(Y_OFFSETS_50MM, range(2)):
        for x, xi in zip(X_OFFSETS_50MM, range(2)):
            ret.append(translate([x, y, 0])(cylinder(h=UPPER_TRAY_H + 6, d=50)))
            ret.append(
                translate([x, y, BASE_H])(cylinder(h=UPPER_TRAY_H + 6, d=50 + 2))
            )
            if (xi, yi) == (0, 0):
                txt = "Dinin Do'urden"
            elif (xi, yi) == (1, 0):
                txt = "Shimmergloom"
            else:
                txt = "Feral Troll"
            ret.append(
                translate([x, y, -TEXT_D])(
                    linear_extrude(TEXT_D * 2)(
                        text(txt, size=4, halign="center", valign="center")
                    )
                )
            )

        ret.append(
            translate([0, y, UPPER_TRAY_H / 3])(
                rotate([90, 0, 90])(
                    linear_extrude(UPPER_TRAY_W)(
                        translate([0, fingerd / 2, 0])(circle(d=fingerd))
                        + translate([-fingerd / 2, +fingerd / 2, 0])(
                            square([fingerd, UPPER_TRAY_H], center=False)
                        )
                    )
                )
            )
        )
    return up(FLOOR)(union()(*ret))


def large_minis_tray(outlineonly=False):
    cutouts = []
    if not outlineonly:
        cutouts.append(bases_50mm())
        cutouts.append(
            translate([UPPER_TRAY_W / 2, UPPER_TRAY_D / 2, BASE_H])(
                mini_outlines_large(UPPER_TRAY_H)
            )
        )
    cutouts.append(translate([UPPER_TRAY_W - 5, UPPER_TRAY_D - 5, 0])(peghole()))
    cutouts.append(
        translate([UPPER_TRAY_W - 5, UPPER_TRAY_D - 5, UPPER_TRAY_H])(pegident())
    )
    # Main cube is build in 2 parts to allow one side (opposite Shimmergoolm) to be a
    # touch lower so there is room for the manuals.

    thecube = intersection()(
        (
            right(UPPER_TRAY_W / 2)(
                roundedCube([UPPER_TRAY_W / 2, UPPER_TRAY_D, UPPER_TRAY_H], 2, False)
            )
            + roundedCube(
                [UPPER_TRAY_W, UPPER_TRAY_D, UPPER_TRAY_H - MANUAL_THICKNESS], 2, False
            )
        ),
        roundedCube([UPPER_TRAY_W, UPPER_TRAY_D, UPPER_TRAY_H], 5, True),
    )
    d = difference()(thecube, *cutouts)
    return up(H_FOR_BIG_TRAY)(d)


def clipsocket():
    return translate([0, (CLIP_SOCKET / 2), 0.001])(
        rotate([90, 180, 0])(socket(CLIP_SOCKET))
    )


def cards_box():
    d = card_box_obj(CARD_BOX_H)
    if SHOW_PARTS:
        d += translate([CARD_EDGE_WALL, CARD_WALL + 2, CARD_EDGE_WALL])(
            cards_stack()
        ).set_modifier("%")
    # if (withlid) {
    #     %translate([CARD_BOX_W, 0, CARD_BOX_H+CARD_BOX_LID_H]) rotate([0, 180, 0]) card_box_lid();
    return d


def cards_box_lid():
    d = card_box_obj(CARD_BOX_LID_H)
    t = translate([CARD_BOX_W / 2, CARD_BOX_D / 2, -0.1])(
        mirror([1, 0, 0])(
            linear_extrude(TEXT_D + 0.1)(
                text(
                    "CARDS",
                    size=7,
                    font="Arial:style=Bold",
                    halign="center",
                    valign="center",
                )
            )
        )
    )
    return d - t


def card_box_obj(h):
    d = difference()(
        roundedCube([CARD_BOX_W, CARD_BOX_D, h], 5, True),
        translate([CARD_EDGE_WALL, CARD_WALL, CARD_WALL])(
            roundedCube(
                [CARD_BOX_W - CARD_EDGE_WALL * 2, CARD_BOX_D - CARD_WALL * 2, h],
                2,
                True,
            )
        ),
    )
    # //#translate([CARD_WALL, 2*SMALL_TERRAIN_TILES+CARD_WALL, 0]) rotate([90, 0, 0]) small_terrain_tile(SMALL_TERRAIN_TILES);
    for x in [0, 1]:
        offset = x * (CARD_BOX_W - CARD_EDGE_WALL)
        d -= translate(
            [CLIP_SOCKET_WALL + CLIP_SOCKET / 2 + offset, CARD_BOX_D / 2, h]
        )(rotate([0, 0, 90])(clipsocket()))
    return d


def cards_stack():
    return cube([CARD_W, CARD_STACK, CARD_D])


def large_terrain_tiles_vertical():
    d = difference()(
        roundedCube(
            [LARGE_TERRAIN_BOX_W, LARGE_TERRAIN_BOX_D, LARGE_TERRAIN_BOX_H], 5, True
        ),
        translate([CARD_WALL, CARD_WALL, TERRAIN_TAB_W])(
            roundedCube(
                [
                    LARGE_TERRAIN_BOX_W - CARD_WALL * 2,
                    LARGE_TERRAIN_BOX_D - CARD_WALL * 2,
                    LARGE_TERRAIN_BOX_H,
                ],
                1,
                True,
            )
        ),
        translate([TERRAIN_V_SUPPORT_W + CARD_WALL, CARD_WALL, -0.1])(
            cube(
                [
                    LARGE_TERRAIN_BOX_W - TERRAIN_V_SUPPORT_W * 2 - CARD_WALL * 2,
                    LARGE_TERRAIN_BOX_D - CARD_WALL * 2,
                    LARGE_TERRAIN_BOX_H,
                ]
            )
        ),
    )
    if SHOW_PARTS:
        d += translate([CARD_WALL, CARD_WALL, 0])(
            large_terrain_tile(LARGE_TERRAIN_TILE_COUNT)
        )
    return d


def large_terrain_tile(count):
    tiles = []
    for i in range(count):
        if i % 2 == 1:
            tcolor = "blue"
        else:
            tcolor = "red"
        tiles.append(
            color(tcolor)(
                translate([109, TOKEN_THICK * i, 58])(
                    rotate([0, 90, 90])(
                        (
                            linear_extrude(TOKEN_THICK)(
                                polygon(LARGE_TERRAIN_TILE_POINTS)
                            )
                        )
                    )
                )
            )
        )
    return objsum(tiles)


def small_terrain_tiles_vertical():
    d = difference()(
        roundedCube(
            [SMALL_TERRAIN_BOX_W, SMALL_TERRAIN_BOX_D, SMALL_TERRAIN_BOX_H], 5, True
        ),
        translate([CARD_WALL, CARD_WALL, TERRAIN_TAB_W])(
            roundedCube(
                [
                    SMALL_TERRAIN_BOX_W - CARD_WALL * 2,
                    SMALL_TERRAIN_BOX_D - CARD_WALL * 2,
                    SMALL_TERRAIN_BOX_H,
                ],
                1,
                True,
            )
        ),
        translate([TERRAIN_V_SUPPORT_W + CARD_WALL, CARD_WALL, -0.1])(
            cube(
                [
                    SMALL_TERRAIN_BOX_W - TERRAIN_V_SUPPORT_W * 2 - CARD_WALL * 2,
                    SMALL_TERRAIN_BOX_D - CARD_WALL * 2,
                    SMALL_TERRAIN_BOX_H,
                ]
            )
        ),
    )
    # //#translate([CARD_WALL, 2*SMALL_TERRAIN_TILES+CARD_WALL, 0]) rotate([90, 0, 0]) small_terrain_tile(SMALL_TERRAIN_TILES);
    if SHOW_PARTS:
        d += translate([CARD_WALL, CARD_WALL, 0])(
            small_terrain_tile(SMALL_TERRAIN_TILE_COUNT)
        )
    return d


def small_terrain_tile(count):
    tiles = []
    for i in range(count):
        if i % 2 == 1:
            tcolor = "blue"
        else:
            tcolor = "red"
        tiles.append(
            color(tcolor)(
                translate([58, TOKEN_THICK * i, 58])(
                    rotate([0, 90, 90])(
                        (
                            linear_extrude(TOKEN_THICK)(
                                polygon(SMALL_TERRAIN_TILE_POINTS)
                            )
                        )
                    )
                )
            )
        )
    return objsum(tiles)


def cavern_edge_tiles():
    cutouts = [
        translate([CARD_EDGE_WALL, CARD_WALL, TERRAIN_TAB_W])(
            roundedCube(
                [
                    CAVERN_EDGE_BOX_W - CARD_EDGE_WALL * 2,
                    CAVERN_EDGE_BOX_D - CARD_WALL * 2,
                    CAVERN_EDGE_BOX_H,
                ],
                2,
                True,
            )
        ),
        translate([TERRAIN_V_SUPPORT_W + CARD_WALL, CARD_WALL, -0.1])(
            cube(
                [
                    CAVERN_EDGE_BOX_W - TERRAIN_V_SUPPORT_W * 2 - CARD_WALL * 2,
                    CAVERN_EDGE_BOX_D - CARD_WALL * 2,
                    CAVERN_EDGE_BOX_H,
                ]
            )
        ),
    ]

    # Clip sockets
    cutouts.append(
        translate(
            [
                CLIP_SOCKET_WALL + CLIP_SOCKET / 2,
                CAVERN_EDGE_BOX_D / 2,
                CAVERN_EDGE_BOX_H,
            ]
        )(rotate([0, 0, 90])(clipsocket()))
    )
    cutouts.append(
        translate(
            [
                CAVERN_EDGE_BOX_W - CLIP_SOCKET_WALL - CLIP_SOCKET / 2,
                CAVERN_EDGE_BOX_D / 2,
                CAVERN_EDGE_BOX_H,
            ]
        )(rotate([0, 0, 90])(clipsocket()))
    )
    cutouts.append(
        translate([CLIP_SOCKET_WALL + CLIP_SOCKET / 2, CAVERN_EDGE_BOX_D / 2, 0])(
            rotate([0, 180, 90])(clipsocket())
        )
    )

    d = difference()(
        roundedCube([CAVERN_EDGE_BOX_W, CAVERN_EDGE_BOX_D, CAVERN_EDGE_BOX_H], 5, True),
        *cutouts,
    )
    # //#translate([CARD_WALL, 2*CAVERN_EDGE_TILES+CARD_WALL, 0]) rotate([90, 0, 0]) CAVERN_EDGE_tile(CAVERN_EDGE_TILES);
    if SHOW_PARTS:
        d += translate([CARD_WALL, CARD_WALL, 0])(
            cavern_edge_tile(CAVERN_EDGE_TILE_COUNT)
        )
    return d


def cavern_edge_tiles_lid():
    h = CAVERN_EDGE_BOX_H + FLOOR
    cutouts = [
        translate([CARD_EDGE_WALL, CARD_WALL, FLOOR])(
            roundedCube(
                [
                    CAVERN_EDGE_BOX_W - CARD_EDGE_WALL * 2,
                    CAVERN_EDGE_BOX_D - CARD_WALL * 2,
                    h,
                ],
                2,
                True,
            )
        )
    ]

    # Clip sockets
    cutouts.append(
        translate([CLIP_SOCKET_WALL + CLIP_SOCKET / 2, CAVERN_EDGE_BOX_D / 2, h])(
            rotate([0, 0, 90])(clipsocket())
        )
    )
    cutouts.append(
        translate(
            [
                CAVERN_EDGE_BOX_W - CLIP_SOCKET_WALL - CLIP_SOCKET / 2,
                CAVERN_EDGE_BOX_D / 2,
                h,
            ]
        )(rotate([0, 0, 90])(clipsocket()))
    )
    cutouts.append(
        translate([CAVERN_EDGE_BOX_W / 2, CAVERN_EDGE_BOX_D / 2, -0.1])(
            mirror([1, 0, 0])(
                linear_extrude(TEXT_D + 0.1)(
                    text(
                        "CAVERN EDGE TILES",
                        size=7,
                        font="Arial:style=Bold",
                        halign="center",
                        valign="center",
                    )
                )
            )
        )
    )
    # "Finger" hole for removing the lid
    cutouts.append(
        translate([CAVERN_EDGE_BOX_W / 2, CAVERN_EDGE_BOX_D + 0.1, h])(
            rotate([90, 0, 0])(cylinder(d=25, h=CAVERN_EDGE_BOX_D + 1))
        )
    )
    d = difference()(
        roundedCube([CAVERN_EDGE_BOX_W, CAVERN_EDGE_BOX_D, h], 5, True), *cutouts
    )
    return d


def cavern_edge_tile(count):
    tiles = []
    for i in range(count):
        if i % 2 == 1:
            tcolor = "blue"
        else:
            tcolor = "red"
        tiles.append(
            color(tcolor)(
                translate([50 + 2, TOKEN_THICK * i, 22])(
                    rotate([0, 90, 90])(
                        (linear_extrude(TOKEN_THICK)(polygon(CAVERN_EDGE_TILE_POINTS)))
                    )
                )
            )
        )
    return objsum(tiles)


def round_token_tile(count):
    tiles = []
    for i in range(count):
        if i % 2 == 1:
            tcolor = "blue"
        else:
            tcolor = "red"
        tiles.append(
            right(i * TOKEN_THICK)(
                color(tcolor)(
                    rotate([0, 90, 0])((cylinder(d=ROUND_TOKEN_DIA, h=TOKEN_THICK)))
                )
            )
        )
    return objsum(tiles)


def time_token_stack(count):
    tiles = []
    for i in range(count):
        if i % 2 == 1:
            tcolor = "blue"
        else:
            tcolor = "red"
        tiles.append(
            up(i * TOKEN_THICK)(
                color(tcolor)(linear_extrude(TOKEN_THICK)(polygon(TIME_TOKEN_POINTS)))
            )
        )
    return objsum(tiles)


def round_tokens_tray():
    def gencutout(count):
        return rotate([0, 90, 0])(
            cylinder(d=ROUND_TOKEN_DIA, h=(count + 1) * TOKEN_THICK)
        )

    centertoedge = (ROUND_TOKEN_BOX_D - CARD_EDGE_WALL * 2) / 4 + CARD_EDGE_WALL
    halfd = ROUND_TOKEN_DIA / 2
    cutouts = []
    parts = []
    secondstack = (8 + 1) * TOKEN_THICK
    thirdstack = secondstack + (7 + 1) * TOKEN_THICK

    rtokens = []
    # Strike tokens
    rtokens.append(
        ([CARD_WALL, centertoedge, FLOOR + halfd], ROUND_TOKEN_STRIKE_COUNT, "STRIKE")
    )

    # Other Round tokens
    rtokens.append(
        (
            [CARD_WALL + TOKEN_SPACING + secondstack, centertoedge, FLOOR + halfd],
            ROUND_TOKEN_OTHER_COUNT,
            "MISC",
        )
    )

    # Hero tokens
    rtokens.append(
        (
            [CARD_WALL, ROUND_TOKEN_BOX_D - centertoedge, FLOOR + halfd],
            ROUND_TOKEN_HERO_COUNT,
            "HERO",
        )
    )

    # Item tokens
    rtokens.append(
        (
            [
                CARD_WALL + TOKEN_SPACING + secondstack,
                ROUND_TOKEN_BOX_D - centertoedge,
                FLOOR + halfd,
            ],
            ROUND_TOKEN_ITEM_COUNT,
            "ITEM",
        )
    )

    for tokenpos, tokencount, txt in rtokens:
        cutouts.append(translate(tokenpos)(gencutout(tokencount)))
        txtpos = [
            tokenpos[0] + ((tokencount + 1) * TOKEN_THICK) / 2,
            tokenpos[1],
            FLOOR - TEXT_D,
        ]
        cutouts.append(
            translate(txtpos)(
                linear_extrude(TEXT_D + 5.1)(
                    text(
                        txt,
                        size=3,
                        font="Arial:style=Bold",
                        halign="center",
                        valign="center",
                    )
                )
            )
        )
        if SHOW_PARTS:
            parts.append(translate(tokenpos)(round_token_tile(tokencount)))

    # Time Tokens
    cutouts.append(
        translate(
            [
                CARD_WALL + TOKEN_SPACING * 2 + thirdstack,
                (ROUND_TOKEN_BOX_D - TIME_TOKEN_W) / 2,
                ROUND_TOKEN_BOX_H - TIME_TOKEN_H / 2,
            ]
        )(cube([(TIME_TOKEN_COUNT + 1) * TOKEN_THICK, TIME_TOKEN_W, TIME_TOKEN_H]))
    )
    cutouts.append(
        translate(
            [
                CARD_WALL
                + TOKEN_SPACING * 2
                + thirdstack
                + ((TIME_TOKEN_COUNT + 1) * TOKEN_THICK) / 2,
                (ROUND_TOKEN_BOX_D - TIME_TOKEN_W) / 2 + TIME_TOKEN_W / 2,
                ROUND_TOKEN_BOX_H - TIME_TOKEN_H / 2 - TEXT_D,
            ]
        )(
            rotate([0, 0, 90])(
                linear_extrude(TEXT_D + 0.1)(
                    text(
                        "TIME TOKENS",
                        size=3,
                        font="Arial:style=Bold",
                        halign="center",
                        valign="center",
                    )
                )
            )
        )
    )

    if SHOW_PARTS:
        parts.append(
            translate(
                [
                    CARD_WALL + TOKEN_SPACING * 2 + thirdstack,
                    (ROUND_TOKEN_BOX_D - TIME_TOKEN_W) / 2,
                    ROUND_TOKEN_BOX_H - TIME_TOKEN_H / 2,
                ]
            )(rotate([90, 0, 90])(time_token_stack(TIME_TOKEN_COUNT)))
        )

    # Clip sockets
    cutouts.append(
        translate(
            [
                ROUND_TOKEN_BOX_W / 2,
                CLIP_SOCKET_WALL + CLIP_SOCKET / 2,
                ROUND_TOKEN_BOX_H + 0.001,
            ]
        )(clipsocket())
    )
    cutouts.append(
        translate(
            [
                ROUND_TOKEN_BOX_W / 2,
                ROUND_TOKEN_BOX_D - (CLIP_SOCKET_WALL + CLIP_SOCKET / 2),
                ROUND_TOKEN_BOX_H + 0.001,
            ]
        )(clipsocket())
    )
    cutouts.append(
        translate(
            [
                CARD_EDGE_WALL + 10,
                ROUND_TOKEN_BOX_D - CLIP_SOCKET_WALL - CLIP_SOCKET / 2,
                0,
            ]
        )(rotate([180, 0, 0])(clipsocket()))
    )
    cutouts.append(
        translate(
            [
                ROUND_TOKEN_BOX_W - CARD_EDGE_WALL - 10,
                ROUND_TOKEN_BOX_D - CLIP_SOCKET_WALL - CLIP_SOCKET / 2,
                0,
            ]
        )(rotate([180, 0, 0])(clipsocket()))
    )

    d = difference()(
        roundedCube([ROUND_TOKEN_BOX_W, ROUND_TOKEN_BOX_D, ROUND_TOKEN_BOX_H], 5, True),
        *cutouts,
    )
    d = objsum([d] + parts)

    return d


def round_tokens_tray_lid():
    cutouts = [
        translate([CARD_WALL, CARD_EDGE_WALL, FLOOR])(
            roundedCube(
                [
                    ROUND_TOKEN_BOX_W - CARD_WALL * 2,
                    ROUND_TOKEN_BOX_D - CARD_EDGE_WALL * 2,
                    ROUND_TOKEN_BOX_H,
                ],
                5,
                True,
            )
        )
    ]
    # Clip sockets
    cutouts.append(
        translate(
            [
                ROUND_TOKEN_BOX_W / 2,
                CLIP_SOCKET_WALL + CLIP_SOCKET / 2,
                ROUND_TOKEN_BOX_H + 0.001,
            ]
        )(clipsocket())
    )
    cutouts.append(
        translate(
            [
                ROUND_TOKEN_BOX_W / 2,
                ROUND_TOKEN_BOX_D - (CLIP_SOCKET_WALL + CLIP_SOCKET / 2),
                ROUND_TOKEN_BOX_H + 0.001,
            ]
        )(clipsocket())
    )

    cutouts.append(
        translate([-0.1, ROUND_TOKEN_BOX_D / 2, ROUND_TOKEN_BOX_H])(
            rotate([0, 90, 0])(cylinder(d=20, h=ROUND_TOKEN_BOX_W + 1))
        )
    )

    cutouts.append(
        translate([ROUND_TOKEN_BOX_W / 2, ROUND_TOKEN_BOX_D / 2 + 5, -0.1])(
            mirror([1, 0, 0])(
                linear_extrude(TEXT_D + 0.1)(
                    text(
                        "ROUND &",
                        size=7,
                        font="Arial:style=Bold",
                        halign="center",
                        valign="center",
                    )
                )
            )
        )
    )
    cutouts.append(
        translate([ROUND_TOKEN_BOX_W / 2, ROUND_TOKEN_BOX_D / 2 - 5, -0.1])(
            mirror([1, 0, 0])(
                linear_extrude(TEXT_D + 0.1)(
                    text(
                        "TIME TOKENS",
                        size=7,
                        font="Arial:style=Bold",
                        halign="center",
                        valign="center",
                    )
                )
            )
        )
    )
    d = difference()(
        roundedCube([ROUND_TOKEN_BOX_W, ROUND_TOKEN_BOX_D, ROUND_TOKEN_BOX_H], 5, True),
        *cutouts,
    )
    return d

    def gencutout(count):
        return rotate([0, 90, 0])(
            cylinder(d=ROUND_TOKEN_DIA, h=(count + 1) * TOKEN_THICK)
        )

    centertoedge = (ROUND_TOKEN_BOX_D - CARD_EDGE_WALL * 2) / 4 + CARD_EDGE_WALL
    halfd = ROUND_TOKEN_DIA / 2
    cutouts = []
    parts = []
    secondstack = (8 + 1) * TOKEN_THICK
    thirdstack = secondstack + (7 + 1) * TOKEN_THICK

    rtokens = []
    # Strike tokens
    rtokens.append(
        ([CARD_WALL, centertoedge, FLOOR + halfd], ROUND_TOKEN_STRIKE_COUNT, "STRIKE")
    )

    # Other Round tokens
    rtokens.append(
        (
            [CARD_WALL + TOKEN_SPACING + secondstack, centertoedge, FLOOR + halfd],
            ROUND_TOKEN_OTHER_COUNT,
            "MISC",
        )
    )

    # Hero tokens
    rtokens.append(
        (
            [CARD_WALL, ROUND_TOKEN_BOX_D - centertoedge, FLOOR + halfd],
            ROUND_TOKEN_HERO_COUNT,
            "HERO",
        )
    )

    # Item tokens
    rtokens.append(
        (
            [
                CARD_WALL + TOKEN_SPACING + secondstack,
                ROUND_TOKEN_BOX_D - centertoedge,
                FLOOR + halfd,
            ],
            ROUND_TOKEN_ITEM_COUNT,
            "ITEM",
        )
    )

    for tokenpos, tokencount, txt in rtokens:
        cutouts.append(translate(tokenpos)(gencutout(tokencount)))
        txtpos = [
            tokenpos[0] + ((tokencount + 1) * TOKEN_THICK) / 2,
            tokenpos[1],
            FLOOR - TEXT_D,
        ]
        cutouts.append(
            translate(txtpos)(
                linear_extrude(TEXT_D + 5.1)(
                    text(
                        txt,
                        size=3,
                        font="Arial:style=Bold",
                        halign="center",
                        valign="center",
                    )
                )
            )
        )
        if SHOW_PARTS:
            parts.append(translate(tokenpos)(round_token_tile(tokencount)))

    # Time Tokens
    cutouts.append(
        translate(
            [
                CARD_WALL + TOKEN_SPACING * 2 + thirdstack,
                (ROUND_TOKEN_BOX_D - TIME_TOKEN_W) / 2,
                ROUND_TOKEN_BOX_H - TIME_TOKEN_H / 2,
            ]
        )(cube([(TIME_TOKEN_COUNT + 1) * TOKEN_THICK, TIME_TOKEN_W, TIME_TOKEN_H]))
    )
    cutouts.append(
        translate(
            [
                CARD_WALL
                + TOKEN_SPACING * 2
                + thirdstack
                + ((TIME_TOKEN_COUNT + 1) * TOKEN_THICK) / 2,
                (ROUND_TOKEN_BOX_D - TIME_TOKEN_W) / 2 + TIME_TOKEN_W / 2,
                ROUND_TOKEN_BOX_H - TIME_TOKEN_H / 2 - TEXT_D,
            ]
        )(
            rotate([0, 0, 90])(
                linear_extrude(TEXT_D + 0.1)(
                    text(
                        "TIME TOKENS",
                        size=3,
                        font="Arial:style=Bold",
                        halign="center",
                        valign="center",
                    )
                )
            )
        )
    )

    if SHOW_PARTS:
        parts.append(
            translate(
                [
                    CARD_WALL + TOKEN_SPACING * 2 + thirdstack,
                    (ROUND_TOKEN_BOX_D - TIME_TOKEN_W) / 2,
                    ROUND_TOKEN_BOX_H - TIME_TOKEN_H / 2,
                ]
            )(rotate([90, 0, 90])(time_token_stack(TIME_TOKEN_COUNT)))
        )

    # Clip sockets
    cutouts.append(
        translate(
            [
                ROUND_TOKEN_BOX_W / 2,
                CLIP_SOCKET_WALL + CLIP_SOCKET / 2,
                ROUND_TOKEN_BOX_H + 0.001,
            ]
        )(clipsocket())
    )
    cutouts.append(
        translate(
            [
                ROUND_TOKEN_BOX_W / 2,
                ROUND_TOKEN_BOX_D - (CLIP_SOCKET_WALL + CLIP_SOCKET / 2),
                ROUND_TOKEN_BOX_H + 0.001,
            ]
        )(clipsocket())
    )
    cutouts.append(
        translate(
            [
                CARD_EDGE_WALL + 10,
                ROUND_TOKEN_BOX_D - CLIP_SOCKET_WALL - CLIP_SOCKET / 2,
                0,
            ]
        )(rotate([180, 0, 0])(clipsocket()))
    )
    cutouts.append(
        translate(
            [
                ROUND_TOKEN_BOX_W - CARD_EDGE_WALL - 10,
                ROUND_TOKEN_BOX_D - CLIP_SOCKET_WALL - CLIP_SOCKET / 2,
                0,
            ]
        )(rotate([180, 0, 0])(clipsocket()))
    )

    d = objsum([d] + parts)

    return d


def generatetokenstack(token, count, expandy=False):
    tokens = []
    for i in range(count):
        if i % 2 == 1:
            tcolor = "blue"
        else:
            tcolor = "red"
        if expandy:
            t = [0, TOKEN_THICK * i, 0]
        else:
            t = [TOKEN_THICK * i, 0, 0]
        tokens.append(color(tcolor)(translate(t)(token)))
    return objsum(tokens)


def large_tokens_tray(showlid=False):
    tokens1cent = (
        LARGE_TOKEN_BOX_W - ADVENTURE_TOKEN_W - MONSTER_TOKEN_W - CARD_EDGE_WALL * 2
    ) / 3 + ADVENTURE_TOKEN_W / 2
    rtokens = []
    cutouts = []
    rtokens.append(
        (
            [
                tokens1cent - COLLAPSED_TUNNEL_TOKEN_W / 2 + COLLAPSED_TUNNEL_TOKEN_W,
                CARD_WALL,
                LARGE_TOKEN_BOX_H - COLLAPSED_TUNNEL_TOKEN_H / 2,
            ],
            rotate([90, 0, 180])(
                linear_extrude((COLLAPSED_TUNNEL_TOKEN_COUNT + 1) * TOKEN_THICK)(
                    polygon(COLLAPSED_TUNNEL_CUTOUT_POINTS)
                )
            ),
            rotate([90, 0, 180])(
                linear_extrude(TOKEN_THICK)(polygon(COLLAPSED_TUNNEL_TOKEN_POINTS))
            ),
            COLLAPSED_TUNNEL_TOKEN_COUNT,
        )
    )
    cutouts.append(
        translate(
            [
                tokens1cent + 5,
                CARD_WALL + (COLLAPSED_TUNNEL_TOKEN_COUNT + 1) * TOKEN_THICK / 2 + 2,
                LARGE_TOKEN_BOX_H - COLLAPSED_TUNNEL_TOKEN_H / 2 - TEXT_D,
            ]
        )(
            linear_extrude(TEXT_D + 5.1)(
                text(
                    "COLLAPSED",
                    size=3,
                    font="Arial:style=Bold",
                    halign="center",
                    valign="center",
                )
            )
        )
    )
    cutouts.append(
        translate(
            [
                tokens1cent + 5,
                CARD_WALL + (COLLAPSED_TUNNEL_TOKEN_COUNT + 1) * TOKEN_THICK / 2 - 2,
                LARGE_TOKEN_BOX_H - COLLAPSED_TUNNEL_TOKEN_H / 2 - TEXT_D,
            ]
        )(
            linear_extrude(TEXT_D + 5.1)(
                text(
                    "TUNNEL",
                    size=3,
                    font="Arial:style=Bold",
                    halign="center",
                    valign="center",
                )
            )
        )
    )

    rtokens.append(
        (
            [
                tokens1cent - ADVENTURE_TOKEN_W / 2,
                CARD_WALL
                + TOKEN_SPACING
                + (COLLAPSED_TUNNEL_TOKEN_COUNT + 1) * TOKEN_THICK,
                LARGE_TOKEN_BOX_H - ADVENTURE_TOKEN_H / 2,
            ],
            cube(
                [
                    ADVENTURE_TOKEN_W,
                    (ADVENTURE_TOKEN_COUNT + 1) * TOKEN_THICK,
                    ADVENTURE_TOKEN_H,
                ]
            ),
            cube([ADVENTURE_TOKEN_W, TOKEN_THICK, ADVENTURE_TOKEN_H]),
            ADVENTURE_TOKEN_COUNT,
        )
    )
    cutouts.append(
        translate(
            [
                tokens1cent,
                CARD_WALL
                + TOKEN_SPACING
                + (COLLAPSED_TUNNEL_TOKEN_COUNT + 1) * TOKEN_THICK
                + (ADVENTURE_TOKEN_COUNT + 1) * TOKEN_THICK / 2
                + 2,
                LARGE_TOKEN_BOX_H - ADVENTURE_TOKEN_H / 2 - TEXT_D,
            ]
        )(
            linear_extrude(TEXT_D + 5.1)(
                text(
                    "ENCOUNTER &",
                    size=3,
                    font="Arial:style=Bold",
                    halign="center",
                    valign="center",
                )
            )
        )
    )
    cutouts.append(
        translate(
            [
                tokens1cent,
                CARD_WALL
                + TOKEN_SPACING
                + (COLLAPSED_TUNNEL_TOKEN_COUNT + 1) * TOKEN_THICK
                + (ADVENTURE_TOKEN_COUNT + 1) * TOKEN_THICK / 2
                - 2,
                LARGE_TOKEN_BOX_H - ADVENTURE_TOKEN_H / 2 - TEXT_D,
            ]
        )(
            linear_extrude(TEXT_D + 5.1)(
                text(
                    "ADVENTURE",
                    size=3,
                    font="Arial:style=Bold",
                    halign="center",
                    valign="center",
                )
            )
        )
    )

    rtokens.append(
        (
            [
                tokens1cent,
                CARD_WALL
                + (COLLAPSED_TUNNEL_TOKEN_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING
                + (ADVENTURE_TOKEN_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING,
                LARGE_TOKEN_BOX_H,
            ],
            forward((HEALING_SURGE_COUNT + 1) * TOKEN_THICK)(
                rotate([90, 0, 0])(
                    cylinder(
                        d=HEALING_SURGE_DIA, h=(HEALING_SURGE_COUNT + 1) * TOKEN_THICK
                    )
                )
            ),
            forward(TOKEN_THICK)(
                rotate([90, 0, 0])(cylinder(d=HEALING_SURGE_DIA, h=TOKEN_THICK))
            ),
            HEALING_SURGE_COUNT,
        )
    )
    cutouts.append(
        intersection()(
            translate(
                [
                    tokens1cent,
                    CARD_WALL
                    + (COLLAPSED_TUNNEL_TOKEN_COUNT + 1) * TOKEN_THICK
                    + TOKEN_SPACING
                    + (ADVENTURE_TOKEN_COUNT + 1) * TOKEN_THICK
                    + TOKEN_SPACING
                    + (HEALING_SURGE_COUNT + 1) * TOKEN_THICK / 2,
                    LARGE_TOKEN_BOX_H - HEALING_SURGE_DIA / 2 - TEXT_D,
                ]
            )(
                linear_extrude(TEXT_D + HEALING_SURGE_DIA)(
                    text(
                        "HEALING SURGE",
                        size=3,
                        font="Arial:style=Bold",
                        halign="center",
                        valign="center",
                    )
                )
            ),
            translate(
                [
                    tokens1cent,
                    CARD_WALL
                    + (COLLAPSED_TUNNEL_TOKEN_COUNT + 1) * TOKEN_THICK
                    + TOKEN_SPACING
                    + (ADVENTURE_TOKEN_COUNT + 1) * TOKEN_THICK
                    + TOKEN_SPACING,
                    LARGE_TOKEN_BOX_H,
                ]
            )(
                forward((HEALING_SURGE_COUNT + 1) * TOKEN_THICK)(
                    rotate([90, 0, 0])(
                        cylinder(
                            d=HEALING_SURGE_DIA + TEXT_D * 2,
                            h=(HEALING_SURGE_COUNT + 1) * TOKEN_THICK,
                        )
                    )
                )
            ),
        )
    )

    tokens2cent = (
        LARGE_TOKEN_BOX_W - ADVENTURE_TOKEN_W - MONSTER_TOKEN_W - CARD_EDGE_WALL * 2
    ) / 3 + MONSTER_TOKEN_W / 2

    rtokens.append(
        (
            [
                LARGE_TOKEN_BOX_W - tokens2cent - MONSTER_TOKEN_W / 2,
                CARD_WALL,
                LARGE_TOKEN_BOX_H - MONSTER_TOKEN_H / 2,
            ],
            cube(
                [
                    MONSTER_TOKEN_W,
                    (MONSTER_TOKEN_COUNT + 1) * TOKEN_THICK,
                    MONSTER_TOKEN_H,
                ]
            ),
            cube([MONSTER_TOKEN_W, TOKEN_THICK, MONSTER_TOKEN_H]),
            MONSTER_TOKEN_COUNT,
        )
    )
    cutouts.append(
        translate(
            [
                LARGE_TOKEN_BOX_W - tokens2cent,
                CARD_WALL + (MONSTER_TOKEN_COUNT + 1) * TOKEN_THICK / 2,
                LARGE_TOKEN_BOX_H - MONSTER_TOKEN_H / 2 - TEXT_D,
            ]
        )(
            linear_extrude(TEXT_D + 5.1)(
                text(
                    "MONSTER",
                    size=3,
                    font="Arial:style=Bold",
                    halign="center",
                    valign="center",
                )
            )
        )
    )

    rtokens.append(
        (
            [
                LARGE_TOKEN_BOX_W - tokens2cent - CHEST_TOKEN_W / 2,
                CARD_WALL + (MONSTER_TOKEN_COUNT + 1) * TOKEN_THICK + TOKEN_SPACING,
                LARGE_TOKEN_BOX_H - CHEST_TOKEN_H / 2,
            ],
            cube([CHEST_TOKEN_W, (CHEST_TOKEN_COUNT + 1) * TOKEN_THICK, CHEST_TOKEN_H]),
            cube([CHEST_TOKEN_W, TOKEN_THICK, CHEST_TOKEN_H]),
            CHEST_TOKEN_COUNT,
        )
    )
    cutouts.append(
        translate(
            [
                LARGE_TOKEN_BOX_W - tokens2cent,
                CARD_WALL
                + (MONSTER_TOKEN_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING
                + (CHEST_TOKEN_COUNT + 1) * TOKEN_THICK / 2,
                LARGE_TOKEN_BOX_H - CHEST_TOKEN_H / 2 - TEXT_D,
            ]
        )(
            linear_extrude(TEXT_D + 5.1)(
                text(
                    "CHEST",
                    size=3,
                    font="Arial:style=Bold",
                    halign="center",
                    valign="center",
                )
            )
        )
    )

    rtokens.append(
        (
            [
                LARGE_TOKEN_BOX_W - tokens2cent,
                LARGE_TOKEN_BOX_D - CARD_WALL - (STANCE_TOKEN_COUNT + 1) * TOKEN_THICK,
                LARGE_TOKEN_BOX_H,
            ],
            forward((STANCE_TOKEN_COUNT + 1) * TOKEN_THICK)(
                rotate([90, 0, 0])(
                    scale([STANCE_TOKEN_DIA_W / STANCE_TOKEN_DIA_H, 1, 1])(
                        cylinder(
                            d=STANCE_TOKEN_DIA_H,
                            h=(STANCE_TOKEN_COUNT + 1) * TOKEN_THICK,
                        )
                    )
                )
            ),
            forward(TOKEN_THICK)(
                rotate([90, 0, 0])(
                    scale([STANCE_TOKEN_DIA_W / STANCE_TOKEN_DIA_H, 1, 1])(
                        cylinder(d=STANCE_TOKEN_DIA_H, h=TOKEN_THICK)
                    )
                )
            ),
            STANCE_TOKEN_COUNT,
        )
    )
    cutouts.append(
        translate(
            [
                LARGE_TOKEN_BOX_W - tokens2cent,
                LARGE_TOKEN_BOX_D
                - CARD_WALL
                - (STANCE_TOKEN_COUNT + 1) * TOKEN_THICK
                - 2,
                LARGE_TOKEN_BOX_H - TEXT_D,
            ]
        )(
            linear_extrude(TEXT_D + 5.1)(
                text(
                    "STANCE",
                    size=3,
                    font="Arial:style=Bold",
                    halign="center",
                    valign="center",
                )
            )
        )
    )

    parts = []
    for tokenpos, tokenstack, singletoken, tokencount in rtokens:
        cutouts.append(translate(tokenpos)(tokenstack))
        if SHOW_PARTS:
            parts.append(
                translate(tokenpos)(generatetokenstack(singletoken, tokencount, True))
            )

    # Clip sockets
    cutouts.append(
        translate(
            [
                CLIP_SOCKET / 2 + CLIP_SOCKET_WALL,
                LARGE_TOKEN_BOX_D / 2,
                LARGE_TOKEN_BOX_H,
            ]
        )(rotate([0, 0, 90])(clipsocket()))
    )
    cutouts.append(
        translate(
            [
                LARGE_TOKEN_BOX_W - CLIP_SOCKET / 2 - CLIP_SOCKET_WALL,
                LARGE_TOKEN_BOX_D / 2,
                LARGE_TOKEN_BOX_H,
            ]
        )(rotate([0, 0, 90])(clipsocket()))
    )

    # Corner marker to match with lid
    cutouts.append(
        translate([LARGE_TOKEN_BOX_W + 0.1, LARGE_TOKEN_BOX_D / 4, LARGE_TOKEN_BOX_H])(
            rotate([0, -90, 0])(cylinder(d=10, h=2 + 0.5))
        )
    )

    d = difference()(
        roundedCube([LARGE_TOKEN_BOX_W, LARGE_TOKEN_BOX_D, LARGE_TOKEN_BOX_H], 5, True),
        *cutouts,
    )
    d = objsum([d] + parts)

    if showlid:
        d += translate([LARGE_TOKEN_BOX_W, 0, LARGE_TOKEN_BOX_H * 2])(
            rotate([0, 180, 0])(large_tokens_tray_lid())
        ).set_modifier("%")

    return d


def large_tokens_tray_lid():
    d = difference()(
        roundedCube([LARGE_TOKEN_BOX_W, LARGE_TOKEN_BOX_D, LARGE_TOKEN_BOX_H], 5, True),
        translate([CARD_EDGE_WALL, CARD_WALL, FLOOR])(
            roundedCube(
                [
                    LARGE_TOKEN_BOX_W - CARD_EDGE_WALL * 2,
                    LARGE_TOKEN_BOX_D - CARD_WALL * 2,
                    LARGE_TOKEN_BOX_H,
                ],
                5,
                True,
            )
        ),
    ) + intersection()(
        roundedCube([LARGE_TOKEN_BOX_W, LARGE_TOKEN_BOX_D, LARGE_TOKEN_BOX_H], 5, True),
        down(5)(
            roundedCube(
                [
                    MONSTER_TOKEN_W + CARD_EDGE_WALL + TOKEN_SPACING / 2,
                    (MONSTER_TOKEN_COUNT + 1) * TOKEN_THICK
                    + CARD_WALL
                    + TOKEN_SPACING / 2,
                    5 + LARGE_TOKEN_BOX_H - MONSTER_TOKEN_H / 2 - 1,
                ],
                2,
                False,
            )
        ),
    )
    d = difference()(
        d,
        translate([LARGE_TOKEN_BOX_W / 2, LARGE_TOKEN_BOX_D + 1, LARGE_TOKEN_BOX_H])(
            rotate([90, 0, 0])(cylinder(d=20, h=LARGE_TOKEN_BOX_D + 2))
        ),
        translate([LARGE_TOKEN_BOX_W / 2, LARGE_TOKEN_BOX_D / 2, -0.1])(
            rotate([0, 0, 0])(
                mirror([1, 0, 0])(
                    linear_extrude(TEXT_D + 0.1)(
                        text(
                            "LARGER TOKENS",
                            size=7,
                            font="Arial:style=Bold",
                            halign="center",
                            valign="center",
                        )
                    )
                )
            )
        ),
        translate(
            [
                CLIP_SOCKET / 2 + CLIP_SOCKET_WALL,
                LARGE_TOKEN_BOX_D / 2,
                LARGE_TOKEN_BOX_H,
            ]
        )(rotate([0, 0, 90])(clipsocket())),
        translate(
            [
                LARGE_TOKEN_BOX_W - CLIP_SOCKET / 2 - CLIP_SOCKET_WALL,
                LARGE_TOKEN_BOX_D / 2,
                LARGE_TOKEN_BOX_H,
            ]
        )(rotate([0, 0, 90])(clipsocket())),
    )
    d += translate([0, LARGE_TOKEN_BOX_D / 4, LARGE_TOKEN_BOX_H])(
        rotate([0, 90, 0])(cylinder(d=10, h=2))
    )

    return d

    d = objsum([d] + parts)

    return d


def status_tokens_tray(showlid=False):
    endpadding = (
        STATUS_TOKENS_BOX_D
        - (
            (
                POISONED_TOKENS_COUNT
                + IMMOBILIZED_TOKENS_COUNT
                + MONSTER_1_HP_TOKEN_COUNT
                + 3
            )
            * TOKEN_THICK
            + DIE_DIA
            + TOKEN_SPACING * 3
        )
    ) / 2
    rtokens = []
    cutouts = []
    rtokens.append(
        (
            [
                (STATUS_TOKENS_BOX_W - IMMOBILIZED_TOKENS_W) / 2,
                endpadding,
                STATUS_TOKENS_BOX_H - IMMOBILIZED_TOKENS_H / 2,
            ],
            (
                [
                    IMMOBILIZED_TOKENS_W,
                    (IMMOBILIZED_TOKENS_COUNT + 1) * TOKEN_THICK,
                    IMMOBILIZED_TOKENS_H,
                ]
            ),
            cube([IMMOBILIZED_TOKENS_W, TOKEN_THICK, IMMOBILIZED_TOKENS_H]),
            IMMOBILIZED_TOKENS_COUNT,
            "IMMOBILIZED",
        )
    )
    rtokens.append(
        (
            [
                (STATUS_TOKENS_BOX_W - POISONED_TOKENS_W) / 2,
                endpadding
                + (IMMOBILIZED_TOKENS_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING,
                STATUS_TOKENS_BOX_H - POISONED_TOKENS_H / 2,
            ],
            (
                [
                    POISONED_TOKENS_W,
                    (POISONED_TOKENS_COUNT + 1) * TOKEN_THICK,
                    POISONED_TOKENS_H,
                ]
            ),
            cube([POISONED_TOKENS_W, TOKEN_THICK, POISONED_TOKENS_H]),
            POISONED_TOKENS_COUNT,
            "POISONED",
        )
    )

    rtokens.append(
        (
            [
                (STATUS_TOKENS_BOX_W - HP_5_TOKEN_W - DIE_DIA) / 3,
                endpadding
                + (IMMOBILIZED_TOKENS_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING
                + (POISONED_TOKENS_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING,
                STATUS_TOKENS_BOX_H - HP_5_TOKEN_H / 2,
            ],
            ([HP_5_TOKEN_W, (HP_5_TOKEN_COUNT + 1) * TOKEN_THICK, HP_5_TOKEN_H]),
            cube([HP_5_TOKEN_W, TOKEN_THICK, HP_5_TOKEN_H]),
            HP_5_TOKEN_COUNT,
            "5 HP",
        )
    )

    rtokens.append(
        (
            [
                CARD_EDGE_WALL,
                endpadding
                + (IMMOBILIZED_TOKENS_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING
                + (POISONED_TOKENS_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING
                + DIE_DIA
                + TOKEN_SPACING,
                STATUS_TOKENS_BOX_H - MONSTER_HP_TOKEN_H / 2,
            ],
            (
                [
                    MONSTER_HP_TOKEN_W,
                    (MONSTER_1_HP_TOKEN_COUNT + 1) * TOKEN_THICK,
                    MONSTER_HP_TOKEN_H,
                ]
            ),
            cube([MONSTER_HP_TOKEN_W, TOKEN_THICK, MONSTER_HP_TOKEN_H]),
            MONSTER_1_HP_TOKEN_COUNT,
            "1 HP",
        )
    )

    rtokens.append(
        (
            [
                STATUS_TOKENS_BOX_W - CARD_EDGE_WALL - MONSTER_HP_TOKEN_W,
                endpadding
                + (IMMOBILIZED_TOKENS_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING
                + (POISONED_TOKENS_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING
                + DIE_DIA
                + TOKEN_SPACING,
                STATUS_TOKENS_BOX_H - MONSTER_HP_TOKEN_H / 2,
            ],
            (
                [
                    MONSTER_HP_TOKEN_W,
                    (MONSTER_4AC_TOKEN_COUNT + 1) * TOKEN_THICK,
                    MONSTER_HP_TOKEN_H,
                ]
            ),
            cube([MONSTER_HP_TOKEN_W, TOKEN_THICK, MONSTER_HP_TOKEN_H]),
            MONSTER_4AC_TOKEN_COUNT,
            "-4 AC",
        )
    )

    rtokens.append(
        (
            [
                STATUS_TOKENS_BOX_W - CARD_EDGE_WALL - MONSTER_HP_TOKEN_W,
                endpadding
                + (IMMOBILIZED_TOKENS_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING
                + (POISONED_TOKENS_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING
                + DIE_DIA
                + TOKEN_SPACING
                + (MONSTER_4AC_TOKEN_COUNT + 1) * TOKEN_THICK
                + TOKEN_SPACING,
                STATUS_TOKENS_BOX_H - MONSTER_HP_TOKEN_H / 2,
            ],
            (
                [
                    MONSTER_HP_TOKEN_W,
                    (MONSTER_2_HP_TOKEN_COUNT + 1) * TOKEN_THICK,
                    MONSTER_HP_TOKEN_H,
                ]
            ),
            cube([MONSTER_HP_TOKEN_W, TOKEN_THICK, MONSTER_HP_TOKEN_H]),
            MONSTER_2_HP_TOKEN_COUNT,
            "2 HP",
        )
    )

    parts = []
    for tokenpos, tokenstack, singletoken, tokencount, txt in rtokens:
        cutouts.append(translate(tokenpos)(cube(tokenstack)))
        txtpos = [
            tokenpos[0] + tokenstack[0] / 2,
            tokenpos[1] + tokenstack[1] / 2,
            tokenpos[2] - TEXT_D,
        ]
        cutouts.append(
            translate(txtpos)(
                rotate([0, 0, 180])(
                    linear_extrude(TEXT_D + 1)(
                        text(
                            txt,
                            size=3,
                            font="Arial:style=Bold",
                            halign="center",
                            valign="center",
                        )
                    )
                )
            )
        )
        if SHOW_PARTS:
            parts.append(
                translate(tokenpos)(generatetokenstack(singletoken, tokencount, True))
            )

    # The Die
    spherepos = [
        STATUS_TOKENS_BOX_W
        - (STATUS_TOKENS_BOX_W - HP_5_TOKEN_W - DIE_DIA) / 3
        - DIE_DIA / 2,
        endpadding
        + (IMMOBILIZED_TOKENS_COUNT + 1) * TOKEN_THICK
        + TOKEN_SPACING
        + (POISONED_TOKENS_COUNT + 1) * TOKEN_THICK
        + TOKEN_SPACING
        + DIE_DIA / 2,
        STATUS_TOKENS_BOX_H,
    ]
    cutouts.append(translate(spherepos)(sphere(d=DIE_DIA)))
    cutouts.append(
        down(DIE_DIA / 2 + TEXT_D)(
            translate(spherepos)(
                rotate([0, 0, 180])(
                    linear_extrude(DIE_DIA)(
                        text(
                            "D20",
                            size=3,
                            font="Arial:style=Bold",
                            halign="center",
                            valign="center",
                        )
                    )
                )
            )
        )
    )
    if SHOW_PARTS:
        parts.append(
            translate(spherepos)(color("purple")(sphere(d=DIE_DIA, segments=7)))
        )

    # Clip sockets
    cutouts.append(
        translate(
            [
                CLIP_SOCKET / 2 + CLIP_SOCKET_WALL,
                STATUS_TOKENS_BOX_D / 2,
                STATUS_TOKENS_BOX_H,
            ]
        )(rotate([0, 0, 90])(clipsocket()))
    )
    cutouts.append(
        translate(
            [
                STATUS_TOKENS_BOX_W - CLIP_SOCKET / 2 - CLIP_SOCKET_WALL,
                STATUS_TOKENS_BOX_D / 2,
                STATUS_TOKENS_BOX_H,
            ]
        )(rotate([0, 0, 90])(clipsocket()))
    )

    # Sphere cutout to show correct matching end for lid
    cutouts.append(
        translate([STATUS_TOKENS_BOX_W / 2, STATUS_TOKENS_BOX_D, STATUS_TOKENS_BOX_H])(
            sphere(d=20)
        )
    )
    cutouts.append(
        translate([STATUS_TOKENS_BOX_W, STATUS_TOKENS_BOX_D, STATUS_TOKENS_BOX_H])(
            sphere(d=10)
        )
    )

    d = difference()(
        roundedCube(
            [STATUS_TOKENS_BOX_W, STATUS_TOKENS_BOX_D, STATUS_TOKENS_BOX_H], 5, True
        ),
        *cutouts,
    )
    d = objsum([d] + parts)
    if showlid:
        d += translate([0, STATUS_TOKENS_BOX_D, STATUS_TOKENS_BOX_H * 2])(
            rotate([180, 0, 0])((status_tokens_tray_lid()))
        ).set_modifier("%")

    return d


def status_tokens_tray_lid():
    cutouts = []

    # Clip sockets
    cutouts.append(
        translate(
            [
                CLIP_SOCKET / 2 + CLIP_SOCKET_WALL,
                STATUS_TOKENS_BOX_D / 2,
                STATUS_TOKENS_BOX_H,
            ]
        )(rotate([0, 0, 90])(clipsocket()))
    )
    cutouts.append(
        translate(
            [
                STATUS_TOKENS_BOX_W - CLIP_SOCKET / 2 - CLIP_SOCKET_WALL,
                STATUS_TOKENS_BOX_D / 2,
                STATUS_TOKENS_BOX_H,
            ]
        )(rotate([0, 0, 90])(clipsocket()))
    )
    cutouts.append(
        translate([STATUS_TOKENS_BOX_W / 2 - 9, STATUS_TOKENS_BOX_D / 2, -0.1])(
            rotate([0, 0, 90])(
                mirror([1, 0, 0])(
                    linear_extrude(TEXT_D + 0.1)(
                        text(
                            "CONDITIONS",
                            size=7,
                            font="Arial:style=Bold",
                            halign="center",
                            valign="center",
                        )
                    )
                )
            )
        )
    )
    cutouts.append(
        translate([STATUS_TOKENS_BOX_W / 2, STATUS_TOKENS_BOX_D / 2, -0.1])(
            rotate([0, 0, 90])(
                mirror([1, 0, 0])(
                    linear_extrude(TEXT_D + 0.1)(
                        text(
                            "HP & AC TOKENS",
                            size=7,
                            font="Arial:style=Bold",
                            halign="center",
                            valign="center",
                        )
                    )
                )
            )
        )
    )
    cutouts.append(
        translate([STATUS_TOKENS_BOX_W / 2 + 9, STATUS_TOKENS_BOX_D / 2, -0.1])(
            rotate([0, 0, 90])(
                mirror([1, 0, 0])(
                    linear_extrude(TEXT_D + 0.1)(
                        text(
                            "D20 DIE",
                            size=7,
                            font="Arial:style=Bold",
                            halign="center",
                            valign="center",
                        )
                    )
                )
            )
        )
    )

    cutouts.append(
        translate(
            [STATUS_TOKENS_BOX_W / 2, STATUS_TOKENS_BOX_D / 2, STATUS_TOKENS_BOX_H]
        )(rotate([90, 0, 0])(cylinder(d=20, h=STATUS_TOKENS_BOX_D / 2 + 1)))
    )

    fillcube = roundedCube(
        [STATUS_TOKENS_BOX_W, STATUS_TOKENS_BOX_D, STATUS_TOKENS_BOX_H + 10], 5, True
    )

    d = (
        difference()(
            roundedCube(
                [STATUS_TOKENS_BOX_W, STATUS_TOKENS_BOX_D, STATUS_TOKENS_BOX_H], 5, True
            ),
            translate([CARD_EDGE_WALL, CARD_WALL, FLOOR])(
                roundedCube(
                    [
                        STATUS_TOKENS_BOX_W - CARD_EDGE_WALL * 2,
                        STATUS_TOKENS_BOX_D - CARD_WALL * 2,
                        STATUS_TOKENS_BOX_H,
                    ],
                    5,
                    True,
                )
            ),
        )
        + intersection()(
            # The "Lock" for the corner
            translate([STATUS_TOKENS_BOX_W, 0, STATUS_TOKENS_BOX_H])(sphere(d=10)),
            fillcube,
        )
        + intersection()(
            fillcube,
            roundedCube(
                # Extra padding to prevent the tokens falling out
                [
                    STATUS_TOKENS_BOX_W,
                    (MONSTER_1_HP_TOKEN_COUNT + 1) * TOKEN_THICK + TOKEN_SPACING * 1.5,
                    FLOOR + (POISONED_TOKENS_H - MONSTER_HP_TOKEN_H) / 2,
                ],
                2,
                False,
            ),
        )
    )

    d = difference()(d, *cutouts)
    return d


def hero_box():
    """This is designed to be missing an edge as the available width is very tight
    """
    d = difference()(
        left(10)(roundedCube([HERO_BOX_W + 10, HERO_BOX_D, HERO_BOX_H], 5, True)),
        translate([-20, -1, -1])(cube([20, HERO_BOX_D * 2, HERO_BOX_H * 2])),
        translate([-0.1, CARD_EDGE_WALL, FLOOR])(
            cube([HERO_CARD_W + 0.1, (HERO_CARD_COUNT + 1) * TOKEN_THICK, HERO_CARD_H])
        ),
    )
    # To round off the corners
    cutouts = [
        up(HERO_BOX_H - 10)(
            difference()(
                translate([-0.1, -0.1, 0])(cube([11, HERO_BOX_D + 2, 11])),
                translate([10, -1, 0])(
                    rotate([-90, 0, 0])(cylinder(h=HERO_BOX_D * 2, d=20))
                ),
            )
        )
    ]
    cutouts.append(
        translate([HERO_BOX_W / 2, HERO_BOX_D / 2, FLOOR - TEXT_D])(
            linear_extrude(TEXT_D + 0.1)(
                text(
                    "HERO CARDS",
                    size=7,
                    font="Arial:style=Bold",
                    halign="center",
                    valign="center",
                )
            )
        )
    )
    d = difference()(d, *cutouts)
    return d


def slide_lid_obj(width, depth, cutouts):
    if cutouts:
        h = SLIDE_BOX_WALL - SLIDE_LID_TOLERANCE
    else:
        h = SLIDE_BOX_WALL
    d = cube([width, depth, h])
    if cutouts:
        # Ensure there is a solid wall all the way around
        edgew = SLIDE_BOX_WALL * 2
        center_box = translate([edgew, edgew, -0.1])(
            cube([width - edgew * 2, depth - edgew * 2, SLIDE_BOX_WALL + 1])
        )
        d -= center_box
        leftline = rotate([0, 0, 45])(cube([width + depth, SLIDE_BOX_WALL, h]))
        rightline = rotate([0, 0, -45])(cube([width + depth, SLIDE_BOX_WALL, h]))
        lineset = leftline + rightline
        lines = []
        i = -depth
        while i < width + depth:
            lines.append(forward(i)(lineset))
            i += SLIDE_BOX_WALL * 6
        mesh = intersection()(center_box, union()(*lines))
        d += mesh

    cutouts = []
    trigtop = SLIDE_BOX_WALL * math.tan(math.radians(30))
    edgecut = forward(depth + 1)(
        rotate([90, 0, 0])(
            linear_extrude(depth + 2)(
                polygon(
                    [
                        [-0.1, -0.1],
                        [trigtop, SLIDE_BOX_WALL + 0.1],
                        [-0.1, SLIDE_BOX_WALL + 0.1],
                    ]
                )
            )
        )
    )
    cutouts.append(edgecut)
    cutouts.append(right(width)(mirror([1, 0, 0])(edgecut)))
    return difference()(d, *cutouts)


def hp_1_token_box_lid():
    lidedge = SLIDE_BOX_WALL * 0.4
    w = HP_1_TOKEN_W - lidedge * 2 - SLIDE_LID_TOLERANCE * 2
    d = slide_lid_obj(w, HP_1_TOKEN_D - SLIDE_BOX_WALL, True)
    # Add a finger hole
    h = SLIDE_BOX_WALL - SLIDE_LID_TOLERANCE
    fingerhole = translate([w / 2, (SLIDE_LID_FINGER_DIA + SLIDE_BOX_WALL * 2) / 2, 0])(
        cylinder(d=SLIDE_LID_FINGER_DIA + SLIDE_BOX_WALL * 2, h=h)
        + hole()(down(0.1)(cylinder(d=SLIDE_LID_FINGER_DIA, h=h + 0.2)))
    )
    d += fingerhole

    return intersection()(
        d,
        roundedCube(
            [
                HP_1_TOKEN_W - lidedge * 2 - SLIDE_LID_TOLERANCE * 2,
                HP_1_TOKEN_D,
                HP_1_TOKEN_H,
            ],
            5,
            True,
        ),
    )


def hp_1_token_box(showlid=False):
    d = roundedCube([HP_1_TOKEN_W, HP_1_TOKEN_D, HP_1_TOKEN_H], 5, True)
    cutouts = []
    cutouts.append(
        translate([SLIDE_BOX_WALL, SLIDE_BOX_WALL, FLOOR])(
            roundedCube(
                [
                    HP_1_TOKEN_W - SLIDE_BOX_WALL * 2,
                    HP_1_TOKEN_D - SLIDE_BOX_WALL * 2,
                    HP_1_TOKEN_H * 2,
                ],
                4,
                False,
            )
        )
    )
    lidedge = SLIDE_BOX_WALL * 0.4
    cutouts.append(
        translate([lidedge, -SLIDE_BOX_WALL, HP_1_TOKEN_H - SLIDE_BOX_WALL + 0.01])(
            slide_lid_obj(HP_1_TOKEN_W - lidedge * 2, HP_1_TOKEN_D, False)
        )
    )
    d = difference()(d, *cutouts)

    if showlid:
        d += color("green")(
            translate(
                [lidedge + SLIDE_LID_TOLERANCE, 0, HP_1_TOKEN_H - SLIDE_BOX_WALL]
            )(hp_1_token_box_lid())
        )
    return d


# [22.15848, 49.941852], Min: [-22.15848, -49.941852]


def mini_svg_locations():
    small_x = 5
    small_y = 90
    print("25 mm")
    for x, y, _ in OFFSETS_25mm:
        print(x + small_x - 25 / 2, small_y + LOWER_TRAY_D - y - 25 / 2)
    print("20 mm")
    for x, y, _ in OFFSETS_20mm:
        print(x + small_x - 20 / 2, small_y + LOWER_TRAY_D - y - 20 / 2)

    large_x = -200
    large_y = 0
    print("50 mm")
    for x in X_OFFSETS_50MM:
        for y in Y_OFFSETS_50MM:
            print(x + large_x - 50 / 2, large_y + UPPER_TRAY_D - y - 50 / 2)


def rendereverything(includelids=True):
    d = difference()(
        translate([-1 / 2, -1 / 2, -1 / 2])(
            cube([BOX_INNER_W + 1, BOX_INNER_W + 1, BOX_INNER_H + 1 / 2])
        ),
        translate([0, 0, 0])(cube([BOX_INNER_W, BOX_INNER_W, BOX_INNER_H + 1])),
    ).set_modifier("%")

    d += color("red")(lower_small_minis_tray(True))
    d += color("blue")(upper_small_minis_tray(True))
    d += color("green")(large_minis_tray(True))
    d += translate([BIG_TRAY_W + CAVERN_EDGE_BOX_D, 0, LOWER_TRAY_H])(
        rotate([0, 0, 90])(color("cyan")(cavern_edge_tiles()))
    )
    d += translate([0, LOWER_TRAY_D, 0])(
        rotate([0, 0, 0])(color("magenta")(small_terrain_tiles_vertical()))
    )
    d += translate([0, LOWER_TRAY_D + SMALL_TERRAIN_BOX_D, 0])(
        rotate([0, 0, 0])(color("#808080cc")(large_terrain_tiles_vertical()))
    )

    if includelids:
        d += translate(
            [
                SMALL_TERRAIN_BOX_W + CARD_BOX_W,
                LOWER_TRAY_D,
                CARD_BOX_H + CARD_BOX_LID_H,
            ]
        )(rotate([0, 180, 0])(color("#adff2f99")(cards_box_lid())))
    d += translate([SMALL_TERRAIN_BOX_W, LOWER_TRAY_D + CARD_BOX_D, 0])(
        rotate([0, 0, 0])(color("#2e8b57cc")(cards_box()))
    )
    if includelids:
        d += translate(
            [
                SMALL_TERRAIN_BOX_W + CARD_BOX_W,
                LOWER_TRAY_D + CARD_BOX_D,
                CARD_BOX_H + CARD_BOX_LID_H,
            ]
        )(rotate([0, 180, 0])(color("#2e8b5799")(cards_box_lid())))
    d += translate([SMALL_TERRAIN_BOX_W, LOWER_TRAY_D, 0])(
        rotate([0, 0, 0])(color("#adff2fcc")(cards_box()))
    )
    d += translate([0, UPPER_TRAY_D, LOWER_TRAY_H])(
        rotate([0, 0, 0])(color("DarkRed")(round_tokens_tray()))
    )
    d += translate([LOWER_TRAY_W, HERO_BOX_D + 106, STATUS_TOKENS_BOX_H * 2])(
        rotate([0, 0, 0])(color("DarkViolet")(large_tokens_tray()))
    )
    d += translate([LOWER_TRAY_W + STATUS_TOKENS_BOX_D, HERO_BOX_D + 106, 0])(
        rotate([0, 0, 90])(color("Turquoise")(status_tokens_tray()))
    )
    d += translate([LOWER_TRAY_W, 0, 0])(hero_box())
    # Errtu
    d += translate([LOWER_TRAY_W + 106 / 2 - 5, 106 / 2 + HERO_BOX_D, 0])(
        cylinder(d=106, h=95)
    ).set_modifier("#")

    saveasscad(d, "test")


def main():
    mini_svg_locations()

    # saveasscad((clipsocket()), "test")
    saveasscad((cards_box()), "cards-box-x2")
    saveasscad((cards_box_lid()), "cards-box-lid-x2")
    saveasscad(round_tokens_tray(), "round-tokens-tray")
    saveasscad(round_tokens_tray_lid(), "round-tokens-tray-lid")
    saveasscad((large_terrain_tiles_vertical()), "large-terrain-tiles")
    saveasscad(hp_1_token_box(), "1-hp-tokens-x2")
    saveasscad(hp_1_token_box_lid(), "1-hp-tokens-lid-x2")
    saveasscad((cavern_edge_tiles()), "cavern-edge-terrain-tiles")
    saveasscad((cavern_edge_tiles_lid()), "cavern-edge-terrain-tiles-lid")
    saveasscad(hero_box(), "hero-box")

    saveasscad(status_tokens_tray(), "status-tokens-tray")
    saveasscad(status_tokens_tray_lid(), "status-tokens-tray-lid")
    saveasscad((small_terrain_tiles_vertical()), "small-terrain-tiles")

    saveasscad(large_tokens_tray(), "large-tokens-tray")
    saveasscad(large_tokens_tray_lid(), "large-tokens-tray-lid")

    saveasscad(lower_small_minis_tray(), "small-minis-lower")
    saveasscad(upper_small_minis_tray(), "small-minis-upper")
    saveasscad(large_minis_tray(), "large-minis", fn=250)
    rendereverything()


def saveasscad(obj, desc, fn=50):
    pfn = pathlib.Path(__file__)
    pfn = pfn.parent / "generated"
    if not pfn.exists():
        pfn.mkdir()
    outfn = pfn / ("{}.scad".format(desc))
    scad_render_to_file(obj, outfn, file_header=f"$fn = {fn};\n")


if __name__ == "__main__":
    main()

