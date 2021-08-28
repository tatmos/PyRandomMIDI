

# mido関連
import mido 
from mido import Message
from mido import Message, MidiFile, MidiTrack, MetaMessage
# 乱数
import random
# 時刻
import time


# 再生用のMIDI Port名取得（良き出力ポートを選ぶ）
ports = mido.get_output_names()
print(ports)
port = ports[2]


# MIDIノートを作る
def makenote(track,note,length,velocity):
    track.append(Message('note_on', note=note, velocity=velocity, time=0))
    track.append(Message('note_off', note=note, velocity=0,time=int(length)))


# ノート生成
mid = MidiFile()

# track
for repat in range(0,3):
    track = MidiTrack()
    mid.tracks.append(track)


# テンポ
mid.tracks[0].append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(128)))

# Track1
for repeat in range(0,32 * 4): 
    makenote(mid.tracks[0],int(random.uniform(55, 101)),int(480 / (1 + repeat % 2)),int(random.uniform(32,127)))

# Track2
for repeat in range(0,32 * 3): 
    makenote(mid.tracks[1],int(random.uniform(36, 70)),int(480 / (1 + repeat % 3)),int(random.uniform(32,127)))
   
# Track3
for repeat in range(0,32 * 2): 
    makenote(mid.tracks[1],int(random.uniform(36, 48)),int(480 / (1 + repeat % 4)),int(random.uniform(96,127)))

# MIDIファイル保存
mid.save('new_song.mid')


# 再生
with mido.open_output(port) as outport:
    for msg in mido.MidiFile('new_song.mid'):
        time.sleep(msg.time)
        if not msg.is_meta:
            print(outport, msg)
            outport.send(msg) 