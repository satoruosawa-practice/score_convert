import turtle
from bs4 import BeautifulSoup

def extractMusic(soup):
    """ Extract music data from xml file. """
    pitch_list = []
    cur_time = 0 # Current time
    tmp_duration = 0
    # parse
    for m in soup.find_all("measure"):
        for nb in m.find_all({"note", "backup"}):
            if nb.name == "backup": # 巻き戻し
                cur_time -= int(nb.duration.string)
            if nb.name == "note":
                if not nb.chord: # 和音でなければ
                    cur_time += tmp_duration
                if nb.pitch: # 音符
                    pitch_list.append([cur_time,
                                       nb.pitch.octave.string,
                                       nb.pitch.step.string,
                                       nb.accidental.string])
                if nb.rest: # 休符
                    pass
                if nb.duration: # 装飾音はdurationないので飛ばす
                    tmp_duration = int(nb.duration.string)
    return pitch_list

def pitchId(pitch):
    """ Calculate absolute height of given pitch. """
    if pitch[2] == "sharp":
        code_list = ["", "c", "", "d", "", "", "f", "", "g", "", "a", ""]
        if pitch[1].lower() == "e" or pitch[1].lower() == "b":
            print("error: " + pitch[1].lower() + " " + pitch[2])
    elif pitch[2] == "flat":
        code_list = ["" ,"d", "", "e", "", "", "g", "", "a", "", "b", ""]
        if pitch[1].lower() == "c" or pitch[1].lower() == "f":
            print("error: " + pitch[1].lower() + " " + pitch[2])
    else:
        code_list = ["c", "", "d", "", "e", "f", "", "g", "", "a", "", "b"]
    p_id =  int(pitch[0]) * 12 - 9
    p_id += code_list.index(pitch[1].lower())
    return p_id

def freq(pitch_id):
    freq_list = [
        27.5, 29.135, 30.868,
        32.703, 34.648, 36.708, 38.891, 41.203, 43.654,
        46.249, 48.999, 51.913, 55, 58.27, 61.735,
        65.406, 69.296, 73.416, 77.782, 82.407, 87.307,
        92.499, 97.999, 103.826, 110, 116.541, 123.471,
        130.813, 138.591, 146.832, 155.563, 164.814, 174.614,
        184.997, 195.998, 207.652, 220, 233.082, 246.942,
        261.626, 277.183, 293.665, 311.127, 329.628, 349.228,
        369.994, 391.995, 415.305, 440, 466.164, 493.883,
        523.251, 554.365, 587.33, 622.254, 659.255, 698.456,
        739.989, 783.991, 830.609, 880, 932.328, 987.767,
        1046.502, 1108.731, 1174.659, 1244.508, 1318.51, 1396.913,
        1479.978, 1567.982, 1661.219, 1760, 1864.655, 1975.533,
        2093.005, 2217.461, 2349.318, 2489.016, 2637.02, 2793.826,
        2959.955, 3135.963, 3322.438, 3520, 3729.31, 3951.066, 4186.009
    ]
    freq = freq_list[pitch_id]
    return freq

xml_name = './src/data/data.xml'
soup = BeautifulSoup(open(xml_name, 'r').read(), "html.parser")

parts = soup.find_all('part')

part = extractMusic(parts[0])

for p in part:
    print(freq(pitchId(p[1:])))
