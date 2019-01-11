include <consts.scad>;


module small_terrain_tiles_vertical() {
    difference() {
        union() {
            translate([0, 0, 0]) roundedCube([SMALL_TERRAIN_BOX_W, SMALL_TERRAIN_BOX_D, SMALL_TERRAIN_BOX_H], 5, true);
            echo([SMALL_TERRAIN_BOX_W, SMALL_TERRAIN_BOX_D, SMALL_TERRAIN_BOX_H], 5, true);
        }
        translate([TERRAIN_V_WALL, TERRAIN_V_WALL, TERRAIN_TAB_W]) roundedCube([SMALL_TERRAIN_BOX_W-TERRAIN_V_WALL*2, SMALL_TERRAIN_BOX_D-TERRAIN_V_WALL*2, SMALL_TERRAIN_BOX_H], 1, true);
        translate([TERRAIN_V_SUPPORT_W+TERRAIN_V_WALL, TERRAIN_V_WALL, -0.1]) cube([SMALL_TERRAIN_BOX_W-TERRAIN_V_SUPPORT_W*2-TERRAIN_V_WALL*2, SMALL_TERRAIN_BOX_D-TERRAIN_V_WALL*2, SMALL_TERRAIN_BOX_H], 5, true);
    }
    //#translate([TERRAIN_V_WALL, 2*SMALL_TERRAIN_TILES+TERRAIN_V_WALL, 0]) rotate([90, 0, 0]) small_terrain_tile(SMALL_TERRAIN_TILES);
}

module large_terrain_tiles_vertical() {
    difference() {
        union() {
            translate([0, 0, 0]) roundedCube([LARGE_TERRAIN_BOX_W, LARGE_TERRAIN_BOX_D, LARGE_TERRAIN_BOX_H], 5, true);
            echo([LARGE_TERRAIN_BOX_W, LARGE_TERRAIN_BOX_D, LARGE_TERRAIN_BOX_H], 5, true);
        }
        translate([TERRAIN_V_WALL, TERRAIN_V_WALL, TERRAIN_TAB_W]) roundedCube([LARGE_TERRAIN_BOX_W-TERRAIN_V_WALL*2, LARGE_TERRAIN_BOX_D-TERRAIN_V_WALL*2, LARGE_TERRAIN_BOX_H], 1, true);
        translate([TERRAIN_V_SUPPORT_W+TERRAIN_V_WALL, TERRAIN_V_WALL, -0.1]) cube([LARGE_TERRAIN_BOX_W-TERRAIN_V_SUPPORT_W*2-TERRAIN_V_WALL*2, LARGE_TERRAIN_BOX_D-TERRAIN_V_WALL*2, LARGE_TERRAIN_BOX_H], 5, true);
    }
    //#translate([TERRAIN_V_WALL, 2*LARGE_TERRAIN_TILES+TERRAIN_V_WALL, 0]) rotate([90, 0, 0]) large_terrain_tile(LARGE_TERRAIN_TILES);
}

module small_terrain_tiles() {
    difference() {
        union() {
            // Floor for the holder
            translate([0, 0, TERRAIN_SUPPORT-TERRAIN_FLOOR]) roundedCube([SMALL_TERRAIN_BASE_W, SMALL_TERRAIN_BASE_D, TERRAIN_FLOOR], 5, true);
            // Cubes for corner pegs, that are then cut out
            terrain_pegs(SMALL_TERRAIN_BASE_W/2, SMALL_TERRAIN_BASE_D, SMALL_TERRAIN_BASE_H);
            translate([SMALL_TERRAIN_BASE_W/2, 0, 0]) terrain_pegs(SMALL_TERRAIN_BASE_W/2, SMALL_TERRAIN_BASE_D, SMALL_TERRAIN_BASE_H);
            base_support(SMALL_TERRAIN_BASE_W, SMALL_TERRAIN_BASE_D);
            // A small peg to hold the tray above in place
            translate([SMALL_TERRAIN_BASE_W/2, 10, SMALL_TERRAIN_BASE_H]) cylinder(d=4, h=TERRAIN_SUPPORT);
            translate([SMALL_TERRAIN_BASE_W/2, SMALL_TERRAIN_BASE_D - 10, SMALL_TERRAIN_BASE_H]) cylinder(d=4, h=TERRAIN_SUPPORT);
        }
        // Thumb holes to get the last tiles out, offset to align with tile tab
        translate([0, SMALL_TERRAIN_BASE_D/2-10, -0.1]) cylinder(h=10, d=30);
        translate([SMALL_TERRAIN_BASE_W, SMALL_TERRAIN_BASE_D/2+10, -0.1]) cylinder(h=10, d=30);
    }
}

module large_terrain_tiles() {
    difference() {
        union() {
            // Floor for the holder
            translate([0, 0, TERRAIN_SUPPORT-TERRAIN_FLOOR]) roundedCube([LARGE_TERRAIN_BASE_W, LARGE_TERRAIN_BASE_D, TERRAIN_FLOOR], 5, true);
            // Cubes for corner pegs, that are then cut out
            terrain_pegs(LARGE_TERRAIN_BASE_W, LARGE_TERRAIN_BASE_D, LARGE_TERRAIN_BASE_H);
            base_support(LARGE_TERRAIN_BASE_W, LARGE_TERRAIN_BASE_D);
            // Support for the alignment holes
            translate([LARGE_TERRAIN_BASE_W/2, 10, 0]) cylinder(d=10, h=TERRAIN_SUPPORT);
            translate([LARGE_TERRAIN_BASE_W/2, LARGE_TERRAIN_BASE_D - 10, 0]) cylinder(d=10, h=TERRAIN_SUPPORT);
        }
        // Thumb holes to get the last tiles out, offset to align with tile tab
        translate([0, LARGE_TERRAIN_BASE_D/2-10, -0.1]) cylinder(h=10, d=30);
        // A small hole to align with the peg below
        translate([LARGE_TERRAIN_BASE_W/2, 10, -0.1]) cylinder(d=5, h=TERRAIN_SUPPORT+2);
        translate([LARGE_TERRAIN_BASE_W/2, LARGE_TERRAIN_BASE_D - 10, -0.1]) cylinder(d=5, h=TERRAIN_SUPPORT+2);
    }
}

module base_support(W, D) {
    // This is a grid that's on the base to improve strength, without using solid plastic everywhere
    spacing = 30;
    for (x=[spacing/2:spacing:W]) {
        translate([x, 0, 0]) cube([TERRAIN_SUPPORT, D, TERRAIN_SUPPORT]);
    }
    for (y=[spacing/2:spacing:D]) {
        translate([0, y, 0]) cube([W, TERRAIN_SUPPORT, TERRAIN_SUPPORT]);
    }
}

module terrain_pegs(W, D, H) {
    difference() {
        union() {
            roundedCube([W, D, H], 5, true);
        }
        translate([TERRAIN_WALL, TERRAIN_WALL, 0]) roundedCube([W-TERRAIN_WALL*2, D-TERRAIN_WALL*2, H+0.1], 5, true);
        translate([TERRAIN_PEG_EDGE, -0.01, 0]) cube([(W)-TERRAIN_PEG_EDGE*2, D+0.1, H+0.1]);
        translate([-0.01, TERRAIN_PEG_EDGE, 0]) cube([(W)+0.1, D-TERRAIN_PEG_EDGE*2, H+0.1]);
    }
}

module small_terrain_tile(count=1) {
    for (i=[0:count-1]) {
        color((i%2 == 1) ? "blue" : "red")
        translate([58, 58, 2*i]) mirror() linear_extrude(2) polygon(SMALL_TERRAIN_TILE_POINTS);
    }
}
module large_terrain_tile(count=1) {
    for (i=[0:count-1]) {
        color((i%2 == 1) ? "blue" : "red")
        translate([109, 58, 2*i]) rotate([0, 0, 90]) mirror() linear_extrude(2) polygon(LARGE_TERRAIN_TILE_POINTS);
    }
}

/*
small_terrain_tiles();
#translate([0, 0, TERRAIN_SUPPORT]) small_terrain_tile(34/2);
#translate([SMALL_TERRAIN_BASE_W/2, 0, TERRAIN_SUPPORT]) small_terrain_tile();

translate([0, 150, 0]) {
    large_terrain_tiles();
    #translate([0, 0, TERRAIN_SUPPORT]) large_terrain_tile(4);
}
*/

//small_terrain_tiles_vertical();
translate([150, 0, 0]) large_terrain_tiles_vertical();







function min_x(shape_points) = min([ for (x = shape_points) min(x[0])]);
function max_x(shape_points) = max([ for (x = shape_points) max(x[0])]);
function min_y(shape_points) = min([ for (x = shape_points) min(x[1])]);
function max_y(shape_points) = max([ for (x = shape_points) max(x[1])]);
echo(min_x(LARGE_TERRAIN_TILE_POINTS));
echo(min_y(LARGE_TERRAIN_TILE_POINTS));

SMALL_TERRAIN_TILE_POINTS = [[0.158923,57.470413],[-0.825423,56.789624],[-1.482859,55.790933],[-1.781982,55.074787],[-1.909269,54.413383],[-1.869424,53.734647],[-1.667147,52.966503],[-1.329913,52.127030],[-0.905831,51.462059],[0.580704,50.188713],[1.264915,49.452653],[1.484806,48.915684],[1.474476,48.062073],[1.203015,46.838803],[1.002407,46.346343],[0.748407,45.910413],[0.494407,45.537573],[0.145157,45.233893],[-0.685771,44.811993],[-1.060712,44.664279],[-1.860610,44.604179],[-7.094282,44.708853],[-14.625483,44.795553],[-16.523178,44.872853],[-17.092640,45.559529],[-17.735627,46.735963],[-19.733844,50.713533],[-20.293530,51.189873],[-30.851353,51.310443],[-45.178430,51.231310],[-50.506664,50.998443],[-50.824891,50.352063],[-51.021783,43.370463],[-51.208187,36.753193],[-51.195927,35.948003],[-51.075038,25.717463],[-51.070338,22.834793],[-51.039778,20.079123],[-51.464817,19.820643],[-55.352106,17.898596],[-56.823716,17.137963],[-57.232874,16.575885],[-57.390499,14.875585],[-57.385633,8.629708],[-57.313460,2.723272],[-57.176738,0.698467],[-56.504512,-0.591631],[-55.733362,-1.503507],[-54.890360,-1.809141],[-53.924757,-1.952860],[-52.966864,-1.926699],[-52.146992,-1.722694],[-50.715946,-0.522569],[-49.704087,0.382587],[-48.784823,0.881828],[-47.852843,1.010899],[-46.802831,0.805543],[-46.129650,0.487387],[-45.444281,-0.063583],[-44.765505,-0.911357],[-44.516002,-2.159033],[-44.526672,-9.334533],[-44.580112,-12.192033],[-44.587012,-15.049533],[-44.669840,-16.547024],[-44.864203,-16.809370],[-45.269491,-17.070023],[-47.702017,-18.385113],[-50.227498,-19.707188],[-50.634231,-20.004026],[-50.813517,-20.265486],[-50.975839,-21.897930],[-51.039757,-27.931826],[-51.214057,-35.393076],[-51.229297,-35.560033],[-51.218047,-36.274733],[-51.264005,-36.975142],[-51.145397,-37.639983],[-50.995451,-39.132705],[-50.945768,-43.053033],[-50.867700,-48.785912],[-50.643541,-50.788846],[-50.053799,-51.253505],[-48.665207,-51.529081],[-46.228653,-51.640797],[-42.495022,-51.613875],[-29.955545,-51.535668],[-21.303802,-51.663445],[-20.371792,-51.817674],[-19.845812,-52.035746],[-18.494529,-54.304365],[-17.403048,-56.388033],[-17.034103,-56.984718],[-16.662573,-57.503960],[-16.229502,-57.637525],[-14.286351,-57.751070],[-8.627832,-57.785033],[-1.394468,-57.681814],[-0.120893,-57.461112],[0.609470,-57.046191],[1.252333,-56.474763],[1.708296,-55.678623],[2.118836,-54.265539],[1.986199,-52.922727],[1.324868,-51.697034],[0.149325,-50.635310],[-0.657741,-50.001532],[-1.097643,-49.318125],[-1.349742,-48.594584],[-1.415040,-47.896447],[-1.294207,-47.240049],[-0.987913,-46.641727],[-0.327987,-45.920225],[0.127413,-45.568550],[0.954580,-45.149833],[2.613605,-44.919709],[10.034992,-44.919993],[15.854205,-45.152899],[16.763089,-45.382806],[17.119004,-45.783533],[17.735845,-46.758915],[18.147484,-47.441884],[19.998815,-50.764508],[20.539467,-51.065433],[21.512984,-51.330150],[34.668689,-51.491066],[48.563979,-51.408620],[50.292109,-51.161991],[51.080279,-50.726100],[51.274461,-50.422979],[51.353677,-49.586611],[51.223959,-43.434035],[51.129059,-33.147035],[51.091159,-26.643168],[51.072139,-21.623631],[51.235399,-20.394650],[51.848530,-19.935887],[53.178279,-19.225395],[56.052217,-17.725585],[56.694141,-17.267276],[57.053639,-16.851706],[57.390499,-16.332192],[57.390499,-8.217057],[57.309245,-0.556162],[57.083530,0.542380],[56.624069,1.171695],[55.598579,1.928664],[54.282569,2.368667],[53.663425,2.359325],[52.895309,2.047994],[51.657329,1.137504],[50.566106,-0.105531],[49.738522,-0.837503],[48.982614,-1.189861],[48.106419,-1.294055],[47.108131,-1.181603],[46.223431,-0.806550],[45.482480,-0.187341],[44.915439,0.657579],[44.663307,1.291888],[44.519044,2.159333],[44.416229,6.095965],[44.277439,9.612097],[44.288639,9.994066],[44.426519,13.047347],[44.552289,16.163096],[44.979935,16.681406],[46.727319,17.628994],[49.537381,19.120952],[50.505039,19.897853],[51.049119,20.481113],[51.035319,27.353793],[51.022819,34.861463],[51.018819,39.369963],[51.047419,46.991963],[50.988156,50.648369],[50.797823,51.207885],[50.433519,51.401713],[43.442299,51.491204],[28.309139,51.422813],[20.329861,51.411613],[20.057690,51.568902],[19.828389,51.896253],[19.513423,52.324033],[19.472043,52.436643],[19.352539,52.706193],[19.163441,53.005213],[17.739951,56.070533],[16.863605,57.435783],[16.492434,57.785033],[8.588686,57.767933],[1.611097,57.717852],[0.587801,57.632715],[0.158955,57.470483],[0.158923,57.470413]];
LARGE_TERRAIN_TILE_POINTS = [[1.851202,108.682148],[0.120473,108.405568],[-0.994618,107.720688],[-1.838477,106.629218],[-2.146811,105.850702],[-2.212797,104.881588],[-2.148445,103.974291],[-1.903243,103.220655],[-1.398975,102.462955],[-0.557427,101.543468],[0.392983,100.492768],[0.914195,99.646351],[1.071961,98.844607],[0.932033,97.927928],[0.662800,97.311678],[0.112392,96.667378],[-0.558252,96.095584],[-1.363763,95.803690],[-2.726868,95.718122],[-5.070297,95.765308],[-12.514758,95.860008],[-16.993786,95.983818],[-17.454775,96.399818],[-17.706497,96.910098],[-17.961608,97.354598],[-18.173727,97.767348],[-18.490419,98.260728],[-18.722801,98.841828],[-19.040301,99.418348],[-19.357800,99.909138],[-19.801323,100.970041],[-20.490426,101.920738],[-21.654352,102.225113],[-23.009489,102.187428],[-23.707988,102.179428],[-29.617769,102.326538],[-35.693385,102.472878],[-36.073006,102.523466],[-36.582104,102.404478],[-38.280490,102.248095],[-43.863494,102.212768],[-50.580312,102.212768],[-50.956491,101.896228],[-51.269410,101.515728],[-51.424357,100.975478],[-51.513627,85.744048],[-51.544184,73.347815],[-51.607299,71.425463],[-51.722256,70.938288],[-54.282795,69.474258],[-56.653024,68.202266],[-57.469264,67.572798],[-57.835202,67.156018],[-57.834554,59.713538],[-57.797937,53.446311],[-57.630250,51.460278],[-57.350053,50.660762],[-56.944400,49.964567],[-56.430088,49.394805],[-55.823916,48.974588],[-55.054921,48.677823],[-53.919036,48.627688],[-52.482266,48.722888],[-51.518814,49.531018],[-50.262954,50.625790],[-49.201464,51.232331],[-48.142553,51.422723],[-46.894430,51.269048],[-46.240834,51.034528],[-45.633985,50.538798],[-45.119881,49.915577],[-44.951563,49.126718],[-44.874223,41.316218],[-44.888723,34.331218],[-45.202297,34.074008],[-47.200583,32.957578],[-50.318348,31.274727],[-50.820257,30.819169],[-51.045031,30.328488],[-51.212164,28.778547],[-51.239045,23.766358],[-51.179785,16.932218],[-51.113385,7.077608],[-51.132525,-0.018838],[-51.248953,-2.225142],[-51.338021,-2.557517],[-51.258963,-2.877472],[-51.035521,-16.943422],[-50.998340,-28.978711],[-51.065660,-30.567905],[-51.211977,-30.926131],[-55.892464,-33.396486],[-56.761130,-33.988536],[-57.169204,-34.456648],[-57.323334,-35.266567],[-57.376218,-42.426613],[-57.271364,-49.834490],[-56.936135,-51.112049],[-56.152731,-52.209658],[-55.129400,-52.941123],[-53.774799,-53.153341],[-52.821338,-53.138631],[-52.149409,-52.988230],[-51.536266,-52.610617],[-50.759159,-51.914268],[-49.832555,-51.072257],[-49.149676,-50.613169],[-48.469699,-50.422118],[-47.551799,-50.384224],[-46.472054,-50.437884],[-45.810395,-50.667075],[-44.987285,-51.231282],[-44.733415,-51.682525],[-44.561374,-52.396778],[-44.392896,-55.065057],[-44.342083,-60.137617],[-44.299733,-67.357447],[-44.687516,-67.644878],[-47.489951,-68.983647],[-47.795800,-69.162068],[-49.045348,-69.874535],[-50.182386,-70.611356],[-50.674491,-71.460147],[-50.823887,-83.715647],[-50.889427,-98.460396],[-50.807150,-101.382199],[-50.590906,-101.917178],[-50.187677,-102.210242],[-49.425701,-102.404854],[-47.945890,-102.539264],[-42.408301,-102.651553],[-28.692301,-102.592643],[-20.836847,-102.629167],[-19.680779,-102.864931],[-19.207378,-103.337151],[-18.622981,-104.289651],[-17.654877,-106.131151],[-16.512281,-107.932697],[-15.992406,-108.303244],[-15.352462,-108.477612],[-11.218903,-108.755458],[-5.895798,-108.798760],[-1.855039,-108.613032],[-0.006808,-108.288862],[0.868735,-107.728539],[1.579966,-106.899494],[2.057361,-105.908205],[2.231392,-104.861151],[2.089753,-103.591151],[1.995253,-103.083016],[1.431063,-102.289266],[0.723673,-101.495651],[-0.024997,-100.916642],[-0.768297,-99.915213],[-1.045053,-98.743496],[-0.829785,-97.641859],[-0.179070,-96.741116],[0.850513,-96.172080],[3.388309,-95.885207],[9.090243,-95.741061],[14.499045,-95.766568],[16.855183,-96.017332],[17.554684,-96.863579],[19.141833,-99.834883],[20.074733,-101.312807],[20.418465,-101.624050],[20.952972,-101.858487],[23.611510,-102.139611],[30.084755,-102.241509],[42.407113,-102.249511],[48.722018,-102.210014],[50.343003,-102.012712],[50.832841,-101.764218],[51.160750,-101.431568],[51.520683,-100.225651],[51.654920,-90.312730],[51.580283,-80.935405],[51.500083,-76.103558],[51.518170,-72.263113],[51.653183,-71.201746],[53.857803,-69.991400],[56.487379,-68.539000],[57.132744,-68.051031],[57.504433,-67.609120],[57.794803,-67.142151],[57.835203,-59.903151],[57.790458,-52.839667],[57.627657,-51.474101],[57.318543,-50.604124],[56.589751,-49.625279],[55.530010,-48.968859],[54.281858,-48.692476],[52.987832,-48.853740],[51.819321,-49.487499],[50.734023,-50.648819],[50.161091,-51.270963],[49.383463,-51.725383],[48.006939,-52.112372],[47.378050,-52.060349],[46.735363,-51.847101],[45.837433,-51.298367],[45.178003,-50.441651],[44.840843,-49.870151],[44.848843,-42.631151],[44.949943,-34.915399],[45.079000,-34.521072],[45.335138,-34.188630],[46.484463,-33.468139],[48.280483,-32.527544],[49.714282,-31.889415],[50.222962,-31.636235],[50.667653,-31.147785],[51.180313,-30.312151],[51.246313,-21.739651],[51.222813,-11.579642],[51.170312,13.629858],[51.129155,24.339814],[51.226616,29.387831],[51.380195,30.491317],[51.631868,31.022564],[52.002781,31.262654],[52.514083,31.492668],[53.921192,32.295288],[55.318192,33.136238],[56.724307,34.117571],[57.352342,34.972378],[57.430442,42.425258],[57.269175,49.457647],[57.076371,50.731905],[56.746993,51.315448],[56.461242,51.757248],[56.048493,52.161128],[55.276043,52.667218],[54.183794,53.046016],[53.072863,53.114688],[51.138123,52.130488],[50.324733,51.221858],[49.707140,50.556424],[49.125639,50.129680],[48.486329,49.890400],[47.695312,49.787358],[46.849826,49.788192],[46.325662,49.939228],[45.371132,50.657250],[44.689302,51.651128],[44.472864,52.148732],[44.373246,53.172213],[44.379173,61.333288],[44.434981,65.884105],[44.560443,67.329748],[46.999743,68.699378],[49.496778,70.053048],[50.458293,70.847008],[50.674338,71.546491],[50.800631,73.260848],[50.867713,82.019358],[50.796789,97.423981],[50.710498,100.571022],[50.575723,101.665708],[50.166259,102.119530],[49.476243,102.389518],[41.348243,102.541838],[33.417093,102.735068],[32.964281,102.843857],[32.515393,102.730068],[26.010960,102.576905],[19.522203,102.663268],[18.631703,104.371578],[17.916563,105.747028],[17.345243,106.920368],[16.741488,107.825218],[15.942943,108.692418],[9.521543,108.798760],[1.851243,108.682418],[1.851202,108.682148]];