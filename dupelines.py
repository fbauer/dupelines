'''Show similarities in a text file, graphically'''

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pylab import plot, show
import sys

def show_similiarities(filename):
    f = open(filename, 'r')
    #lines = f.readlines()
    lines = f.read()
    x_positions = []
    y_positions = []
    lines_x = []
    lines_y = []
    possible_line_continuations = {}
    for xPos, first_line in enumerate(lines[:-1]):
        for yPos, second_line in enumerate(lines[xPos+1:]):
            if first_line == second_line and first_line != '\n':
                if (xPos, yPos) in possible_line_continuations:
                    possible_line_continuations[xPos + 1, yPos + 1] =\
                    possible_line_continuations.pop((xPos, yPos))
                else:
                    possible_line_continuations[xPos + 1, yPos + 1] = (xPos, yPos)
                x_positions.append(xPos)
                y_positions.append(yPos)
    
    for after_line_end in possible_line_continuations.iterkeys():
        start = possible_line_continuations[after_line_end]
        stop = (after_line_end[0]-1, after_line_end[1]-1)
        if start != stop:
            lines_x.extend(range(start[0] - 1, after_line_end[0]))
            lines_y.extend(range(start[1] - 1, after_line_end[1]))
    plot(x_positions, y_positions, 'b.')
    plot(lines_x, lines_y, 'ro')
    show()
if __name__ == '__main__':
    show_similiarities(sys.argv[1])
    

