import re

from DataSet import DataSet, SKIP

width = 400
height = 300
length = 30
padding = 40
page_width = 540
page_height = 720
datasets = []
space = 0
current_line = 0


def x(index: int) -> float:
    return padding + index * space + length * index


def y(data: float, delta: float, max: float) -> float:
    return padding + (max - data) * height / delta


def draw_bold_line(x: float, y: float) -> str:
    return f'''<graphic
BoundingBox="{x} {y} {x + length} {y}"
LineType="Bold"
GraphicType="Line" />
'''


def draw_dashed_line(x1: float, y1: float, x2: float, y2: float) -> str:
    return f'''<graphic
BoundingBox="{x1} {y1} {x2} {y2}"
LineType="Dashed"
GraphicType="Line" />
'''


def preamble(p: str):
    global width, height, length, padding, page_width, page_height
    try:
        matches = re.match(r'%(?:w|width)=(\d+)', p, re.I)
        if matches:
            width = int(matches.group(1))
            print(f'Set width: {width}')
            return
        matches = re.match(r'%(?:h|height)=(\d+)', p, re.I)
        if matches:
            height = int(matches.group(1))
            print(f'Set height: {height}')
            return
        matches = re.match(r'%(?:l|length)=(\d+)', p, re.I)
        if matches:
            length = int(matches.group(1))
            print(f'Set length: {length}')
            return
        matches = re.match(r'%(?:pw|pagewidth)=(\d+)', p, re.I)
        if matches:
            page_width = int(matches.group(1))
            print(f'Set page width: {page_width}')
            return
        matches = re.match(r'%(?:ph|pageheight)=(\d+)', p, re.I)
        if matches:
            page_height = int(matches.group(1))
            print(f'Set page height: {page_height}')
            return
        matches = re.match(r'%(?:pd|padding)=(\d+)', p, re.I)
        if matches:
            padding = int(matches.group(1))
            print(f'Set padding: {padding}')
            return
    except ValueError:
        raise Exception(f'Wrong preamble value: {p}')
    raise Exception(f'Wrong preamble: {p}')


s = ''
try:
    input_file = open('input.edf', 'r')
    s = input_file.readline().strip('\n')
    current_line += 1
    while s.startswith('%'):
        preamble(s)
        s = input_file.readline().strip('\n')
        current_line += 1

    while True:
        if s.startswith('%'):
            raise Exception(f'''Wrong syntax at line {current_line}: '{s}' should write in preamble''')
        if s.startswith('#'):
            pass
        elif s == '':
            s = input_file.readline().strip('\n')
            current_line += 1
            if s == '':
                break
            else:
                continue
        else:
            dataset = DataSet()
            dataset.set_data(s)
            s = input_file.readline().strip('\n')
            current_line += 1
            if s != '':
                dataset.set_labels(s)
            datasets.append(dataset)

        s = input_file.readline().strip('\n')
        current_line += 1

    print('end')
    if len(datasets) == 0:
        raise Exception('''Missing data.
--- At least one set of data must be provided.''')
    count = datasets[0].count
    delta_energy = datasets[0].delta_energy
    max_energy = datasets[0].max_energy
    for dataset in datasets:
        count = max(count, dataset.count)
        delta_energy = max(delta_energy, dataset.delta_energy)
        max_energy = max(max_energy, dataset.max_energy)
    space = (width - length * count) / (count - 1)

    diagram = ''
    for dataset in datasets:
        data = dataset.data
        current = -1
        for i in range(dataset.count):
            if data[i] == SKIP:
                continue
            if current != -1:
                diagram += draw_dashed_line(x(current) + length, y(data[current], delta_energy, max_energy),
                                            x(i), y(data[i], delta_energy, max_energy))
            current = i
            diagram += draw_bold_line(x(i), y(data[i], delta_energy, max_energy))

    output_file = open('output.cdxml', 'w')
    output_file.write(f'''<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE CDXML SYSTEM "http://www.cambridgesoft.com/xml/cdxml.dtd" >
<CDXML
 ><colortable>
<color r="1" g="1" b="1"/>
<color r="0" g="0" b="0"/>
<color r="1" g="0" b="0"/>
<color r="1" g="1" b="0"/>
<color r="0" g="1" b="0"/>
<color r="0" g="1" b="1"/>
<color r="0" g="0" b="1"/>
<color r="1" g="0" b="1"/>
</colortable><fonttable>
<font id="3" charset="iso-8859-1" name="Arial"/>
</fonttable><page
 id="5"
 BoundingBox="0 0 {max(width + 2 * padding, page_width)} {max(height + 2 * padding, page_height)}"
 Width="{max(width + 2 * padding, page_width)}"
 Height="{max(height + 2 * padding, page_height)}"
 HeaderPosition="36"
 FooterPosition="36"
 PrintTrimMarks="yes"
 DrawingSpace="poster"
>
{diagram}
</page></CDXML>''')
except Exception as e:
    print(f'''Error at line {current_line}: {e}''')
    raise
