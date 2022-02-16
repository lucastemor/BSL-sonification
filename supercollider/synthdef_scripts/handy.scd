// Handy functions for setup etc. Eventually automate through python

//Set where synthdefs will be saved
SynthDef.synthDefDir = "/home/bsl/Documents/BSL-sonification/supercollider/synthdefs";

//set memory allocation -- this seems to work so far for everything
s.options.numWireBufs = 256;
s.options.memSize = 8 * 48*1024; // in KB (4*48 MB)

// These three lines are useful on MacOS for routing to soundflower for recording
ServerOptions.devices;
Server.default.options.outDevice_("Built-in Output");
Server.default.options.outDevice_("Soundflower (2ch)");
Server.default.options.outDevice_("Sonify");
Server.default.options.outDevice_("ScreenRecordwithAudio");

//Chnages wont' take effect until reboot
//If on Linux make sure supercollider is manually reconnected to PulseAudio JACK sources - instlal qjackctl
s.reboot;

//Test tone
{Pan2.ar(SinOsc.ar(440))}.play;

//Useful bash command if having issues on linux with audio - forcekill and restart pulseaudio
pulseaudio -k && sudo alsa force-reloads