from utillc import *
import numpy as np
import cv2
import numpy as np

from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects

screensize = (720,460)
EKO()

v1 = '/mnt/hd1/data/download/DJI_0099.MP4'
v2 = '/mnt/hd1/data/download/DJI_0100.MP4'


pano = (VideoFileClip(v2, audio=False).subclip("03:25", "03:44"))
#pano = pano.fx( vfx.speedx, 0.5)

title = (TextClip('Laura, Samuel & cie vus du ciel',
                   color='white',
#                  font="Amiri-Bold",
                   kerning = 5, fontsize=100).set_duration(2.5).fadein(.5).fadeout(.5))

title = title.set_pos('center').set_duration(10) 
title = CompositeVideoClip([pano, title]) 

descente = (VideoFileClip(v2, audio=False).subclip("03:47", "04:07")).crossfadein(2.0)

descente1 = (VideoFileClip(v2, audio=False).subclip("02:46", "03:16").fx(vfx.time_mirror).crossfadein(2.0))


group_survol_bas = (VideoFileClip(v2, audio=False)
                    .subclip("01:30", "01:52"))
        
group1_bas_remontee = VideoFileClip(v1, audio=False).subclip("00:16", "01:24")

survol_bas = VideoFileClip(v1, audio=False).subclip("02:14", "02:41")

remontee_descente_travelling = VideoFileClip(v1, audio=False).subclip("01:36", "02:07")        

group_coucou_survol = (VideoFileClip(v2, audio=False)
                       .subclip("00:11", "01:13"))
group_coucou_survol1 = (VideoFileClip(v2, audio=False)
                       .subclip("00:11", "00:20"))
group_coucou_survol2 = (VideoFileClip(v2, audio=False)
                       .subclip("00:20", "01:13"))


def concatenate_videoclips_fadeinout(video_clips) :
    video_fx_list = [video_clips[0]]
    # set padding to initial video
    padding = 2
    idx = video_clips[0].duration - padding
    for video in video_clips[1:]:
        video_fx_list.append(video.set_start(idx).crossfadein(padding))
        idx += video.duration - padding
    final_video = CompositeVideoClip(video_fx_list)
    return final_video

size = pano.size
EKOX(size)

credits = (TextClip('Musique \nPink Floy - High Hopes',
                    color='white',
                    font="Amiri-Bold",
                    kerning = 5, fontsize=100, size=size).set_duration(2.5).set_pos('center'))


w,h = size
white = np.ones((h,w,2))*255
flash = ImageClip(white, duration=0.2)
white = np.ones((h,w,2))*255
flash0 = ImageClip(white*0, duration=0.2)
EKOX(flash.size)
im = ImageClip("./detect.png", duration=3)
im = im.resize(newsize=(w,h))
EKOX(im.size)

annot = (TextClip('56 people detected,\n 00 boats detected',
                  color='green',
#                  font="Amiri-Bold",
                  kerning = 5, fontsize=60).set_duration(2).set_position("top"))
annot = CompositeVideoClip([im, annot])

group_coucou_survol12 =  concatenate_videoclips([group_coucou_survol1, flash, flash0, im, annot, group_coucou_survol2])

hello_pilote = VideoFileClip(v2, audio=False).subclip("02:22", "02:28")
EKO()

l = [ title, descente, group_survol_bas, group1_bas_remontee,
      remontee_descente_travelling,  group_coucou_survol12,
      hello_pilote,
      credits]

#l = [title, credits]

final = concatenate_videoclips(l)
EKOX(final.duration)
audio = (AudioFileClip("/mnt/hd2/data/PinkFloyd.mkv")
         .audio_fadein(2)
         .audio_fadeout(1).volumex(0.6))
#.set_duration(final.duration))

EKOX(audio.duration)
clic = AudioFileClip("/mnt/hd2/data/clic.mkv").set_duration(1).volumex(3)
audio = CompositeAudioClip([audio, clic.set_start("02:48")])
EKOX(audio.duration)

EKOX(audio)
audio = audio.set_duration(final.duration)
EKOX(audio.duration)
final = final.set_audio(audio)

EKOX(final.duration)
final.write_videofile("l2.mp4", fps=descente.fps,
                      audio_bitrate="1000k", bitrate="4000k")

        

