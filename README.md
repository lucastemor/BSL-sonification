# BSL-sonification
Tools for sonification of BSL data, examples, documentation

## Current state:
<ul>
	<li>Spectrogram feature, flat q, and chromagram synthdefs all working on lab linux workstation</li>
	<li>utility to render audio and sync with video working on lab linux workstation</li>
</ul>

<b>To do (roughly temporal order):</b>
<ul>
	<li>documentation for preprocessing.py (DONE)</li>
	<li>Figure out how to automate docs properly (DONE) </li>
	<li> documentation for synth, pythonsynthdefs, chromagram, addsoundtovideo </li>
	<li>finish other synthdefs - resynth, piched/noise only, chromagram, (done) flat_q (done)</li>
	<li>make tool for computing an sonifying sac chromagrams, not global, as is done now</li>
	<li>Alternatively/additionally, precompute all sac chromagrams so big matgrix doesn't have to be read every time</li>
	<li>Make a branch of BSL and document changes, eventually merge so these packages can work together</li>
	<li>get new add_sound to video working (DONE)</li>
	<li>Utility to bulk compute flat q etc. so we cna bulk compute q-sonifications for 50 cases</li>
	<li>debugging tools - mostly w.r.t. auido device seleciton </li>
	<li>Mac and linux cross-platform compatibility / install instructions</li>
	<li>Tutorial/examples plus descriptions of common naming confentions (e.g., Pxx, freqs, etc)</li>
</ul>


<b>To do lower priority:</b>
<ul>
	<li>Ckeaner argument specification for add_sound_to_video.py</li>
	<li>clean up spectroharmonic_preprocessing.py</li>
	<li>clean up flat_q_with_spectro_env.py</li>
</ul>



<b>Install  instructions (just taking notes so I can remember everything that has to be done):</b>
<ul>
	<li>other dependancy list - numpy, pyaudio, etc .. </li>
	<li>pip install -e BSL-sonification/supercollider/.  for sc-pytohn library</li>
	<li>pip install -e BSL-sonification/. for sonification library</li>
	<li>synth class -> set synthdef path and sc path</li>
	<li>choose sound device</li>
	<li>handy.scd setup</li>
</ul>