// **************************************************************
// **************************************************************
//   1. DEFINE BLOCK LAYOUT
//   -- Enable POINT LABLES IN VIEW
// **************************************************************
// **************************************************************


// --------------------------------------------------------------
//   Define the Cylinder Zone 
// --------------------------------------------------------------
r1 = 1^2;

Point(1) = {0, 0, 0, 1.0};
Point(2) = { Sqrt(r1/2), Sqrt(r1/2), 0, 1.0};
Point(3) = { Sqrt(r1/2),-Sqrt(r1/2), 0, 1.0};
Point(4) = {-Sqrt(r1/2), Sqrt(r1/2), 0, 1.0};
Point(5) = {-Sqrt(r1/2),-Sqrt(r1/2), 0, 1.0};

Circle(1) = {2, 1, 4};
Circle(2) = {4, 1, 5};
Circle(3) = {5, 1, 3};
Circle(4) = {3, 1, 2};

// --------------------------------------------------------------
//   Define the Cylinder BL Zone  
// --------------------------------------------------------------
r1 = 1.2^2; 

Point(6) = { Sqrt(r1/2), Sqrt(r1/2), 0, 1.0};
Point(7) = { Sqrt(r1/2),-Sqrt(r1/2), 0, 1.0};
Point(8) = {-Sqrt(r1/2), Sqrt(r1/2), 0, 1.0};
Point(9) = {-Sqrt(r1/2),-Sqrt(r1/2), 0, 1.0};

Circle(5) = {6, 1, 8};
Circle(6) = {8, 1, 9};
Circle(7) = {9, 1, 7};
Circle(8) = {7, 1, 6};

// Lines connecting the cylinder surface to the outer region
Line(9)  = {2,6};
Line(10) = {4,8};
Line(11) = {5,9};
Line(12) = {3,7};

// --------------------------------------------------------------
//   Cylinder Nearfield Square Zone  
// --------------------------------------------------------------
d1 = 5;

Point(10) = { d1, d1, 0, 1.0};
Point(11) = { d1,-d1, 0, 1.0};
Point(12) = {-d1, d1, 0, 1.0};
Point(13) = {-d1,-d1, 0, 1.0};

// Lines connecting the cylinder Outer surface to the outer square edge
Line(13) = {6,10};
Line(14) = {7,11};
Line(15) = {8,12};
Line(16) = {9,13};

// ..............................................................
// Circles used to distribute those cells more evently  
// across zones (i.e., the 5-point star region)
// ..............................................................
// Add reference points (ref=0 for circle, ref=infinity for lines)
ref = 60;
Point(101) = {-ref,   0, 0, 1.0};
Point(102) = { ref,   0, 0, 1.0};
Point(103) = {   0,-ref, 0, 1.0};
Point(104) = {   0, ref, 0, 1.0};

// Lines defining the outer regions of the central area
Circle(17) = {11,101,10};
Circle(18) = {13,102,12};
Circle(19) = {12,103,10};
Circle(20) = {13,104,11};


// --------------------------------------------------------------
//   Define the RECTANGULAR DOMAIN CORNERS (POINTS)
// --------------------------------------------------------------

// Build the outer edges 
dx = 10;
dy = 15;

// TOP LEFT ZONE 
Point(21) = {-d1-dx, d1   , 0, 1.0};
Point(22) = {-d1   , d1+dy, 0, 1.0};
Point(23) = {-d1-dx, d1+dy, 0, 1.0};

// BOTTOM LEFT ZONE 
Point(24) = {-d1-dx,-d1   , 0, 1.0};
Point(25) = {-d1   ,-d1-dy, 0, 1.0};
Point(26) = {-d1-dx,-d1-dy, 0, 1.0};

dx = dx*2.5;
// TOP RIGHT ZONE 
Point(27) = { d1+dx, d1   , 0, 1.0};
Point(28) = { d1   , d1+dy, 0, 1.0};
Point(29) = { d1+dx, d1+dy, 0, 1.0};

// BOTTOM RIGHTZONE 
Point(30) = { d1+dx,-d1   , 0, 1.0};
Point(31) = { d1   ,-d1-dy, 0, 1.0};
Point(32) = { d1+dx,-d1-dy, 0, 1.0};


// --------------------------------------------------------------
// COMPLETE THE GRID FOCUSING ONLY ON VERITCAL LINES 
// --------------------------------------------------------------

// (TOP) - aligned from Centre OUTWARDS
Line(21) = {21,23};
Line(22) = {12,22};
Line(23) = {10,28};
Line(24) = {27,29};

// (BOT) - aligned from Centre OUTWARDS
Line(26) = {24,26};
Line(27) = {13,25};
Line(28) = {11,31};
Line(29) = {30,32};

// (MID) - aligned from BOT to TOP
Line(30) = {24,21};
Line(31) = {30,27};


// --------------------------------------------------------------
// COMPLETE THE GRID FOCUSING ONLY ON HORIZONTAL LINES 
// --------------------------------------------------------------
 
// (TOP) - aligned from LEFT to RIGHT 
Line(32) = {23,22};
Line(34) = {22,28};
Line(35) = {28,29};

Line(36) = {21,12};
Line(37) = {10,27};

Line(39) = {24,13};
Line(40) = {11,30};

// (BOT) - aligned from LEFT to RIGHT 
Line(41) = {26,25};
Line(42) = {25,31};
Line(43) = {31,32};


// **************************************************************
// **************************************************************
//   2. DEFINE SURFACES (USE THE GUI)
//   -- Enable LINE LABLES IN VIEW ONLY 
//   -- GEO > ELEM > ADD > PLANE SURFACE
//   -- View updated script in here 
// **************************************************************
// **************************************************************

// --------------------------------------------------------------
// DEFINE PLANE SURFACES
// --------------------------------------------------------------
// Specific convention (notice sign changes)

Curve Loop(1) = {21, 32, -22, -36};
Plane Surface(1) = {1};
Curve Loop(2) = {22, 34, -23, -19};
Plane Surface(2) = {2};
Curve Loop(3) = {23, 35, -24, -37};
Plane Surface(3) = {3};
Curve Loop(4) = {26, 41, -27, -39};
Plane Surface(4) = {4};
Curve Loop(5) = {27, 42, -28, -20};
Plane Surface(5) = {5};
Curve Loop(6) = {28, 43, -29, -40};
Plane Surface(6) = {6};
Curve Loop(7) = {30, 36, -18, -39};
Plane Surface(7) = {7};
Curve Loop(8) = {18, -15, 6, 16};
Plane Surface(8) = {8};
Curve Loop(9) = {6, -11, -2, 10};
Plane Surface(9) = {9};
Curve Loop(10) = {4, 9, -8, -12};
Plane Surface(10) = {10};
Curve Loop(11) = {8, 13, -17, -14};
Plane Surface(11) = {11};
Curve Loop(12) = {16, 20, -14, -7};
Plane Surface(12) = {12};
Curve Loop(13) = {11, 7, -12, -3};
Plane Surface(13) = {13};
Curve Loop(14) = {10, -5, -9, 1};
Plane Surface(14) = {14};
Curve Loop(15) = {15, 19, -13, 5};
Plane Surface(15) = {15};
Curve Loop(16) = {17, 37, -31, -40};
Plane Surface(16) = {16};


// **************************************************************
// **************************************************************
//   3. DEFINE POINT DISTRIBUTION ALONG EDGES
// **************************************************************
// **************************************************************

// TOP VERTICAL EDGES GOING LEFT TO RIGHT 
Transfinite Curve {21, 22, 23, 24} = 16 Using Progression 1.105;

// BOT VERTICAL EDGES GOING LEFT TO RIGHT 
Transfinite Curve {26, 27, 28, 29} = 16 Using Progression 1.105;

// LEFT HORIZONTAL EDGES GOING TOP TO BOTTOM
Transfinite Curve {32, 36, 39, 41} = 16 Using Progression 0.9;

// RIGHT HORIZONTAL EDGES GOING TOP TO BOTTOM
Transfinite Curve {35, 37, 40, 43} = 70 Using Progression 1.01;


// ------------------------------------------------------------
//  Nearfield specific (dependent on cyl)
// ------------------------------------------------------------
// UPSTREAM REGION (going towards cyl surface)
Transfinite Curve {30, 18} = 51 Using Bump 1.0;
Transfinite Curve {6, 2} = 51 Using Progression 1.0;

// DOWNSTREAM REGION (going away from cyl surface)
Transfinite Curve {8, 4} = 51 Using Progression 1.0;
Transfinite Curve {17, 31} = 51 Using Bump 1.0;

// RADIALLY FROM CYLINDER IN BL
//Transfinite Curve {9, 10, 11, 12} = 27 Using Progression 1.25;
Transfinite Curve {9, 10, 11, 12} = 5 Using Progression 0.8;

// RADIALLY FROM CYLINDER OUTSIDE BL 
Transfinite Curve {13, 14, 15, 16} = 30 Using Progression 1.05;


// OVERHEAD REGION
Transfinite Curve {34, 19, 5, 1} = 51 Using Progression 1.0;
Transfinite Curve {42, 20, 7, 3} = 51 Using Progression 1.0;


// MASTER COMMAND TO SPECIFY STRUCTURED GRID IN SPECIFIC PLANEs
Transfinite Surface {1:16}; 
Recombine Surface {1:16};


// EXTRUDE MESH INTO 3-D GEOMETRY WITH SPAN OF 1 UNIT
Extrude {0, 0, 1} {
	Surface{1:16};
	Layers{1};
	Recombine;
}


Transfinite Surface "*";
Physical Volume("Fluid") = {1:16};
Transfinite Volume "*";
Recombine Surface "*";
Coherence;

// **************************************************************
// **************************************************************
//   4. SPECIFY BOUNDARY CONDITION PATCHES (DO WITH GUI)
//   -- Enable surface views, no need for any labels  
//   -- GEO > PHYS GROUPS > ADD > SURFACE
//   -- View updated script in here 
// **************************************************************
// **************************************************************
Physical Surface("inlet") = {52, 184, 118};
Physical Surface("outlet") = {104, 390, 170};
Physical Surface("topBot") = {56, 78, 100, 122, 144, 166};
Physical Surface("wall") = {350, 236, 328, 250};

Physical Surface("sides") = {65, 1, 87, 2, 109, 3, 197, 7, 219, 8, 373, 15, 285, 11, 395, 16, 175, 6, 153, 5, 131, 4, 307, 12, 329, 241, 351, 263, 9, 14, 10, 13};



//+
Show "*";
//+
Show "*";
//+
Show "*";
//+
Show "*";
//+
Show "*";
//+
Hide {
  Point{1}; Point{101}; Point{102}; Point{103}; Point{104}; Point{128}; Point{162}; Point{182}; Point{193}; Point{229}; 
}
