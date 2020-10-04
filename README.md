# Dungeons Dragons The Legend of Drizzt Board Game Organizer

This is the source code to generate the Legend of Drizzt Board Game Organizer on [Thingiverse](https://www.thingiverse.com/thing:4614298).

The `generate-inserts.py` file is the one that actually runs the code and will output everything into a `generated` folder. I have named things to include `x2` etc if 2 copies should be printed.

The `*-lid.scad` files are generally optional if you don't want lids on things, but I find them useful for keeping things in place.

The output `test.scad` file is a view of all of the items laid out in the box (to test if they would fit and show the correct layout).

## Mini Locations

The minis are placed mostly so they will fit, not in much of an order.

The trays have the names of the mini's at the bottom of each, but you can also use the `mini-outlines.svg` file to print out a legend if you want a printed copy (generally easier to read). This file was created in Inkscape if you want to modify it. See the next section for how it's used in the generation of the actual trays.

## How things were made

The mini outlines files were generated using the [Paths2OpenSCAD](https://github.com/sillyfrog/inkscape-paths2openscad) extension for Inkscape. I created a layer in Inkscape for each tray, and another layer with a photo of each of the minis to help me lay everything out and then put a path around where the cutouts should be. Once this was looking good I could then select just the correct layer and use the Paths2OpenSCAD to make the `mini-outlines-*.scad` files.

The `generate-inserts.py` file does all of the real work. This is a Python file using SolidPython which outputs OpenSCAD files. To use this, you'll need to link in the `MCAD` directory from OpenSCAD. On a Mac, this is done by running:

```
ln -s /Applications/OpenSCAD.app/Contents/Resources/libraries/MCAD
```
