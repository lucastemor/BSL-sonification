SynthDef.synthDefDir="/home/lucas/Documents/sonification/sonification_package/synths/synthdefs";

s.options.numWireBufs = 256;
s.options.memSize = 8 * 48*1024; // in KB (4*48 MB)

s.boot;

{Pan2.ar(SinOsc.ar(440))}.play;