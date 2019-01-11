use <large-parts-outlines.scad>;
use <MCAD/boxes.scad>
include <consts.scad>;

50MM_Y_OFFSETS = [70, 8];
50MM_X_OFFSETS = [200-195, 200-117];

module large_minis_tray() {
translate([UPPER_TRAY_W/2, UPPER_TRAY_D/2, FLOOR+BASE_H]) {
    difference() {
        translate([0, 0, UPPER_TRAY_H/2-FLOOR-BASE_H]) roundedBox([UPPER_TRAY_W, UPPER_TRAY_D, UPPER_TRAY_H], 5, true);

        translate([0, 0, 0]) upperoutlines();

        // 50mm bases
        for (i=[0:1]) {
            start = -100+5+20/2;
            y = -UPPER_TRAY_D/2+50/2+50MM_Y_OFFSETS[i];
            for (j=[0:1]){
                x = -UPPER_TRAY_W/2+50/2+50MM_X_OFFSETS[j];
                translate([x, y, -BASE_H]) cylinder(h=UPPER_TRAY_H+6, d=50);
                translate([x, y, 0]) cylinder(h=UPPER_TRAY_H+6, d=50+2);
            }
            translate([0, y, -BASE_H]) fingergrab(31);
        }
        // Corner peg to hold upper tray
        translate([-UPPER_TRAY_W/2+5, -UPPER_TRAY_D/2+5, -FLOOR-BASE_H-0.1]) union() {
            cylinder(d=6, h=4);
            translate([0, 0, 4]) sphere(d=6);
            // Show on the upper surface where to match the corner
            translate([0, 0, UPPER_TRAY_H]) sphere(d=5);
        }
    }
    for (i=[0:1]) {
        start = -100+5+20/2;
        y = -UPPER_TRAY_D/2+50/2+50MM_Y_OFFSETS[i];
        for (j=[0:1]){
            x = -UPPER_TRAY_W/2+50/2+50MM_X_OFFSETS[j];
            translate([x, y, -BASE_H]) largeputtext(j, i);
        }
    }
}
}

module largeputtext(x, y) {
    if (x == 0 && y == 0) {
        largesaytext("Dinin Do'urden");
    } else if (x == 1 && y == 0) {
        largesaytext("Shimmergloom");
    } else if (y == 1) {
        largesaytext("Feral Troll");
    }
}

module largesaytext(txt) {
    echo(txt);
    linear_extrude(0.6) color("blue") text(txt, size=4, halign="center", valign="center");
}

large_minis_tray();

module fingergrab(d, l=200) {
    l = l + 0.1;
    translate([-l/2, 0, UPPER_TRAY_H/3]) rotate([90, 0, 90]) linear_extrude(l) {
        translate([0, +d/2, 0]) circle(d=d);
        translate([-d/2, +d/2, 0]) square([d, UPPER_TRAY_H], center=false);
    }
}
