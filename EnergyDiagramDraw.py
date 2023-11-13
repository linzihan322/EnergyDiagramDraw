import re
import sys

from DataSet import DataSet, SKIP
from EDDrawException import *

width = 400
height = 300
length = 30
padding = 40
page_width = 540
page_height = 720
space = 0

NUMBER_FONT = 3
LABEL_FONT = 20


def x(index: int) -> float:
    return round(padding + index * space + length * index, 2)


def y(data: float, delta: float, max: float) -> float:
    return round(padding + (max - data) * height / delta, 2)


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


def draw_text(text: str, x: float, y: float, font: int, size: int, bold: bool = False) -> str:
    return f'''<t
 p="{x} {y}"
 CaptionJustification="Center"
 Justification="Center"
 LineHeight="auto"
><s font="{font}" size="{size}" color="0" {'face="1"' if bold else ''}>{text}</s></t>
'''


def preamble(source_line, p: str):
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
        raise EDDrawPreambleParserException(source_line, f'''Wrong preamble value: {p}
--- Please input an integer, and make sure there are no spaces before or after '='.''')
    raise EDDrawPreambleParserException(source_line, f'''\'{p}' is not a valid preamble statement.
--- Please read 'README.md'.''')


def main(argv=None):
    global space
    current_line = 0
    datasets = []
    try:
        if argv is None:
            argv = sys.argv[1:]
        if len(argv) == 0:
            raise EDDrawInternalException('Input file required.')
        if len(argv) > 2:
            raise EDDrawInternalException('Too many parameters.')
        input_filename = argv[0]
        output_filename = re.sub(r'\.edf$', '', argv[1] if len(argv) == 2 else input_filename)
        if not output_filename.endswith('.cdxml'):
            output_filename += '.cdxml'
        with open(input_filename, 'r') as input_file:
            print(f'''Reading file '{input_filename}'...''')
            s = input_file.readline().strip('\n')
            current_line += 1
            while s.startswith('%'):
                preamble(current_line, s)
                s = input_file.readline().strip('\n')
                current_line += 1

            while True:
                if s.startswith('%'):
                    raise EDDrawPreambleParserException(current_line, f'''\'{s}' should write in preamble part''')
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
                    dataset = DataSet(current_line)
                    dataset.set_data(s)
                    print(f'Parsing data at line {current_line}...')
                    s = input_file.readline().strip('\n')
                    current_line += 1
                    if s != '':
                        dataset.set_labels(s)
                        print(f'Parsing labels at line {current_line}...')
                    datasets.append(dataset)

                s = input_file.readline().strip('\n')
                current_line += 1

        print(f'''Finished reading the file '{input_filename}'.''')
        if len(datasets) == 0:
            raise EDDrawDataParserException(-1, '''Missing data.
--- At least one set of data must be provided.''')
        count = datasets[0].count
        delta_energy = datasets[0].delta_energy
        max_energy = datasets[0].max_energy
        for dataset in datasets:
            count = max(count, dataset.count)
            delta_energy = max(delta_energy, dataset.delta_energy)
            max_energy = max(max_energy, dataset.max_energy)
        space = (width - length * count) / (count - 1)

        print('Generating energy diagram...')
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
                diagram += draw_text(str(data[i]), x(i) + length / 2, y(data[i], delta_energy, max_energy) - 5,
                                     NUMBER_FONT, 10)
                if dataset.labels is not None:
                    diagram += draw_text(str(dataset.labels[i]), x(i) + length / 2,
                                         y(data[i], delta_energy, max_energy) + 15, LABEL_FONT, 12, bold=True)

        with open(output_filename, 'w') as output_file:
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
<font id="{NUMBER_FONT}" charset="iso-8859-1" name="Arial"/>
<font id="{LABEL_FONT}" charset="iso-8859-1" name="Times New Roman"/>
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
        print(f'''Successful output file '{output_filename}'.''')
        print('Finished.')
        print('-------------------------------------')
        print('EnergyDiagramDraw by Zihan Lin @ USTC')
    except EDDrawException as e:
        print(e)
    except Exception as e:
        print(f'''Unknown error: {e}''')
        raise


if __name__ == '__main__':
    sys.exit(main())
