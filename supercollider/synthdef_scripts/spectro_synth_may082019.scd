// spectrogram reader
// one of several synthdefs used for sonifying full synthdef

(
SynthDef(\spectro_05082019, {
	arg out=0, fr_000 = 440.0;
	var sig;

	sig = SinOsc.ar(fr_000,0,1,0);

	sig = Limiter.ar(sig,1,0.01);
	Out.ar(out, Pan2.ar(sig));
	}).store;
)

x = Synth(\spectro_05082019)

////////////////////////////////////
(
SynthDef(\spectro_05082019, {
	arg out=0,
	pxx_000 = 0.0001,
	pxx_001 = 0.6,
	pxx_002 = 0.8,
	pxx_003 = 0.1,
	pxx_004 = 0.01,
	fr_000 = 440.00,
	gate = 1.0,
	timestretch = 1.0;

	var time, pxx, env, sig ;
	pxx = [pxx_000, pxx_001, pxx_002, pxx_003, pxx_004];
	time = timestretch*(0.951/(pxx.size)); // cycle length = 0.951
	env = EnvGen.kr(Env(pxx,[time]), gate, 1,0,1,2);

	// sig = SinOsc.ar(fr_000,0,1,0);
	sig = (FreeVerb.ar({SinOsc.ar(fr_000,pi.rand,0.2) + PMOsc.ar(fr_000,4*env*fr_000,env*5,0,0.2)}!2,0.33,0.75));
	sig = env*sig;
	sig = Limiter.ar(sig,1,0.01);
	Out.ar(out, Pan2.ar(sig));

}).store;
)

x = Synth(\spectro_05082019, [\fr_000,220]);
x = Synth(\spectro_05082019, [\fr_000,440, \pxx_002,0.001, \timestretch,5.0]);
x.set(\gate,1.0)

////////////////////////////////////
////////////////////////////////////
(
SynthDef(\spectro_05082019, {
	arg out=0,
	pxx_000 = 0.000000001,
	pxx_001 = 0.000000001,
	pxx_002 = 0.000000001,
	pxx_003 = 0.000000001,
	pxx_004 = 0.000000001,
	pxx_005 = 0.000000001,
	pxx_006 = 0.000000001,
	pxx_007 = 0.000000001,
	pxx_008 = 0.000000001,
	pxx_009 = 0.000000001,
	pxx_010 = 0.000000001,
	pxx_011 = 0.000000001,
	pxx_012 = 0.000000001,
	pxx_013 = 0.000000001,
	pxx_014 = 0.000000001,
	pxx_015 = 0.000000001,
	pxx_016 = 0.000000001,
	pxx_017 = 0.000000001,
	pxx_018 = 0.000000001,
	pxx_019 = 0.000000001,
	pxx_020 = 0.000000001,
	pxx_021 = 0.000000001,
	pxx_022 = 0.000000001,
	pxx_023 = 0.000000001,
	pxx_024 = 0.000000001,
	pxx_025 = 0.000000001,
	pxx_026 = 0.000000001,
	pxx_027 = 0.000000001,
	pxx_028 = 0.000000001,
	pxx_029 = 0.000000001,
	pxx_030 = 0.000000001,
	pxx_031 = 0.000000001,
	pxx_032 = 0.000000001,
	pxx_033 = 0.000000001,
	pxx_034 = 0.000000001,
	pxx_035 = 0.000000001,

	ph_000 = 0.0001,
	ph_001 = 0.0001,
	ph_002 = 0.0001,
	ph_003 = 0.0001,
	ph_004 = 0.0001,
	ph_005 = 0.0001,
	ph_006 = 0.0001,
	ph_007 = 0.0001,
	ph_008 = 0.0001,
	ph_009 = 0.0001,
	ph_010 = 0.0001,
	ph_011 = 0.0001,
	ph_012 = 0.0001,
	ph_013 = 0.0001,
	ph_014 = 0.0001,
	ph_015 = 0.0001,
	ph_016 = 0.0001,
	ph_017 = 0.0001,
	ph_018 = 0.0001,
	ph_019 = 0.0001,
	ph_020 = 0.0001,
	ph_021 = 0.0001,
	ph_022 = 0.0001,
	ph_023 = 0.0001,
	ph_024 = 0.0001,
	ph_025 = 0.0001,
	ph_026 = 0.0001,
	ph_027 = 0.0001,
	ph_028 = 0.0001,
	ph_029 = 0.0001,
	ph_030 = 0.0001,
	ph_031 = 0.0001,
	ph_032 = 0.0001,
	ph_033 = 0.0001,
	ph_034 = 0.0001,
	ph_035 = 0.0001,

	fr_000 = 440.00,
	gate = 0.0,
	timestretch = 1.0;

	var time, pxx, env, sig, phase, phase_env;
	pxx = [pxx_000, pxx_001, pxx_002, pxx_003, pxx_004, pxx_005, pxx_006, pxx_007, pxx_008, pxx_009, pxx_010, pxx_011, pxx_012, pxx_013, pxx_014, pxx_015, pxx_016, pxx_017, pxx_018, pxx_019, pxx_020, pxx_021, pxx_022, pxx_023, pxx_024, pxx_025, pxx_026, pxx_027, pxx_028, pxx_029, pxx_030, pxx_031, pxx_032, pxx_033, pxx_034, pxx_035];

	phase = [ph_000, ph_001, ph_002, ph_003, ph_004, ph_005, ph_006, ph_007, ph_008, ph_009, ph_010, ph_011, ph_012, ph_013, ph_014, ph_015, ph_016, ph_017, ph_018, ph_019, ph_020, ph_021, ph_022, ph_023, ph_024, ph_025, ph_026, ph_027, ph_028, ph_029, ph_030, ph_031, ph_032, ph_033, ph_034, ph_035];

	time = timestretch*(1..0/(pxx.size));
	env = EnvGen.kr(Env(pxx,[time]), gate, 1,0,1,0); // setting doneaction to 0 lets us use the gate to control on/off

	phase_env = EnvGen.kr(Env(phase,[time]), gate, 1,0,1,0);

	// Plain old sine wave:
	sig = SinOsc.ar(fr_000,phase_env,1,0);

	sig = (env*sig);
	sig = Limiter.ar(sig,1,0.01);
	Out.ar(out, Pan2.ar(sig));

}).store;
)

x = Synth(\spectro_05082019, [\fr_000,440,\gate,1,\pxx_001,0.5]);

x = Synth(\spectro_05082019, [\fr_000,440, \pxx_002,0.3, \timestretch,5.0]);










////////////////////////////////////


(
SynthDef(\spectro_image, {
	arg out=0,
	pxx_000 = 0.000000001,
	pxx_001 = 0.000000001,
	pxx_002 = 0.000000001,
	pxx_003 = 0.000000001,
	pxx_004 = 0.000000001,
	pxx_005 = 0.000000001,
	pxx_006 = 0.000000001,
	pxx_007 = 0.000000001,
	pxx_008 = 0.000000001,
	pxx_009 = 0.000000001,
	pxx_010 = 0.000000001,
	pxx_011 = 0.000000001,
	pxx_012 = 0.000000001,
	pxx_013 = 0.000000001,
	pxx_014 = 0.000000001,
	pxx_015 = 0.000000001,
	pxx_016 = 0.000000001,
	pxx_017 = 0.000000001,
	pxx_018 = 0.000000001,
	pxx_019 = 0.000000001,
	pxx_020 = 0.000000001,
	pxx_021 = 0.000000001,
	pxx_022 = 0.000000001,
	pxx_023 = 0.000000001,
	pxx_024 = 0.000000001,
	pxx_025 = 0.000000001,
	pxx_026 = 0.000000001,
	pxx_027 = 0.000000001,
	pxx_028 = 0.000000001,
	pxx_029 = 0.000000001,
	pxx_030 = 0.000000001,
	pxx_031 = 0.000000001,
	pxx_032 = 0.000000001,
	pxx_033 = 0.000000001,
	pxx_034 = 0.000000001,
	pxx_035 = 0.000000001,

	cut_000 = 0.0000001,
	cut_001 = 0.0000001,
	cut_002 = 0.0000001,
	cut_003 = 0.0000001,
	cut_004 = 0.0000001,
	cut_005 = 0.0000001,
	cut_006 = 0.0000001,
	cut_007 = 0.0000001,
	cut_008 = 0.0000001,
	cut_009 = 0.0000001,
	cut_010 = 0.0000001,
	cut_011 = 0.0000001,
	cut_012 = 0.0000001,
	cut_013 = 0.0000001,
	cut_014 = 0.0000001,
	cut_015 = 0.0000001,
	cut_016 = 0.0000001,
	cut_017 = 0.0000001,
	cut_018 = 0.0000001,
	cut_019 = 0.0000001,
	cut_020 = 0.0000001,
	cut_021 = 0.0000001,
	cut_022 = 0.0000001,
	cut_023 = 0.0000001,
	cut_024 = 0.0000001,
	cut_025 = 0.0000001,
	cut_026 = 0.0000001,
	cut_027 = 0.0000001,
	cut_028 = 0.0000001,
	cut_029 = 0.0000001,
	cut_030 = 0.0000001,
	cut_031 = 0.0000001,
	cut_032 = 0.0000001,
	cut_033 = 0.0000001,
	cut_034 = 0.0000001,
	cut_035 = 0.0000001,

	ph_000 = 0.0001,
	ph_001 = 0.0001,
	ph_002 = 0.0001,
	ph_003 = 0.0001,
	ph_004 = 0.0001,
	ph_005 = 0.0001,
	ph_006 = 0.0001,
	ph_007 = 0.0001,
	ph_008 = 0.0001,
	ph_009 = 0.0001,
	ph_010 = 0.0001,
	ph_011 = 0.0001,
	ph_012 = 0.0001,
	ph_013 = 0.0001,
	ph_014 = 0.0001,
	ph_015 = 0.0001,
	ph_016 = 0.0001,
	ph_017 = 0.0001,
	ph_018 = 0.0001,
	ph_019 = 0.0001,
	ph_020 = 0.0001,
	ph_021 = 0.0001,
	ph_022 = 0.0001,
	ph_023 = 0.0001,
	ph_024 = 0.0001,
	ph_025 = 0.0001,
	ph_026 = 0.0001,
	ph_027 = 0.0001,
	ph_028 = 0.0001,
	ph_029 = 0.0001,
	ph_030 = 0.0001,
	ph_031 = 0.0001,
	ph_032 = 0.0001,
	ph_033 = 0.0001,
	ph_034 = 0.0001,
	ph_035 = 0.0001,

	fr_000 = 440.00,
	gate = 0.0,
	timestretch = 1.0;

	var time, pxx, amp_env,freq_env, sig,pitched,noise, phase, phase_env,cut,lowpass;

	pxx = [pxx_000, pxx_001, pxx_002, pxx_003, pxx_004, pxx_005, pxx_006, pxx_007, pxx_008, pxx_009, pxx_010, pxx_011, pxx_012, pxx_013, pxx_014, pxx_015, pxx_016, pxx_017, pxx_018, pxx_019, pxx_020, pxx_021, pxx_022, pxx_023, pxx_024, pxx_025, pxx_026, pxx_027, pxx_028, pxx_029, pxx_030, pxx_031, pxx_032, pxx_033, pxx_034, pxx_035];

	cut = [cut_000, cut_001, cut_002, cut_003, cut_004, cut_005, cut_006, cut_007, cut_008, cut_009, cut_010, cut_011, cut_012, cut_013, cut_014, cut_015, cut_016, cut_017, cut_018, cut_019, cut_020, cut_021, cut_022, cut_023, cut_024, cut_025, cut_026, cut_027, cut_028, cut_029, cut_030, cut_031, cut_032, cut_033, cut_034, cut_035];

	phase = [ph_000, ph_001, ph_002, ph_003, ph_004, ph_005, ph_006, ph_007, ph_008, ph_009, ph_010, ph_011, ph_012, ph_013, ph_014, ph_015, ph_016, ph_017, ph_018, ph_019, ph_020, ph_021, ph_022, ph_023, ph_024, ph_025, ph_026, ph_027, ph_028, ph_029, ph_030, ph_031, ph_032, ph_033, ph_034, ph_035];

	time = timestretch*(1.0/(pxx.size));

	amp_env = EnvGen.kr(Env(pxx,[time]), gate, 1,0,1,0); // setting doneaction to 0 lets us use the gate to control on/off
	freq_env = EnvGen.kr(Env(cut,[time]),gate, 1,0,1,0);
	phase_env = EnvGen.kr(Env(phase,[time]), gate, 1,0,1,0);

	//pitched = LFTri.ar(fr_000/2,0,SinOsc.ar(fr_000/2,0,1,0), 0);
	//pitched = SinOsc.ar(fr_000,0,1, SinOsc.ar(fr_000+10,0,1,0));
	//pitched = SinOsc.ar(fr_000,0,SinOsc.ar(10,0,1,0),0);

	pitched = SinOsc.ar(fr_000,0,0.75,0);



	//pitched = SinOsc.ar(220,0,0.2,SinOsc.ar(220*1.25,0,0.2,SinOsc.ar(220*1.5,0,0.2,SinOsc.ar(440,0,0.2,0))));
	//pitched = SinOsc.ar(Vibrato.ar(DC.ar(fr_000),5,0.1) );
	noise =PinkNoise.ar(1,0);
	noise = ((amp_env+3)/4)*noise;

	noise = BLowPass4.ar(noise,freq_env,1,1,0);
	//noise = LPF.ar(noise,freq_env,1,0);
	//noise = lowpass*noise;
	//noise = (freq_env*noise);
	//pitched = Klank.ar(`[[fr_000,fr_000*1.25,fr_000*2],nil,[timestretch,timestretch,timestretch]],pitched,1,0,1);

	pitched = (amp_env*pitched);

	sig = pitched;//+noise;

	sig = Limiter.ar(sig,1,0.01);
	Out.ar(out, Pan2.ar(sig));

}).store;
)


(
SynthDef(\spectro_blob, {
	arg out=0,
	pxx_000 = 0.000000001,
	pxx_001 = 0.000000001,
	pxx_002 = 0.000000001,
	pxx_003 = 0.000000001,
	pxx_004 = 0.000000001,
	pxx_005 = 0.000000001,
	pxx_006 = 0.000000001,
	pxx_007 = 0.000000001,
	pxx_008 = 0.000000001,
	pxx_009 = 0.000000001,
	pxx_010 = 0.000000001,
	pxx_011 = 0.000000001,
	pxx_012 = 0.000000001,
	pxx_013 = 0.000000001,
	pxx_014 = 0.000000001,
	pxx_015 = 0.000000001,
	pxx_016 = 0.000000001,
	pxx_017 = 0.000000001,
	pxx_018 = 0.000000001,
	pxx_019 = 0.000000001,
	pxx_020 = 0.000000001,
	pxx_021 = 0.000000001,
	pxx_022 = 0.000000001,
	pxx_023 = 0.000000001,
	pxx_024 = 0.000000001,
	pxx_025 = 0.000000001,
	pxx_026 = 0.000000001,
	pxx_027 = 0.000000001,
	pxx_028 = 0.000000001,
	pxx_029 = 0.000000001,
	pxx_030 = 0.000000001,
	pxx_031 = 0.000000001,
	pxx_032 = 0.000000001,
	pxx_033 = 0.000000001,
	pxx_034 = 0.000000001,
	pxx_035 = 0.000000001,

	cut_000 = 1,
	cut_001 = 1,
	cut_002 = 1,
	cut_003 = 1,
	cut_004 = 1,
	cut_005 = 1,
	cut_006 = 1,
	cut_007 = 1,
	cut_008 = 1,
	cut_009 = 1,
	cut_010 = 1,
	cut_011 = 1,
	cut_012 = 1,
	cut_013 = 1,
	cut_014 = 1,
	cut_015 = 1,
	cut_016 = 1,
	cut_017 = 1,
	cut_018 = 1,
	cut_019 = 1,
	cut_020 = 1,
	cut_021 = 1,
	cut_022 = 1,
	cut_023 = 1,
	cut_024 = 1,
	cut_025 = 1,
	cut_026 = 1,
	cut_027 = 1,
	cut_028 = 1,
	cut_029 = 1,
	cut_030 = 1,
	cut_031 = 1,
	cut_032 = 1,
	cut_033 = 1,
	cut_034 = 1,
	cut_035 = 1,

	ph_000 = 0.0001,
	ph_001 = 0.0001,
	ph_002 = 0.0001,
	ph_003 = 0.0001,
	ph_004 = 0.0001,
	ph_005 = 0.0001,
	ph_006 = 0.0001,
	ph_007 = 0.0001,
	ph_008 = 0.0001,
	ph_009 = 0.0001,
	ph_010 = 0.0001,
	ph_011 = 0.0001,
	ph_012 = 0.0001,
	ph_013 = 0.0001,
	ph_014 = 0.0001,
	ph_015 = 0.0001,
	ph_016 = 0.0001,
	ph_017 = 0.0001,
	ph_018 = 0.0001,
	ph_019 = 0.0001,
	ph_020 = 0.0001,
	ph_021 = 0.0001,
	ph_022 = 0.0001,
	ph_023 = 0.0001,
	ph_024 = 0.0001,
	ph_025 = 0.0001,
	ph_026 = 0.0001,
	ph_027 = 0.0001,
	ph_028 = 0.0001,
	ph_029 = 0.0001,
	ph_030 = 0.0001,
	ph_031 = 0.0001,
	ph_032 = 0.0001,
	ph_033 = 0.0001,
	ph_034 = 0.0001,
	ph_035 = 0.0001,

	fr_000 = 440.00,
	gate = 0.0,
	timestretch = 1.0;

	var time, pxx, amp_env,freq_env, sig,pitched,noise, pitch, pitch_env,cut,lowpass;

	pxx = [pxx_000, pxx_001, pxx_002, pxx_003, pxx_004, pxx_005, pxx_006, pxx_007, pxx_008, pxx_009, pxx_010, pxx_011, pxx_012, pxx_013, pxx_014, pxx_015, pxx_016, pxx_017, pxx_018, pxx_019, pxx_020, pxx_021, pxx_022, pxx_023, pxx_024, pxx_025, pxx_026, pxx_027, pxx_028, pxx_029, pxx_030, pxx_031, pxx_032, pxx_033, pxx_034, pxx_035];

	cut = [cut_000, cut_001, cut_002, cut_003, cut_004, cut_005, cut_006, cut_007, cut_008, cut_009, cut_010, cut_011, cut_012, cut_013, cut_014, cut_015, cut_016, cut_017, cut_018, cut_019, cut_020, cut_021, cut_022, cut_023, cut_024, cut_025, cut_026, cut_027, cut_028, cut_029, cut_030, cut_031, cut_032, cut_033, cut_034, cut_035];

	pitch = [ph_000, ph_001, ph_002, ph_003, ph_004, ph_005, ph_006, ph_007, ph_008, ph_009, ph_010, ph_011, ph_012, ph_013, ph_014, ph_015, ph_016, ph_017, ph_018, ph_019, ph_020, ph_021, ph_022, ph_023, ph_024, ph_025, ph_026, ph_027, ph_028, ph_029, ph_030, ph_031, ph_032, ph_033, ph_034, ph_035];

	time = timestretch*(1.0/(pxx.size));

	amp_env = EnvGen.kr(Env(pxx,[time]), gate, 1,0,1,0); // setting doneaction to 0 lets us use the gate to control on/off
	freq_env = EnvGen.kr(Env(cut,[time]),gate, 1,0,1,0);
	pitch_env = EnvGen.kr(Env(pitch,[time]), gate, 1,0,1,0);

	//pitched = LFTri.ar(fr_000/2,0,SinOsc.ar(fr_000/2,0,1,0), 0);
	//pitched = SinOsc.ar(fr_000,0,1, SinOsc.ar(fr_000+10,0,1,0));
	//pitched = SinOsc.ar(fr_000,0,SinOsc.ar(10,0,1,0),0);

	pitched = SinOsc.ar(pitch_env,0,1,0);
	//pitched = SinOsc.ar(220,0,0.2,SinOsc.ar(220*1.25,0,0.2,SinOsc.ar(220*1.5,0,0.2,SinOsc.ar(440,0,0.2,0))));
	//pitched = SinOsc.ar(Vibrato.ar(DC.ar(fr_000),5,0.1) );
	noise =PinkNoise.ar(0.75*(1-amp_env),0);
	//noise = ((amp_env+3)/8)*noise;

	noise = BLowPass4.ar(noise,freq_env,1,1,0);
	//noise = LPF.ar(noise,freq_env,1,0);
	//noise = lowpass*noise;
	//noise = (freq_env*noise);
	//pitched = Klank.ar(`[[fr_000,fr_000*1.25,fr_000*2],nil,[timestretch,timestretch,timestretch]],pitched,1,0,1);

	pitched = (amp_env*pitched);

	sig = pitched+noise;

	sig = Limiter.ar(sig,1,0.01);
	Out.ar(out, Pan2.ar(sig));

}).store;


(
SynthDef(\Pxx_blob, {
	arg
	pxx_000 = 0.000000001,
	pxx_001 = 0.000000001,
	pxx_002 = 0.000000001,
	pxx_003 = 0.000000001,
	pxx_004 = 0.000000001,
	pxx_005 = 0.000000001,
	pxx_006 = 0.000000001,
	pxx_007 = 0.000000001,
	pxx_008 = 0.000000001,
	pxx_009 = 0.000000001,
	pxx_010 = 0.000000001,
	pxx_011 = 0.000000001,
	pxx_012 = 0.000000001,
	pxx_013 = 0.000000001,
	pxx_014 = 0.000000001,
	pxx_015 = 0.000000001,
	pxx_016 = 0.000000001,
	pxx_017 = 0.000000001,
	pxx_018 = 0.000000001,
	pxx_019 = 0.000000001,
	pxx_020 = 0.000000001,
	pxx_021 = 0.000000001,
	pxx_022 = 0.000000001,
	pxx_023 = 0.000000001,
	pxx_024 = 0.000000001,
	pxx_025 = 0.000000001,
	pxx_026 = 0.000000001,
	pxx_027 = 0.000000001,
	pxx_028 = 0.000000001,
	pxx_029 = 0.000000001,
	pxx_030 = 0.000000001,
	pxx_031 = 0.000000001,
	pxx_032 = 0.000000001,
	pxx_033 = 0.000000001,
	pxx_034 = 0.000000001,
	pxx_035 = 0.000000001,

	cut_000 = 1,
	cut_001 = 1,
	cut_002 = 1,
	cut_003 = 1,
	cut_004 = 1,
	cut_005 = 1,
	cut_006 = 1,
	cut_007 = 1,
	cut_008 = 1,
	cut_009 = 1,
	cut_010 = 1,
	cut_011 = 1,
	cut_012 = 1,
	cut_013 = 1,
	cut_014 = 1,
	cut_015 = 1,
	cut_016 = 1,
	cut_017 = 1,
	cut_018 = 1,
	cut_019 = 1,
	cut_020 = 1,
	cut_021 = 1,
	cut_022 = 1,
	cut_023 = 1,
	cut_024 = 1,
	cut_025 = 1,
	cut_026 = 1,
	cut_027 = 1,
	cut_028 = 1,
	cut_029 = 1,
	cut_030 = 1,
	cut_031 = 1,
	cut_032 = 1,
	cut_033 = 1,
	cut_034 = 1,
	cut_035 = 1,

	act_000 = 0.0001,
	act_001 = 0.0001,
	act_002 = 0.0001,
	act_003 = 0.0001,
	act_004 = 0.0001,
	act_005 = 0.0001,
	act_006 = 0.0001,
	act_007 = 0.0001,
	act_008 = 0.0001,
	act_009 = 0.0001,
	act_010 = 0.0001,
	act_011 = 0.0001,
	act_012 = 0.0001,
	act_013 = 0.0001,
	act_014 = 0.0001,
	act_015 = 0.0001,
	act_016 = 0.0001,
	act_017 = 0.0001,
	act_018 = 0.0001,
	act_019 = 0.0001,
	act_020 = 0.0001,
	act_021 = 0.0001,
	act_022 = 0.0001,
	act_023 = 0.0001,
	act_024 = 0.0001,
	act_025 = 0.0001,
	act_026 = 0.0001,
	act_027 = 0.0001,
	act_028 = 0.0001,
	act_029 = 0.0001,
	act_030 = 0.0001,
	act_031 = 0.0001,
	act_032 = 0.0001,
	act_033 = 0.0001,
	act_034 = 0.0001,
	act_035 = 0.0001,

	ph_000 = 0.0001,
	ph_001 = 0.0001,
	ph_002 = 0.0001,
	ph_003 = 0.0001,
	ph_004 = 0.0001,
	ph_005 = 0.0001,
	ph_006 = 0.0001,
	ph_007 = 0.0001,
	ph_008 = 0.0001,
	ph_009 = 0.0001,
	ph_010 = 0.0001,
	ph_011 = 0.0001,
	ph_012 = 0.0001,
	ph_013 = 0.0001,
	ph_014 = 0.0001,
	ph_015 = 0.0001,
	ph_016 = 0.0001,
	ph_017 = 0.0001,
	ph_018 = 0.0001,
	ph_019 = 0.0001,
	ph_020 = 0.0001,
	ph_021 = 0.0001,
	ph_022 = 0.0001,
	ph_023 = 0.0001,
	ph_024 = 0.0001,
	ph_025 = 0.0001,
	ph_026 = 0.0001,
	ph_027 = 0.0001,
	ph_028 = 0.0001,
	ph_029 = 0.0001,
	ph_030 = 0.0001,
	ph_031 = 0.0001,
	ph_032 = 0.0001,
	ph_033 = 0.0001,
	ph_034 = 0.0001,
	ph_035 = 0.0001,

	fr_000 = 440.00,
	gate = 0.0,
	timestretch = 1.0;

	var time, pxx, amp_env,freq_env,active_env, sig,pitched,noise, pitch, pitch_env,cut,lowpass,active,click,sample;

	pxx = [pxx_000, pxx_001, pxx_002, pxx_003, pxx_004, pxx_005, pxx_006, pxx_007, pxx_008, pxx_009, pxx_010, pxx_011, pxx_012, pxx_013, pxx_014, pxx_015, pxx_016, pxx_017, pxx_018, pxx_019, pxx_020, pxx_021, pxx_022, pxx_023, pxx_024, pxx_025, pxx_026, pxx_027, pxx_028, pxx_029, pxx_030, pxx_031, pxx_032, pxx_033, pxx_034, pxx_035]; //heigt of peaks relative to falloff

	cut = [cut_000, cut_001, cut_002, cut_003, cut_004, cut_005, cut_006, cut_007, cut_008, cut_009, cut_010, cut_011, cut_012, cut_013, cut_014, cut_015, cut_016, cut_017, cut_018, cut_019, cut_020, cut_021, cut_022, cut_023, cut_024, cut_025, cut_026, cut_027, cut_028, cut_029, cut_030, cut_031, cut_032, cut_033, cut_034, cut_035]; //for cutoff frequencies of filter

	active = [act_000, act_001, act_002, act_003, act_004, act_005, act_006, act_007, act_008, act_009, act_010, act_011, act_012, act_013, act_014, act_015, act_016, act_017, act_018, act_019, act_020, act_021, act_022, act_023, act_024, act_025, act_026, act_027, act_028, act_029, act_030, act_031, act_032, act_033, act_034, act_035]; //for 'active' detected harmonic bands

	pitch = [ph_000, ph_001, ph_002, ph_003, ph_004, ph_005, ph_006, ph_007, ph_008, ph_009, ph_010, ph_011, ph_012, ph_013, ph_014, ph_015, ph_016, ph_017, ph_018, ph_019, ph_020, ph_021, ph_022, ph_023, ph_024, ph_025, ph_026, ph_027, ph_028, ph_029, ph_030, ph_031, ph_032, ph_033, ph_034, ph_035]; //the pitch of these bands

	time = timestretch*(1.0/(pxx.size));

	amp_env = EnvGen.kr(Env(pxx,[time]), gate, 1,0,1,0); // setting doneaction to 0 lets us use the gate to control on/off
	freq_env = EnvGen.kr(Env(cut,[time]),gate, 1,0,1,0); // cutoff freq
	active_env = EnvGen.kr(Env(active,[time]), gate, 1,0,1,0);
	pitch_env = EnvGen.kr(Env(pitch,[time]), gate, 1,0,1,0);

	//pitched = LFTri.ar(fr_000/2,0,SinOsc.ar(fr_000/2,0,1,0), 0);
	//pitched = SinOsc.ar(fr_000,0,1, SinOsc.ar(fr_000+10,0,1,0));
	//pitched = SinOsc.ar(fr_000,0,SinOsc.ar(10,0,1,0),0);

	//pitched = SinOsc.ar(pitch_env,0,1,0);.ar
	//pitch_env = Vibrato.kr(pitch_env,1,0.05);
	pitched = DynKlang.ar(`[ [pitch_env,pitch_env+7,pitch_env-5], [active_env/3,active_env/3,active_env/3] , nil ],1,0);
	//pitched = pitched + Saw.ar(pitch_env,active_env/50,0);
	//sample =  Buffer.read(s,"/Users/Lucas/Documents/spectrograms-master/sonification/samples/WaterBoil.wav",0,-1);
	//sig = PlayBuf.ar(2,0,1,0) * active_env*4;
	//pitched = DynKlang.ar(`[ [pitch_env,pitch_env*2,pitch_env*3,pitch_env*4,pitch_env*5],  [active_env*0.8,active_env*0.01,active_env*0.01,active_env*0.001,active_env*0.001] , nil ],1,0 ); //overtones
	//pitched = SinOsc.ar(220,0,0.2,SinOsc.ar(220*1.25,0,0.2,SinOsc.ar(220*1.5,0,0.2,SinOsc.ar(440,0,0.2,0))));
	//pitched = SinOsc.ar(Vibrato.ar(DC.ar(fr_000),5,0.1) );
	noise =BrownNoise.ar(5,0);// + BrownNoise.ar(0.2,0) + WhiteNoise.ar(0.1,0) + SinOsc.ar(LFNoise0.kr(200).range(100, freq_env/2), 0, 0.1);
	//noise = ((amp_env+3)/8)*noise;
	//noise = SinOsc.ar(fr_000);
	//noise = noise*amp_env;
	//noise = BLowPass4.ar(noise,freq_env,1,1,0);
	noise = LPF.ar(noise,freq_env,0.5,0);
	//noise = BPF.ar(noise,freq_env,1,0.5,0);
	//noise = RLPF.ar(noise,freq_env,10,1,0);
	//noise = lowpass*noise;
	//noise = (freq_env*noise);
	//pitched = Klank.ar(`[[fr_000,fr_000*1.25,fr_000*2],nil,[timestretch,timestretch,timestretch]],pitched,1,0,1);
	//click = Impulse.ar(freq_env/25,0,1,0);
	//pitched = (active_env*itched);

	//sig = (pitched*amp_env)+noise;//+click;
	//sig = pitched+noise;
	//pitched = SinOsc.ar(fr_000,0,1,0);
	//sig = pitched*amp_env;
	//blend = amp_env - amp_env*((active-1)**2);

	pitched = Limiter.ar(pitched,1,0.1);
	noise = Limiter.ar(noise,1,0.1);
	//Out.ar(0, Pan2.ar(pitched*5*amp_env));
	//Out.ar(0, Pan2.ar(pitched+noise));
	//Out.ar(0, Pan2.ar(sig));
	Out.ar(0, Pan2.ar(pitched,0.0-(3*amp_env),10*amp_env)); //panning and loudness
	Out.ar(0, Pan2.ar(noise,0.0+(3*amp_env),0.5)); //panning
}).store; //Pxx_bob
)
)


(
(
SynthDef(\pitched_only, {
	arg
	pxx_000 = 0.000000001,
	pxx_001 = 0.000000001,
	pxx_002 = 0.000000001,
	pxx_003 = 0.000000001,
	pxx_004 = 0.000000001,
	pxx_005 = 0.000000001,
	pxx_006 = 0.000000001,
	pxx_007 = 0.000000001,
	pxx_008 = 0.000000001,
	pxx_009 = 0.000000001,
	pxx_010 = 0.000000001,
	pxx_011 = 0.000000001,
	pxx_012 = 0.000000001,
	pxx_013 = 0.000000001,
	pxx_014 = 0.000000001,
	pxx_015 = 0000001,
	pxx_016 = 0.000000001,
	pxx_017 = 0.000000001,
	pxx_018 = 0.000000001,
	pxx_019 = 0.000000001,
	pxx_020 = 0.000000001,
	pxx_021 = 0.000000001,
	pxx_022 = 0.000000001,
	pxx_023 = 0.000000001,
	pxx_024 = 0.000000001,
	pxx_025 = 0.000000001,
	pxx_026 = 0.000000001,
	pxx_027 = 0.000000001,
	pxx_028 = 0.000000001,
	pxx_029 = 0.000000001,
	pxx_030 = 0.000000001,
	pxx_031 = 0.000000001,
	pxx_032 = 0.000000001,
	pxx_033 = 0.000000001,
	pxx_034 = 0.000000001,
	pxx_035 = 0.000000001,

	cut_000 = 1,
	cut_001 = 1,
	cut_002 = 1,
	cut_003 = 1,
	cut_004 = 1,
	cut_005 = 1,
	cut_006 = 1,
	cut_007 = 1,
	cut_008 = 1,
	cut_009 = 1,
	cut_010 = 1,
	cut_011 = 1,
	cut_012 = 1,
	cut_013 = 1,
	cut_014 = 1,
	cut_015 = 1,
	cut_016 = 1,
	cut_017 = 1,
	cut_018 = 1,
	cut_019 = 1,
	cut_020 = 1,
	cut_021 = 1,
	cut_022 = 1,
	cut_023 = 1,
	cut_024 = 1,
	cut_025 = 1,
	cut_026 = 1,
	cut_027 = 1,
	cut_028 = 1,
	cut_029 = 1,
	cut_030 = 1,
	cut_031 = 1,
	cut_032 = 1,
	cut_033 = 1,
	cut_034 = 1,
	cut_035 = 1,

	act_000 = 0.0001,
	act_001 = 0.0001,
	act_002 = 0.0001,
	act_003 = 0.0001,
	act_004 = 0.0001,
	act_005 = 0.0001,
	act_006 = 0.0001,
	act_007 = 0.0001,
	act_008 = 0.0001,
	act_009 = 0.0001,
	act_010 = 0.0001,
	act_011 = 0.0001,
	act_012 = 0.0001,
	act_013 = 0.0001,
	act_014 = 0.0001,
	act_015 = 0.0001,
	act_016 = 0.0001,
	act_017 = 0.0001,
	act_018 = 0.0001,
	act_019 = 0.0001,
	act_020 = 0.0001,
	act_021 = 0.0001,
	act_022 = 0.0001,
	act_023 = 0.0001,
	act_024 = 0.0001,
	act_025 = 0.0001,
	act_026 = 0.0001,
	act_027 = 0.0001,
	act_028 = 0.0001,
	act_029 = 0.0001,
	act_030 = 0.0001,
	act_031 = 0.0001,
	act_032 = 0.0001,
	act_033 = 0.0001,
	act_034 = 0.0001,
	act_035 = 0.0001,

	ph_000 = 0.0001,
	ph_001 = 0.0001,
	ph_002 = 0.0001,
	ph_003 = 0.0001,
	ph_004 = 0.0001,
	ph_005 = 0.0001,
	ph_006 = 0.0001,
	ph_007 = 0.0001,
	ph_008 = 0.0001,
	ph_009 = 0.0001,
	ph_010 = 0.0001,
	ph_011 = 0.0001,
	ph_012 = 0.0001,
	ph_013 = 0.0001,
	ph_014 = 0.0001,
	ph_015 = 0.0001,
	ph_016 = 0.0001,
	ph_017 = 0.0001,
	ph_018 = 0.0001,
	ph_019 = 0.0001,
	ph_020 = 0.0001,
	ph_021 = 0.0001,
	ph_022 = 0.0001,
	ph_023 = 0.0001,
	ph_024 = 0.0001,
	ph_025 = 0.0001,
	ph_026 = 0.0001,
	ph_027 = 0.0001,
	ph_028 = 0.0001,
	ph_029 = 0.0001,
	ph_030 = 0.0001,
	ph_031 = 0.0001,
	ph_032 = 0.0001,
	ph_033 = 0.0001,
	ph_034 = 0.0001,
	ph_035 = 0.0001,

	fr_000 = 440.00,
	gate = 0.0,
	timestretch = 1.0;

	var time, pxx, amp_env,freq_env,active_env, sig,pitched,noise, pitch, pitch_env,cut,lowpass,active,click,sample;

	pxx = [pxx_000, pxx_001, pxx_002, pxx_003, pxx_004, pxx_005, pxx_006, pxx_007, pxx_008, pxx_009, pxx_010, pxx_011, pxx_012, pxx_013, pxx_014, pxx_015, pxx_016, pxx_017, pxx_018, pxx_019, pxx_020, pxx_021, pxx_022, pxx_023, pxx_024, pxx_025, pxx_026, pxx_027, pxx_028, pxx_029, pxx_030, pxx_031, pxx_032, pxx_033, pxx_034, pxx_035]; //heigt of peaks relative to falloff

	cut = [cut_000, cut_001, cut_002, cut_003, cut_004, cut_005, cut_006, cut_007, cut_008, cut_009, cut_010, cut_011, cut_012, cut_013, cut_014, cut_015, cut_016, cut_017, cut_018, cut_019, cut_020, cut_021, cut_022, cut_023, cut_024, cut_025, cut_026, cut_027, cut_028, cut_029, cut_030, cut_031, cut_032, cut_033, cut_034, cut_035]; //for cutoff frequencies of filter

	active = [act_000, act_001, act_002, act_003, act_004, act_005, act_006, act_007, act_008, act_009, act_010, act_011, act_012, act_013, act_014, act_015, act_016, act_017, act_018, act_019, act_020, act_021, act_022, act_023, act_024, act_025, act_026, act_027, act_028, act_029, act_030, act_031, act_032, act_033, act_034, act_035]; //for 'active' detected harmonic bands

	pitch = [ph_000, ph_001, ph_002, ph_003, ph_004, ph_005, ph_006, ph_007, ph_008, ph_009, ph_010, ph_011, ph_012, ph_013, ph_014, ph_015, ph_016, ph_017, ph_018, ph_019, ph_020, ph_021, ph_022, ph_023, ph_024, ph_025, ph_026, ph_027, ph_028, ph_029, ph_030, ph_031, ph_032, ph_033, ph_034, ph_035]; //the pitch of these bands

	time = timestretch*(1.0/(pxx.size));

	amp_env = EnvGen.kr(Env(pxx,[time]), gate, 1,0,1,0); // setting doneaction to 0 lets us use the gate to control on/off
	freq_env = EnvGen.kr(Env(cut,[time]),gate, 1,0,1,0); // cutoff freq
	active_env = EnvGen.kr(Env(active,[time]), gate, 1,0,1,0);
	pitch_env = EnvGen.kr(Env(pitch,[time]), gate, 1,0,1,0);

	//pitched = LFTri.ar(fr_000/2,0,SinOsc.ar(fr_000/2,0,1,0), 0);
	//pitched = SinOsc.ar(fr_000,0,1, SinOsc.ar(fr_000+10,0,1,0));
	//pitched = SinOsc.ar(fr_000,0,SinOsc.ar(10,0,1,0),0);

	//pitched = SinOsc.ar(pitch_env,0,1,0);.ar
	//pitch_env = Vibrato.kr(pitch_env,1,0.05);

	//pitched = DynKlang.ar(`[ [pitch_env,pitch_env+7,pitch_env-5], [active_env/3,active_env/3,active_env/3] , nil ],1,0); //sinosc w/overtones


	pitched = VarSaw.ar(pitch_env,
		width:LFNoise2.kr(1).range(0.2, 0.8)*SinOsc.kr(5, Rand(0.0, 1.0)).range(0.7,0.8))*0.6 + PinkNoise.ar(0.05,0)*active_env;

	pitched = LPF.ar(pitched,1000,1,0);

	//pitched = pitched + Saw.ar(pitch_env,active_env/50,0);

	//pitched = Limiter.ar(pitched,1,0.1);
	//Out.ar(0, Pan2.ar(pitched*5*amp_env));
	//Out.ar(0, Pan2.ar(pitched+noise));
	//Out.ar(0, Pan2.ar(pitched));
	Out.ar(0, Pan2.ar(pitched,0,0.05*amp_env*freq_env)); //panning and loudness
}).store; //pitched_only
)
)








// define the violin-like sound synth
(
SynthDef(\violin, {
	| midinote=60, gate=1, amp=0.25 |
	//var env = EnvGen.kr(Env.asr(0.1, 1, 0.1), gate, doneAction:2);
	var sig = VarSaw.ar(
		midinote.midicps,
		width:LFNoise2.kr(1).range(0.2, 0.8)*SinOsc.kr(5, Rand(0.0, 1.0)).range(0.7,0.8))*0.25;
	sig = sig * 1 * amp;
	Out.ar(0, sig!2);
}).add;
)


// play a chord (farfisa-like sound)
(
[60, 64, 67].do ({
	| note |
	Synth(\violin, [\midinote, note]);
})
)

// play a single note (it seems also a flute!)
x = Synth(\violin, [\midinote, 84]);
x.set(\gate, 0); // stop the note




(
SynthDef(\noise_only, {
	arg
	cut_000 = 1,
	cut_001 = 1,
	cut_002 = 1,
	cut_003 = 1,
	cut_004 = 1,
	cut_005 = 1,
	cut_006 = 1,
	cut_007 = 1,
	cut_008 = 1,
	cut_009 = 1,
	cut_010 = 1,
	cut_011 = 1,
	cut_012 = 1,
	cut_013 = 1,
	cut_014 = 1,
	cut_015 = 1,
	cut_016 = 1,
	cut_017 = 1,
	cut_018 = 1,
	cut_019 = 1,
	cut_020 = 1,
	cut_021 = 1,
	cut_022 = 1,
	cut_023 = 1,
	cut_024 = 1,
	cut_025 = 1,
	cut_026 = 1,
	cut_027 = 1,
	cut_028 = 1,
	cut_029 = 1,
	cut_030 = 1,
	cut_031 = 1,
	cut_032 = 1,
	cut_033 = 1,
	cut_034 = 1,
	cut_035 = 1,

	fr_000 = 440.00,
	gate = 0.0,
	timestretch = 1.0;

	var time,freq_env, sig, noise,cut,sample;

	cut = [cut_000, cut_001, cut_002, cut_003, cut_004, cut_005, cut_006, cut_007, cut_008, cut_009, cut_010, cut_011, cut_012, cut_013, cut_014, cut_015, cut_016, cut_017, cut_018, cut_019, cut_020, cut_021, cut_022, cut_023, cut_024, cut_025, cut_026, cut_027, cut_028, cut_029, cut_030, cut_031, cut_032, cut_033, cut_034, cut_035]; //for cutoff frequencies of filter

	time = timestretch*(1.0/(cut.size));

	freq_env = EnvGen.kr(Env(cut,[time]),gate, 1,0,1,0); // cutoff freq

	sample =  Buffer.read(s,"/Users/Lucas/Documents/spectrograms-master/sonification/samples/WaterBoil.wav",0,-1);
	sig = PlayBuf.ar(2,0,1,0,doneAction:2)*4+PinkNoise.ar(0.2)+WhiteNoise.ar(0.1);
	noise = RLPF.ar(sig,freq_env,0.5,1,0);
	//noise = LPF.ar(sig,freq_env,1,0);
	noise = FreeVerb.ar(noise,0.5,1,0,1,0);
	noise = Limiter.ar(noise,1,0.1);
	Out.ar(0, Pan2.ar(noise));
}).store; //noise_only
)








123456789098765423456789876323456789654

(
SynthDef(\player, {
	arg
	pxx_000 = 0.000000001,
	pxx_001 = 0.000000001,
	pxx_002 = 0.000000001,
	pxx_003 = 0.000000001,
	pxx_004 = 0.000000001,
	pxx_005 = 0.000000001,
	pxx_006 = 0.000000001,
	pxx_007 = 0.000000001,
	pxx_008 = 0.000000001,
	pxx_009 = 0.000000001,
	pxx_010 = 0.000000001,
	pxx_011 = 0.000000001,
	pxx_012 = 0.000000001,
	pxx_013 = 0.000000001,
	pxx_014 = 0.000000001,
	pxx_015 = 0.000000001,
	pxx_016 = 0.000000001,
	pxx_017 = 0.000000001,
	pxx_018 = 0.000000001,
	pxx_019 = 0.000000001,
	pxx_020 = 0.000000001,
	pxx_021 = 0.000000001,
	pxx_022 = 0.000000001,
	pxx_023 = 0.000000001,
	pxx_024 = 0.000000001,
	pxx_025 = 0.000000001,
	pxx_026 = 0.000000001,
	pxx_027 = 0.000000001,
	pxx_028 = 0.000000001,
	pxx_029 = 0.000000001,
	pxx_030 = 0.000000001,
	pxx_031 = 0.000000001,
	pxx_032 = 0.000000001,
	pxx_033 = 0.000000001,
	pxx_034 = 0.000000001,
	pxx_035 = 0.000000001,

	cut_000 = 1,
	cut_001 = 1,
	cut_002 = 1,
	cut_003 = 1,
	cut_004 = 1,
	cut_005 = 1,
	cut_006 = 1,
	cut_007 = 1,
	cut_008 = 1,
	cut_009 = 1,
	cut_010 = 1,
	cut_011 = 1,
	cut_012 = 1,
	cut_013 = 1,
	cut_014 = 1,
	cut_015 = 1,
	cut_016 = 1,
	cut_017 = 1,
	cut_018 = 1,
	cut_019 = 1,
	cut_020 = 1,
	cut_021 = 1,
	cut_022 = 1,
	cut_023 = 1,
	cut_024 = 1,
	cut_025 = 1,
	cut_026 = 1,
	cut_027 = 1,
	cut_028 = 1,
	cut_029 = 1,
	cut_030 = 1,
	cut_031 = 1,
	cut_032 = 1,
	cut_033 = 1,
	cut_034 = 1,
	cut_035 = 1,

	act_000 = 0.0001,
	act_001 = 0.0001,
	act_002 = 0.0001,
	act_003 = 0.0001,
	act_004 = 0.0001,
	act_005 = 0.0001,
	act_006 = 0.0001,
	act_007 = 0.0001,
	act_008 = 0.0001,
	act_009 = 0.0001,
	act_010 = 0.0001,
	act_011 = 0.0001,
	act_012 = 0.0001,
	act_013 = 0.0001,
	act_014 = 0.0001,
	act_015 = 0.0001,
	act_016 = 0.0001,
	act_017 = 0.0001,
	act_018 = 0.0001,
	act_019 = 0.0001,
	act_020 = 0.0001,
	act_021 = 0.0001,
	act_022 = 0.0001,
	act_023 = 0.0001,
	act_024 = 0.0001,
	act_025 = 0.0001,
	act_026 = 0.0001,
	act_027 = 0.0001,
	act_028 = 0.0001,
	act_029 = 0.0001,
	act_030 = 0.0001,
	act_031 = 0.0001,
	act_032 = 0.0001,
	act_033 = 0.0001,
	act_034 = 0.0001,
	act_035 = 0.0001,

	ph_000 = 0.0001,
	ph_001 = 0.0001,
	ph_002 = 0.0001,
	ph_003 = 0.0001,
	ph_004 = 0.0001,
	ph_005 = 0.0001,
	ph_006 = 0.0001,
	ph_007 = 0.0001,
	ph_008 = 0.0001,
	ph_009 = 0.0001,
	ph_010 = 0.0001,
	ph_011 = 0.0001,
	ph_012 = 0.0001,
	ph_013 = 0.0001,
	ph_014 = 0.0001,
	ph_015 = 0.0001,
	ph_016 = 0.0001,
	ph_017 = 0.0001,
	ph_018 = 0.0001,
	ph_019 = 0.0001,
	ph_020 = 0.0001,
	ph_021 = 0.0001,
	ph_022 = 0.0001,
	ph_023 = 0.0001,
	ph_024 = 0.0001,
	ph_025 = 0.0001,
	ph_026 = 0.0001,
	ph_027 = 0.0001,
	ph_028 = 0.0001,
	ph_029 = 0.0001,
	ph_030 = 0.0001,
	ph_031 = 0.0001,
	ph_032 = 0.0001,
	ph_033 = 0.0001,
	ph_034 = 0.0001,
	ph_035 = 0.0001,

	fr_000 = 440.00,
	gate = 0.0,
	timestretch = 1.0;

	var time, pxx, amp_env,freq_env,active_env, sig,pitched,noise, pitch, pitch_env,cut,lowpass,active,click,sample;

	pxx = [pxx_000, pxx_001, pxx_002, pxx_003, pxx_004, pxx_005, pxx_006, pxx_007, pxx_008, pxx_009, pxx_010, pxx_011, pxx_012, pxx_013, pxx_014, pxx_015, pxx_016, pxx_017, pxx_018, pxx_019, pxx_020, pxx_021, pxx_022, pxx_023, pxx_024, pxx_025, pxx_026, pxx_027, pxx_028, pxx_029, pxx_030, pxx_031, pxx_032, pxx_033, pxx_034, pxx_035]; //heigt of peaks relative to falloff

	cut = [cut_000, cut_001, cut_002, cut_003, cut_004, cut_005, cut_006, cut_007, cut_008, cut_009, cut_010, cut_011, cut_012, cut_013, cut_014, cut_015, cut_016, cut_017, cut_018, cut_019, cut_020, cut_021, cut_022, cut_023, cut_024, cut_025, cut_026, cut_027, cut_028, cut_029, cut_030, cut_031, cut_032, cut_033, cut_034, cut_035]; //for cutoff frequencies of filter

	active = [act_000, act_001, act_002, act_003, act_004, act_005, act_006, act_007, act_008, act_009, act_010, act_011, act_012, act_013, act_014, act_015, act_016, act_017, act_018, act_019, act_020, act_021, act_022, act_023, act_024, act_025, act_026, act_027, act_028, act_029, act_030, act_031, act_032, act_033, act_034, act_035]; //for 'active' detected harmonic bands

	pitch = [ph_000, ph_001, ph_002, ph_003, ph_004, ph_005, ph_006, ph_007, ph_008, ph_009, ph_010, ph_011, ph_012, ph_013, ph_014, ph_015, ph_016, ph_017, ph_018, ph_019, ph_020, ph_021, ph_022, ph_023, ph_024, ph_025, ph_026, ph_027, ph_028, ph_029, ph_030, ph_031, ph_032, ph_033, ph_034, ph_035]; //the pitch of these bands

	time = timestretch*(1.0/(pxx.size));

	amp_env = EnvGen.kr(Env(pxx,[time]), gate, 1,0,1,0); // setting doneaction to 0 lets us use the gate to control on/off
	freq_env = EnvGen.kr(Env(cut,[time]),gate, 1,0,1,0); // cutoff freq
	active_env = EnvGen.kr(Env(active,[time]), gate, 1,0,1,0);
	pitch_env = EnvGen.kr(Env(pitch,[time]), gate, 1,0,1,0);

	sample =  Buffer.read(s,"/Users/Lucas/Documents/spectrograms-master/sonification/samples/WaterBoil.wav",0,-1);
	sig = PlayBuf.ar(2,0,1,0) * active_env * 2;
	Out.ar(0, Pan2.ar(sig));
}).store; //player
)




(
SynthDef(\turbine, {
	arg
	cut_000 = 1,
	cut_001 = 1,
	cut_002 = 1,
	cut_003 = 1,
	cut_004 = 1,
	cut_005 = 1,
	cut_006 = 1,
	cut_007 = 1,
	cut_008 = 1,
	cut_009 = 1,
	cut_010 = 1,
	cut_011 = 1,
	cut_012 = 1,
	cut_013 = 1,
	cut_014 = 1,
	cut_015 = 1,
	cut_016 = 1,
	cut_017 = 1,
	cut_018 = 1,
	cut_019 = 1,
	cut_020 = 1,
	cut_021 = 1,
	cut_022 = 1,
	cut_023 = 1,
	cut_024 = 1,
	cut_025 = 1,
	cut_026 = 1,
	cut_027 = 1,
	cut_028 = 1,
	cut_029 = 1,
	cut_030 = 1,
	cut_031 = 1,
	cut_032 = 1,
	cut_033 = 1,
	cut_034 = 1,
	cut_035 = 1,

	gate = 0.0,
	timestretch = 1.0;

	var time,freq_env, rq_env, mod_amp_env, sig, car, mod,cut;

	cut = [cut_000, cut_001, cut_002, cut_003, cut_004, cut_005, cut_006, cut_007, cut_008, cut_009, cut_010, cut_011, cut_012, cut_013, cut_014, cut_015, cut_016, cut_017, cut_018, cut_019, cut_020, cut_021, cut_022, cut_023, cut_024, cut_025, cut_026, cut_027, cut_028, cut_029, cut_030, cut_031, cut_032, cut_033, cut_034, cut_035]; //scaled between 0 and 1

	time = timestretch*(1.0/(cut.size));

	freq_env = EnvGen.kr(Env(cut*1950+50,[time]),gate, 1,0,1,0); // cutoff freq
	rq_env = EnvGen.kr(Env(cut*0.5+0.5,[time]),gate, 1,0,1,0);
	mod_amp_env = EnvGen.kr(Env(cut*1.5,[time]),gate, 1,0,1,0);

	car = BrownNoise.ar(1,0);
	mod = BrownNoise.ar(mod_amp_env,0);

	sig = RLPF.ar(car,freq_env+mod,rq_env+mod,50,1 );

	Out.ar(0, Pan2.ar(sig));


}).store; //turbine
)





(
{
    var w, x, y, p, a, b, c, d;

    p = PinkNoise.ar; // source

    // B-format encode
	#w, x, y = PanB2.ar(p, 0.2, 2);

    // B-format decode to quad
    #a, b= DecodeB2.ar(2, w, x, y);

    [a, b] // reorder to my speaker arrangement: Lf Rf Lr Rr
}.play;
)















{Blip.ar(440,910,1,0)}.play;
{ Impulse.ar(120, 0, 1, 0) }.play

(
(SynthDef(\mat,{

	arg out =0,
	p1=220,
	p2=440,
	p3=880,
	p4=880*2,
	p5=880*4,

	a1=0.8,
	a2=0.05,
	a3=0.05,
	a4=0.05,
	a5=0.05;

	var pitch,active,pitched,sig;

	pitch = [p1,p2,p3,p4,p5];
	active = [a1,a2,a3,a4,a5];

	pitched = DynKlang.ar(`[ pitch, active, nil ],1,0 );
	//pitched = SinOsc.ar(p1,0,1,0);

	sig = Limiter.ar(pitched,1,0.01);
	Out.ar(out, Pan2.ar(sig));

})
).add;
)
{SinOsc.ar(800)}.play;
a=Synth(\mat);
a.set(\a1,0.8,\a2,0.01,\a3,0.01,\a4,0.05,\a5,0.05);
a.set(\p1,200,\p2,880,\p3,660);


play({ Klang.ar(`[ [440], [1], [0]], 1, 0)});

{SinOsc.ar(Vibrato.ar(DC.ar(440.0),10,0.1) )}.play

{LFPulse.ar(440,0,0.5,1,0)}.play;

{ LFTri.ar(500, 0, 1, SinOsc.ar(510,0.1,1)    ) }.play

{ SinOsc.ar(500, 0, 1, SinOsc.ar(510,0.1,1)    ) }.play

 {SinOsc.ar(440,0,1,SinOsc.ar(440,1,1,0))}.play
.
{SinOsc.ar(440,SinOsc.ar(440,1,1,0))}.play


{SinOsc.ar(440,0,0.5**2 ,0)}.play

{ LPF.ar(Saw.ar(200,0.1),
	SinOsc.kr(XLine.kr(0.7,300,20),0,3600,4000)
) }.play;


{Klank.ar(`[[440,440*1.25,440*5],nil,[1,1,1]],SinOsc.ar(100,0,1,0),1,0,1)}.play;

(
y = Synth(\spectro_image, [\fr_000,440,\gate,1,\pxx_001,0.5,\pxx_002,0.5,\pxx_003,1,\timestretch,1,

	\cut_000 , 100.000000001,
	\cut_001 , 200.000000001,
	\cut_002 , 300.000000001,
	\cut_003 , 400.000000001,
	\cut_004 , 500.000000001,
	\cut_005 , 600.000000001,
	\cut_006 , 700.000000001,
	\cut_007 , 800.000000001,
	\cut_008 , 900.000000001,
	\cut_009 , 1000.000000001,
	\cut_010 , 1100.000000001,
	\cut_011 , 1200.000000001,
	\cut_012 , 1300.000000001,
	\cut_013 , 1400.000000001,
	\cut_014 , 1500.000000001,
	\cut_015 , 1600.000000001,
	\cut_016 , 1700.000000001,
	\cut_017 , 1800.000000001,
	\cut_018 , 1900.000000001,
	\cut_019 , 2000.000000001,
	\cut_020 , 3000.000000001,
	\cut_021 , 4000.000000001,
	\cut_022 , 5000.000000001,
	\cut_023 , 6000.000000001,
	\cut_024 , 7000.000000001,
	\cut_025 , 8000.000000001,
	\cut_026 , 9000.000000001,
	\cut_027 , 10000.000000001,
	\cut_028 , 8000.000000001,
	\cut_029 , 7000.000000001,
	\cut_030 , 1000.000000001,
	\cut_031 , 0.000000001,
	\cut_032 , 5000.000000001,
	\cut_033 , 6000.000000001,
	\cut_034 , 4100.000000001,
	\cut_035 , 000.000000001
]);


x = Synth(\spectro_image, [\fr_000,80,\gate,1,\pxx_001,0.5,\pxx_002,0.5,\pxx_003,1,\timestretch,1,

	\cut_000 , 100.000000001,
	\cut_001 , 200.000000001,
	\cut_002 , 300.000000001,
	\cut_003 , 400.000000001,
	\cut_004 , 500.000000001,
	\cut_005 , 600.000000001,
	\cut_006 , 700.000000001,
	\cut_007 , 800.000000001,
	\cut_008 , 900.000000001,
	\cut_009 , 1000.000000001,
	\cut_010 , 1100.000000001,
	\cut_011 , 1200.000000001,
	\cut_012 , 1300.000000001,
	\cut_013 , 1400.000000001,
	\cut_014 , 1500.000000001,
	\cut_015 , 1600.000000001,
	\cut_016 , 1700.000000001,
	\cut_017 , 1800.000000001,
	\cut_018 , 1900.000000001,
	\cut_019 , 2000.000000001,
	\cut_020 , 3000.000000001,
	\cut_021 , 4000.000000001,
	\cut_022 , 5000.000000001,
	\cut_023 , 6000.000000001,
	\cut_024 , 7000.000000001,
	\cut_025 , 8000.000000001,
	\cut_026 , 9000.000000001,
	\cut_027 , 10000.000000001,
	\cut_028 , 8000.000000001,
	\cut_029 , 7000.000000001,
	\cut_030 , 1000.000000001,
	\cut_031 , 0.000000001,
	\cut_032 , 5000.000000001,
	\cut_033 , 6000.000000001,
	\cut_034 , 4100.000000001,
	\cut_035 , 000.000000001
]);


)





(
SynthDef(\PinkNoise, {
	arg out=0,
	cut_000 = 0.000000001,
	cut_001 = 0.000000001,
	cut_002 = 0.000000001,
	cut_003 = 0.000000001,
	cut_004 = 0.000000001,
	cut_005 = 0.000000001,
	cut_006 = 0.000000001,
	cut_007 = 0.000000001,
	cut_008 = 0.000000001,
	cut_009 = 0.000000001,
	cut_010 = 0.000000001,
	cut_011 = 0.000000001,
	cut_012 = 0.000000001,
	cut_013 = 0.000000001,
	cut_014 = 0.000000001,
	cut_015 = 0.000000001,
	cut_016 = 0.000000001,
	cut_017 = 0.000000001,
	cut_018 = 0.000000001,
	cut_019 = 0.000000001,
	cut_020 = 0.000000001,
	cut_021 = 0.000000001,
	cut_022 = 0.000000001,
	cut_023 = 0.000000001,
	cut_024 = 0.000000001,
	cut_025 = 0.000000001,
	cut_026 = 0.000000001,
	cut_027 = 0.000000001,
	cut_028 = 0.000000001,
	cut_029 = 0.000000001,
	cut_030 = 0.000000001,
	cut_031 = 0.000000001,
	cut_032 = 0.000000001,
	cut_033 = 0.000000001,
	cut_034 = 0.000000001,
	cut_035 = 0.000000001,


	gate = 0.0,
	timestretch = 1.0;

    var time, freq_env, sig,cut;

	cut = [cut_000, cut_001, cut_002, cut_003, cut_004, cut_005, cut_006, cut_007, cut_008, cut_009, cut_010, cut_011, cut_012, cut_013, cut_014, cut_015, cut_016, cut_017, cut_018, cut_019, cut_020, cut_021, cut_022, cut_023, cut_024, cut_025, cut_026, cut_027, cut_028, cut_029, cut_030, cut_031, cut_032, cut_033, cut_034, cut_035];

	time = timestretch*(1.0/(cut.size));
	freq_env = EnvGen.kr(Env(cut,[time]),gate, 1,0,1,0);

	sig = PinkNoise.ar(1);

	sig = LPF.ar(sig,freq_env,1,0);

	sig = Limiter.ar(sig,1,0.01);
	Out.ar(out, Pan2.ar(sig));
}).store;
)

(
x = Synth(\PinkNoise, [\gate,1,\timestretch,1,

	\cut_000 , 100.000000001,
	\cut_001 , 200.000000001,
	\cut_002 , 300.000000001,
	\cut_003 , 400.000000001,
	\cut_004 , 500.000000001,
	\cut_005 , 600.000000001,
	\cut_006 , 700.000000001,
	\cut_007 , 800.000000001,
	\cut_008 , 900.000000001,
	\cut_009 , 1000.000000001,
	\cut_010 , 1100.000000001,
	\cut_011 , 1200.000000001,
	\cut_012 , 1300.000000001,
	\cut_013 , 1400.000000001,
	\cut_014 , 1500.000000001,
	\cut_015 , 0,
	\cut_016 , 1700.000000001,
	\cut_017 , 1800.000000001,
	\cut_018 , 1900.000000001,
	\cut_019 , -0,
	\cut_020 , 3000.000000001,
	\cut_021 , 4000.000000001,
	\cut_022 , 5000.000000001,
	\cut_023 , 6000.000000001,
	\cut_024 , 7000.000000001,
	\cut_025 , 8000.000000001,
	\cut_026 , 9000.000000001,
	\cut_027 , 10000.000000001,
	\cut_028 , 8000.000000001,
	\cut_029 , 7000.000000001,
	\cut_030 , 1000.000000001,
	\cut_031 , 0.000000001,
	\cut_032 , 5000.000000001,
	\cut_033 , 6000.000000001,
	\cut_034 , 4100.000000001,
	\cut_035 , 000.000000001
]);


)

























	cut_000 = 100.000000001,
	cut_001 = 200.000000001,
	cut_002 = 300.000000001,
	cut_003 = 400.000000001,
	cut_004 = 500.000000001,
	cut_005 = 600.000000001,
	cut_006 = 700.000000001,
	cut_007 = 800.000000001,
	cut_008 = 900.000000001,
	cut_009 = 1000.000000001,
	cut_010 = 1100.000000001,
	cut_011 = 1200.000000001,
	cut_012 = 1300.000000001,
	cut_013 = 1400.000000001,
	cut_014 = 1500.000000001,
	cut_015 = 1600.000000001,
	cut_016 = 1700.000000001,
	cut_017 = 1800.000000001,
	cut_018 = 1900.000000001,
	cut_019 = 2000.000000001,
	cut_020 = 3000.000000001,
	cut_021 = 4000.000000001,
	cut_022 = 5000.000000001,
	cut_023 = 6000.000000001,
	cut_024 = 7000.000000001,
	cut_025 = 8000.000000001,
	cut_026 = 9000.000000001,
	cut_027 = 10000.000000001,
	cut_028 = 8000.000000001,
	cut_029 = 7000.000000001,
	cut_030 = 1000.000000001,
	cut_031 = 0.000000001,
	cut_032 = 5000.000000001,
	cut_033 = 6000.000000001,
	cut_034 = 4100.000000001,
	cut_035 = 2000.000000001,

