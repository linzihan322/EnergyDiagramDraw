# EnergyDiagramDraw

## About

EnergyDiagramDraw is a ready-to-use energy diagram drawing program written in Python.

## Requires

- Python 3.9
- ChemDraw (for diagram viewing)

## Usage

You have the flexibility to specify both the input and output file names.
For the input file, the file extension can be anything (using `.edf`, represented `EnergyDiagramFile`, is recommended).
However, for the output file, the extension must be `.cdxml`.
If you choose not to provide an output filename, the program will automatically change the input file’s extension
from `.edf` to `.cdxml` (for other input file extensions, it will directly append `.cdxml`).

Assuming the input file is `INPUT.edf`, you can execute the following command to generate energy diagram.
For certain systems, you might need to replace `python` with `python3`.

```shell
python EnergyDiagramDraw.py INPUT.edf
python EnergyDiagramDraw.py INPUT.edf OUTPUT.cdxml
```

## Structure of `.edf` file

A `.edf` file contains two parts: `preamble` and `data & labels`.

```edf
preamble - starts with '%', used to set the property of diagram
[blank line]
data
labels - optional
[blank line] - for more data, just repeat this part
data
labels - optional
```

### Preamble

Preamble can change property of diagram. You can write in any order.

| Long format  | Short format | Default value | Note                                                                                      |
|--------------|--------------|---------------|-------------------------------------------------------------------------------------------|
| %width=      | %w=          | 400           | Set the width of diagram                                                                  |
| %height=     | %h=          | 300           | Set the height of diagram                                                                 |
| %length=     | %l=          | 30            | Set the length of energy line                                                             |
| %padding     | %pd=         | 40            | Set the padding of diagram                                                                |
| %pagewidth=  | %pw=         | 540           | Set the width of page<br/>This value will be ignored if less than (width + 2 * padding)   |
| %pageheight= | %ph=         | 720           | Set the height of page<br/>This value will be ignored if less than (height + 2 * padding) |

![preamble.svg](preamble.svg)

### Data and labels

This section contains one or two lines.
The first line consists of data separated by commas.
And the second line represents labels (which are optional).
In either the data or label lines, you can leave empty spaces to skip certain points.
However, it’s essential to ensure that the number of labels corresponds exactly to the number of data points.

You can repeat this part if you want to draw more data in one diagram.
Remember to separate with blank lines.

### Simplest example

The simplest edf file contains only data. Like this:

```edf
1.0,2.0,3.0,4.0,5.0
```

For more examples, please see the files in `examples` folder.

## Author

Zihan Lin @ USTC

linzihan322@mail.ustc.edu.cn