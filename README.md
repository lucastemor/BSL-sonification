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
	<li>make tool for computing an sonifying sac chromagrams, not global, as is done now (DONE)</li>
	<li>Alternatively/additionally, precompute all sac chromagrams so big matgrix doesn't have to be read every time (DONE)</li>
	<li>Make a branch of BSL and document changes, eventually merge so these packages can work together</li>
	<li>get new add_sound to video working (DONE)</li>
	<li>Utility to bulk compute flat q etc. so we cna bulk compute q-sonifications for 50 cases</li>
	<li>debugging tools - mostly w.r.t. auido device seleciton </li>
	<li>Mac and linux cross-platform compatibility / install instructions</li>
	<li>Tutorial/examples plus descriptions of common naming confentions (e.g., Pxx, freqs, etc)</li>
</ul>


<b>To do lower priority:</b>
<ul>
	<li>Cleaner argument specification for add_sound_to_video.py</li>
	<li>clean up spectroharmonic_preprocessing.py</li>
	<li>clean up flat_q_with_spectro_env.py</li>
</ul>



## MacOs install instructions


1. Install supercollider (for synthesis)
2. Install Loopback for audio routing/recording. Note there are alternatives like soundflower or Jackctl that require a bit more setup but are free. Just need to create a virtual adoip device
3. Route loopback autop to output channels 1&2 and add MacOS' Built-in Output as a monitoring device
4. Open ./supercollider/synthdef_scripts/handy.scd using supercollider and change default device settings to the virtual audio device - e.g., Server.default.options.outDevice_("Loopback Audio");
5. Change memory alocation as well now that you're here (working defaults are saved), and remember to reboot server to initiate any changes
6. Test audio - open BSL-sonification/supercollider/synthdefscripts/handy.scd, boot the server and play the line with the sine tone. If you don't hear anything then you did not correctly route audio from Supercollider to the virtual device to the Mac's speakers 

7. conda environment: conda create -n sonify numpy pyaudio scikit-image scipy ; conda activate sonify; conda install -c conda-forge librosa; conda install -c conda-forge pyvista;  conda install -c conda-forge pyvistaqt; conda install ipython
8. pip install -e BSL-sonification/supercollider/.  for sc-pytohn library
9. pip install -e BSL-sonification/. for sonification library
10. pip install -e BSL-sonification/BSL-tools/. for Dan's tools
11. synth class (BSL-sonification/sonify/synth_classes/synth.py) -> set synthdef (e.g., /Documents/BSL-sonification/supercollider/synthdefs) path and sc path (e.g., '/Applications/SuperCollider.app/Contents/Resources/scsynth')

12. Change synth.audio_device attribute to be the same as your device from step 4 (e.g., "Loopack audio")
13. You should be able to run add_sound_to_video.py to generate an example sonificaiton+visualziation




## Linnux Install  instructions **incomplete** (just taking notes so I can remember everything that has to be done):</b>

1. Install supercollider - sudo apt-get supercollider 

2.  Setting up JACK and pulseaudio for recording (Linux)
<ul>
	<li>sudo apt-get install qjackctl pulseaudio-module-jack</li>
	<li>Then configure qjackctl to run the following command after startup. Copy it into "Setup..." > "Options" > "Execute script after Startup":</li>
	<li>pacmd set-default-sink jack_out</li>
	<li>see https://askubuntu.com/questions/572120/how-to-use-jack-and-pulseaudio-alsa-at-the-same-time-on-the-same-audio-device for more info on above</li>
	<li>Restart audio w/ pulseaudio -k && sudo alsa force-reload</li>
	<li>Open ubuntu settings > sound > output device change to Jack sink. Input device to Jack source
	<li>? I am stuck .. switching to mac ... </li>
</ul>


<ul>
	<li>other dependancy list - numpy, pyaudio, librosa, pyvistaqt, skimage etc .. </li>
	<li>pip install -e BSL-sonification/supercollider/.  for sc-pytohn library</li>
	<li>pip install -e BSL-sonification/. for sonification library</li>
	<li>pip install -e BSL-sonification/BSL-tools/. for Dan's tools</li>
	<li>synth class -> set synthdef path and sc path</li>
	<li>choose sound device</li>
	<li>handy.scd setup</li>
</ul>