import os

from blame.blame import *
from conflict.conflict import *
from line.line import *

def fill_blame_info(path):
    for cf in conflicts:
        current_lines = make_lines(cf.current_line, cf.file_path)
        incoming_lines = make_lines(cf.incoming_line, cf.file_path)

        blames.append(Blame(path, cf.file_path, current_lines, incoming_lines))
    
    return 0

def make_lines(conflict_line, file_path):
    msgs = os.popen('git blame -L %s %s' % (str(conflict_line)[1:-1].replace(' ', ''),
                    file_path)).read().split('\n')[:-1]
    
    lines = []
    for msg in msgs:
        rev = msg[:14]
        content = msg[msg.find(')') + 1:]
        author_info = list(filter(lambda x: x != '', msg[:msg.find(')')].split(' ')))
        line_num = author_info[-1]
        date = author_info[-4] + ' ' + author_info[-3]
        author_name = ' '.join(author_info[1:-4])
        author_name = author_name[author_name.find('(') + 1:]
        lines.append(Line(rev, author_name, date, line_num, content))

    return lines
