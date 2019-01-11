use <small-parts-outlines.scad>;
use <small-parts-text-outlines.scad>;
use <MCAD/boxes.scad>
include <consts.scad>;

TOTAL_H = LOWER_TRAY_H;

BIG_TRAY_W = UPPER_TRAY_W + 2;
BIG_TRAY_D = UPPER_TRAY_D + 2;
H_FOR_BIG_TRAY = LOWER_TRAY_UPPER_H; // 40mm

20MM_X_OFFSETS = [5, 30, 62, 95];
25MM_Y_OFFSETS = [165, 135, 95, 60];

module small_minis_tray() {
    translate([100, 100, FLOOR+BASE_H]) small_minis_tray_obj();
}

small_minis_tray();

module small_minis_tray_obj() {
union() {
    difference() {
        translate([0, 0, TOTAL_H/2-FLOOR-BASE_H]) roundedBox([200, 200, TOTAL_H], 5, true);

        translate([0, 0, 0]) outlines();
        translate([0, 0, -BASE_H-0.4]) textoutlines();

        // 25mm bases
        for (y=25MM_Y_OFFSETS) {
            y = y + 25/2 - 100;
            if ((y - 25/2 + 100) == 60) {
                translate([33, y, -BASE_H]) x25mm(5);
                // Still want the finger grab all the way through
                translate([0, y, -BASE_H]) fingergrab(17);
            } else {
                translate([0, y, -BASE_H]) x25mm();
            }
        }
        // Artemis Entreri
        translate([33*5, 10 + 25/2 - 100, -BASE_H]) x25mm(1);
        translate([33*5-10, 10 + 25/2 - 100, -BASE_H]) fingergrab(17);

        // 20mm bases
        for (y=[35+20/2-100, 10+20/2-100]) {
            start = -100+5+20/2;
            for (x=20MM_X_OFFSETS){
                x = -100+20/2+x;
                translate([x, y, -BASE_H]) cylinder(h=TOTAL_H+6, d=21);
                translate([x, y, 0]) cylinder(h=TOTAL_H+6, d=21+2);
                fingersize = 30*4+20;
                translate([-fingersize/2+30, y, -BASE_H]) fingergrab(12, fingersize);
            }
        }

        // Spider stack, these are kept relatively tight in their slot
        SPIDER_STACK_H = LOWER_TRAY_UPPER_H-25-BASE_H-FLOOR;
        translate([-82.5, -27.5, SPIDER_STACK_H]) cylinder(d=26, h = 25.1);
        translate([-82.5, -19.2, SPIDER_STACK_H-0.4]) linear_extrude(1) text("Spider", size=3, font="Arial:style=Bold", halign="center");
        translate([-82.5, -38.5, SPIDER_STACK_H-0.4]) linear_extrude(1) text("Swarm", size=3, font="Arial:style=Bold", halign="center");

        // Cut out for upper tray
        translate([-100+BIG_TRAY_W/2, -100+BIG_TRAY_D/2, TOTAL_H/2-FLOOR-BASE_H+H_FOR_BIG_TRAY]) roundedBox([BIG_TRAY_W, BIG_TRAY_D, TOTAL_H], 5, true);
        translate([-100, -100, H_FOR_BIG_TRAY-FLOOR-BASE_H]) linear_extrude(h=TOTAL_H) polygon([[0, 0], [BIG_TRAY_W, 0], [BIG_TRAY_W, BIG_TRAY_D/2], [BIG_TRAY_W/2, BIG_TRAY_D],[0, BIG_TRAY_D]]);
    }

    // Corner peg to hold upper tray
    translate([-100+5, -100+5, H_FOR_BIG_TRAY-FLOOR-BASE_H]) #union() {
        cylinder(d=5, h=3);
        translate([0, 0, 3]) sphere(d=5);
    }
}
}

module x25mm(count=6) {
    start = -100+5+25/2;
    for (x=[-100+5+25/2:33:start + 33*count-1]){
        translate([x, 0, 0]) cylinder(h=TOTAL_H+6, d=26);
        translate([x, 0, 3]) cylinder(h=TOTAL_H+6, d=26+2);
        fingergrab(17);
    }
}

module fingergrab(d, l=200) {
    l = l + 0.1;
    translate([-l/2, 0, 10]) rotate([90, 0, 90]) linear_extrude(l) {
        translate([0, +d/2, 0]) circle(d=d);
        translate([-d/2, +d/2, 0]) square([d, TOTAL_H], center=false);
    }
}
