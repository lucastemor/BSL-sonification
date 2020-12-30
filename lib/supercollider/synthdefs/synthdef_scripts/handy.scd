// Handy functions"

//SynthDef.synthDefDir= "/Users/Lucas/Documents/sonification/synths/synthdefs/";

//SynthDef.synthDefDir= "/Users/Lucas/Documents/motiongram/synthdefs/";

//SynthDef.synthDefDir="/Users/Lucas/Documents/sonification_fresh/synthdefs";
//SynthDef.synthDefDir="/Users/Lucas/Documents/spectrograms-master/sonification/synthdefs";

//SynthDef.synthDefDir="/Users/Lucas/Documents/spectrograms-master/sonification/synthdefs";


SynthDef.synthDefDir = "/home/lucas/Documents/sonification/sonification_package/synths/synthdefs";


// SynthDef.synthDefDir="" // Include your path here

s.options.numWireBufs = 256;
s.options.memSize = 8 * 48*1024; // in KB (4*48 MB)


//s.options.numWireBufs = 256
//s.options.memSize = 48 * 1024; // in KB (48 MB)

ServerOptions.devices;

Server.default.options.outDevice_("Built-in Output");
Server.default.options.outDevice_("Soundflower (2ch)");
s.reboot;


s.record(path: "/Users/Lucas/Documents/spectrograms-master/sonification/recording/test.wav".standardizePath);

s.stopRecording;


{Pan2.ar(SinOsc.ar(440))}.play;

pulseaudio -k && sudo alsa force-reload