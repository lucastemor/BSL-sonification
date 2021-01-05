(
(
SynthDef(\chromagram_pitched_only, {
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
	freq_env = EnvGen.kr(Env(cut,[time]),gate, 1,0,1,0); //
	active_env = EnvGen.kr(Env(active,[time]), gate, 1,0,1,0);
	pitch_env = EnvGen.kr(Env(pitch,[time]), gate, 1,0,1,0);

	//pitched = LFTri.ar(fr_000/2,0,SinOsc.ar(fr_000/2,0,1,0), 0);
	//pitched = SinOsc.ar(fr_000,0,1, SinOsc.ar(fr_000+10,0,1,0));
	//pitched = SinOsc.ar(fr_000,0,SinOsc.ar(10,0,1,0),0);

	pitched = SinOsc.ar(fr_000,0,pitch_env,0);
	//pitch_env = Vibrato.kr(pitch_env,1,0.05);
	//pitched = DynKlang.ar(`[ [pitch_env,pitch_env+7,pitch_env-5], nil , nil ],1,0);
	//pitched = pitched + Saw.ar(pitch_env,active_env/50,0);

	//pitched = Limiter.ar(pitched,1,0.1);
	//Out.ar(0, Pan2.ar(pitched*5*amp_env));
	//Out.ar(0, Pan2.ar(pitched+noise));
	Out.ar(0, Pan2.ar(pitched));
	//Out.ar(0, Pan2.ar(pitched,0.0-(3*amp_env),10*amp_env)); //panning and loudness
}).store; //pitched_only
)
)



///////////////////////////////////////////////////////////////////////////////////////////////////


(
(
SynthDef(\simple_chromagram, {
	arg

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

	var time,sig,pitched, pitch, pitch_env;

	pitch = [ph_000, ph_001, ph_002, ph_003, ph_004, ph_005, ph_006, ph_007, ph_008, ph_009, ph_010, ph_011, ph_012, ph_013, ph_014, ph_015, ph_016, ph_017, ph_018, ph_019, ph_020, ph_021, ph_022, ph_023, ph_024, ph_025, ph_026, ph_027, ph_028, ph_029, ph_030, ph_031, ph_032, ph_033, ph_034, ph_035]; //the pitch of these bands

	time = timestretch*(1.0/(pitch.size));

	pitch_env = EnvGen.kr(Env(pitch,[time]), gate, 1,0,1,0);

	pitched = SinOsc.ar(fr_000,0,pitch_env,0);

	Out.ar(0, Pan2.ar(pitched*20));

}).store; //simple_chromagram
)
)


(
(
SynthDef(\four_osc_chromagram, {
	arg

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

	var time,sig,pitched, pitch, pitch_env, subOsc,square,saw,sine;

	pitch = [ph_000, ph_001, ph_002, ph_003, ph_004, ph_005, ph_006, ph_007, ph_008, ph_009, ph_010, ph_011, ph_012, ph_013, ph_014, ph_015, ph_016, ph_017, ph_018, ph_019, ph_020, ph_021, ph_022, ph_023, ph_024, ph_025, ph_026, ph_027, ph_028, ph_029, ph_030, ph_031, ph_032, ph_033, ph_034, ph_035]; //the pitch of these bands

	time = timestretch*(1.0/(pitch.size));

	pitch_env = EnvGen.kr(Env(pitch,[time]), gate, 1,0,1,0);


	subOsc  = SinOsc.ar(fr_000/2,0,0.1,0);
	square  = Pulse.ar(fr_000,0.9,0.1,0);
	saw     = Saw.ar(fr_000,0.2,0);
	sine    = SinOsc.ar(fr_000,0,0.3,0);

	sig = subOsc + square+ saw + sine;

	sig = RLPF.ar(sig,4000,0.5,1,0);

	sig = sig*pitch_env;

	Out.ar(0, Pan2.ar(sig*10));

}).store; //four_osc_chromagram
)
)



(
SynthDef(\testing_timbres, {
	arg out = 0,

	subOsc_mul = 0.1,
	square_mul = 0.1,
	saw_mul    = 0.1,
	sine_mul   = 0.1,

	cutoff     = 20000,
	rq         = 1,

	freq = 440;
	var sig, subOsc,square,saw,sine;

	subOsc = SinOsc.ar(freq/2,0,subOsc_mul,0);

	square = Pulse.ar(freq,0.9,square_mul,0);
	saw = Saw.ar(freq,saw_mul,0);
	sine = SinOsc.ar(freq,0,sine_mul,0);

	sig = subOsc + square+ saw + sine;

	sig = RLPF.ar(sig,cutoff,rq,1,0);

	Out.ar(0,Pan2.ar(sig))

}
).add;
)

(
Synth(\testing_timbres,[
	\freq,440,
	\subOsc_mul, 0.05,
	\square_mul, 0.1,
	\saw_mul   , 0.2,
	\sine_mul  , 0.3,

	\cutoff, 4000,
	\rq, 0.5
]);
)


(
SynthDef(\kalimba, {
	//source: https://sccode.org/1-51l
    |out = 0, freq = 440, amp = 0.1, mix = 0.1|
    var snd;
    // Basic tone is a SinOsc
    snd = SinOsc.ar(freq) * EnvGen.ar(Env.perc(0.005, Rand(2.5, 3.5), 1, -8), doneAction: 2);
    // The "clicking" sounds are modeled with a bank of resonators excited by enveloped pink noise
    snd = (snd * (1 - mix)) + (DynKlank.ar(`[
        // the resonant frequencies are randomized a little to add variation
        // there are two high resonant freqs and one quiet "bass" freq to give it some depth
        [240*ExpRand(0.9, 1.1), 2020*ExpRand(0.9, 1.1), 3151*ExpRand(0.9, 1.1)],
        [-7, 0, 3].dbamp,
        [0.8, 0.05, 0.07]
    ], PinkNoise.ar * EnvGen.ar(Env.perc(0.001, 0.01))) * mix);
    Out.ar(out, Pan2.ar(snd, 0, amp));
}).add;
)


Synth(\kalimba,[\freq,440,\amp,1]);




(
SynthDef(\rhodey_sc, {
    |
    // standard meanings
    out = 0, freq = 440, gate = 1, pan = 0, amp = 0.1,
    // all of these range from 0 to 1
    vel = 0.8, modIndex = 0.2, mix = 0.2, lfoSpeed = 0.4, lfoDepth = 0.1
    |
    var env1, env2, env3, env4;
    var osc1, osc2, osc3, osc4, snd;

    lfoSpeed = lfoSpeed * 12;

    freq = freq * 2;

    env1 = EnvGen.ar(Env.adsr(0.001, 1.25, 0.0, 0.04, curve: \lin));
    env2 = EnvGen.ar(Env.adsr(0.001, 1.00, 0.0, 0.04, curve: \lin));
    env3 = EnvGen.ar(Env.adsr(0.001, 1.50, 0.0, 0.04, curve: \lin));
    env4 = EnvGen.ar(Env.adsr(0.001, 1.50, 0.0, 0.04, curve: \lin));

    osc4 = SinOsc.ar(freq * 0.5) * 2pi * 2 * 0.535887 * modIndex * env4 * vel;
    osc3 = SinOsc.ar(freq, osc4) * env3 * vel;
    osc2 = SinOsc.ar(freq * 15) * 2pi * 0.108819 * env2 * vel;
    osc1 = SinOsc.ar(freq, osc2) * env1 * vel;
    snd = Mix((osc3 * (1 - mix)) + (osc1 * mix));
    snd = snd * (SinOsc.ar(lfoSpeed) * lfoDepth + 1);

    // using the doneAction: 2 on the other envs can create clicks (bc of the linear curve maybe?)
    snd = snd * EnvGen.ar(Env.asr(0, 1, 0.1), gate, doneAction: 2);
    snd = Pan2.ar(snd, pan, amp);

    Out.ar(out, snd);
}).add;
)

Synth(\rhodey_sc,[\freq,440]);








