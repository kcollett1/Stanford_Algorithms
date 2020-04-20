#!/Users/kcolletti1/opt/anaconda3/bin/python3


import math
import matplotlib.pyplot as plt


def main():
    ''' Just looking at the data before applying the nearest neighbor TSP heuristic to it '''
    with open('nn.txt') as graph_info:
        num_verts = int(next(graph_info).strip())
        xcoords = [None for _ in range(num_verts)]
        ycoords = [None for _ in range(num_verts)]
        for vert_info in graph_info:
            vert_info = vert_info.strip().split(' ')
            i = int(vert_info[0]) - 1
            xcoords[i] = float(vert_info[1])
            ycoords[i] = float(vert_info[2])

    #maxdist2 = 0
    #mindist2 = float('inf')
    #for i in range(num_verts - 1):
    #    if i % 5000 == 0: print('calculating pairs for vertex', i)
    #    for j in range(i + 1, num_verts):
    #        dx = xcoords[i] - xcoords[j]
    #        dy = ycoords[i] - ycoords[j]
    #        dist2 = dx**2 + dy**2
    #        if dist2 < mindist2: mindist2 = dist2
    #        if dist2 > maxdist2: maxdist2 = dist2
    #print('min and max distances squared (respectively):', mindist2, maxdist2)
    #print('and true min/max distances:', math.sqrt(mindist2), math.sqrt(maxdist2))

    f = plt.figure()
    axes = f.add_axes([0.1,0.1,0.8,0.8])
    plt.scatter(xcoords,ycoords, marker='.')
    axes.set_xlim([min(xcoords)-100, max(xcoords)+100])
    axes.set_ylim([min(ycoords)-100, max(ycoords)+100])
    plt.show()


if __name__ == "__main__":
    main()
    raise SystemExit
