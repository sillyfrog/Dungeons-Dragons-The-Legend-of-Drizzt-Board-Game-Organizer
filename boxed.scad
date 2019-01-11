use <minis-small-insert.scad>;
use <minis-large-insert.scad>;
use <terrain-tiles.scad>;
use <cards.scad>;
include <consts.scad>;

BOX_INNER_W = 305;
BOX_INNER_H = 115;

// The actual box
%difference() {
    translate([-1/2, -1/2, -1/2]) cube([BOX_INNER_W+1, BOX_INNER_W+1, BOX_INNER_H+1/2]);
    translate([0, 0, 0]) cube([BOX_INNER_W, BOX_INNER_W, BOX_INNER_H+1]);
}

// The minis trays
translate([0, 0, 0]) color("yellow") small_minis_tray();
translate([0, 0, LOWER_TRAY_UPPER_H]) color("blue") large_minis_tray();

// Terrain tiles
translate([0, LOWER_TRAY_D, 0]) color("cyan") small_terrain_tiles_vertical();
translate([0, BOX_INNER_W - LARGE_TERRAIN_BOX_D, 0]) color("blue") large_terrain_tiles_vertical();

// Cards
translate([SMALL_TERRAIN_BOX_W, LOWER_TRAY_D, 0]) color("purple") card_box(true);
translate([SMALL_TERRAIN_BOX_W, LOWER_TRAY_D + CARD_BOX_D, 0]) color("pink") card_box(true);

//translate([0, UPPER_TRAY_D, LOWER_TRAY_H]) #small_terrain_tiles();
//translate([(SMALL_TERRAIN_BASE_W-LARGE_TERRAIN_BASE_W)/2, UPPER_TRAY_D, LOWER_TRAY_H+SMALL_TERRAIN_BASE_H]) color("green") large_terrain_tiles();
//translate([0, UPPER_TRAY_D, LOWER_TRAY_H]) #small_terrain_tiles();

// Errtu
translate([BOX_INNER_W-106/2, BOX_INNER_W-106/2,0]) #cylinder(d=106, h=95);

// Space for rest of stuff

translate([LOWER_TRAY_W, 0,0]) #cube([105, 190, 115]);