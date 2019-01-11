include <consts.scad>;


module card_box(withlid=false) {
    card_box_obj(CARD_BOX_H);
    #translate([CARD_EDGE_WALL, CARD_WALL+2, CARD_EDGE_WALL]) cards_stack();
    if (withlid) {
        %translate([CARD_BOX_W, 0, CARD_BOX_H+CARD_BOX_LID_H]) rotate([0, 180, 0]) card_box_lid();
    }
}

module card_box_lid() {
    card_box_obj(CARD_BOX_LID_H);
}

module card_box_obj(H) {
    difference() {
        union() {
            translate([0, 0, 0]) roundedCube([CARD_BOX_W, CARD_BOX_D, H], 5, true);
        }
        translate([CARD_EDGE_WALL, CARD_WALL, CARD_WALL]) roundedCube([CARD_BOX_W-CARD_EDGE_WALL*2, CARD_BOX_D-CARD_WALL*2, H], 2, true);
    }
    //#translate([TERRAIN_V_WALL, 2*SMALL_TERRAIN_TILES+TERRAIN_V_WALL, 0]) rotate([90, 0, 0]) small_terrain_tile(SMALL_TERRAIN_TILES);
    for (x=[0,1]) {
        offset = x * (CARD_BOX_W - CARD_EDGE_WALL);
        #translate([CLIP_H+(CARD_EDGE_WALL-CLIP_H)/2+offset,CARD_BOX_D/2,H]) rotate([-90, 0, 90]) socket(1.5);
    }
}

module cards_stack() {
    cube([CARD_W, CARD_STACK, CARD_D]);
}

card_box();
translate([100, 0, 0]) card_box_lid();