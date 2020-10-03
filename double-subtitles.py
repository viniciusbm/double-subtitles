#!/usr/bin/env python3

import sys
import re

class Sub:
    def __init__(self, text):
        p1 = re.compile('(\r?\n){2,}', re.DOTALL)
        p2 = re.compile(r'\d+ *\r?\n(\d+):(\d+):(\d+)[.,](\d+) *--> *(\d+):(\d+):(\d+)[.,](\d+) *\r?\n(.*)', re.DOTALL)
        self.items = []
        for item in p1.split(text):
            m = p2.match(item)
            if m:
                self.items.append([3600 * int(m.group(1)) + 60 * int(m.group(2)) + int(m.group(3)) + float('0.' + m.group(4)),
                                   3600 * int(m.group(5)) + 60 * int(m.group(6)) + int(m.group(7)) + float('0.' + m.group(8)),
                                   m.group(9)]);
        self.current = 0

    def next_time(self):
        if self.current == len(self.items):
            return float('Inf')
        return self.items[self.current][0]

    def next_dialogue(self):
        if self.next_time() == float('Inf'):
            return [0, 0, '']
        self.current += 1
        return self.items[self.current - 1]


header = '''[Script Info]
Title: Merged subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
Collisions: Normal
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TOP,default,35,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,1,8,10,10,5,1
Style: BOT,default,45,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,4,3,2,10,10,8,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text'''

def time_to_string(t):
    cs = t % 1
    t = int(t)
    s = t % 60
    t //= 60
    m = t % 60
    t /= 60
    h = t
    return '%1d:%02d:%02d.%02d' % (h, m, s, round(100 * cs))

def convert_tags(s):
    s = s.replace('<i>', '{\\i1}')
    s = s.replace('<b>', '{\\b1}')
    s = s.replace('<u>', '{\\u1}')
    s = re.sub(r'<font\s*color\s*=\s*[\'"]#(..)(..)(..)[\'"]\s*>(.*?)</font>', r'{\\c&H\3\2\1&}\4{\\c}', s, flags=re.DOTALL)
    s = s.replace('</i>', '{\\i0}')
    s = s.replace('</b>', '{\\b0}')
    s = s.replace('</u>', '{\\u0}')
    s = s.replace('\r', '')
    s = s.replace('\n', '\\N')
    return s

def print_dialogue(item, style_name):
    print('Dialogue: 0,%s,%s,%s,,0,0,0,,%s' % (time_to_string(item[0]), time_to_string(item[1]), style_name, convert_tags(item[2])))


def parse(filename, encoding):
    try:
        with open(filename, "r", encoding=encoding) as f:
            s = Sub(f.read())
        return s
    except:
        return None

encodings = ['utf-8-sig', 'ascii', 'cp1252', 'utf-8']

for enc in encodings:
    s1 = parse(sys.argv[1], enc)
    if s1:
        break

for enc in encodings:
    s2 = parse(sys.argv[2], enc)
    if s2:
        break

if s1 is None:
    print('Could not open the first file', file=sys.stderr)
if s2 is None:
    print('Could not open the second file', file=sys.stderr)
if s1 is None or s2 is None:
    exit(1)


print(header)

inf = float('Inf')
while s1.next_time() < inf or s2.next_time() < inf:
    if s1.next_time() < s2.next_time():
        print_dialogue(s1.next_dialogue(), 'TOP')
    else:
        print_dialogue(s2.next_dialogue(), 'BOT')

