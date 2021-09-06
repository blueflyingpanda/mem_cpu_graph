from io import TextIOWrapper
import json
import requests
import os
import matplotlib.pyplot as plt
import DatasetConverter as DConverter

tmp_filename = 'tmp.json'
actual_filename = 'dataset_cpu_mem.json'


def parse_dataset(file: TextIOWrapper) -> []:
    time_mem_cpu_data = []
    for line in file:
        time_mem_cpu_data.append(json.loads(line))
    return time_mem_cpu_data


def download_file() -> TextIOWrapper:
    resp = requests.get('http://80.211.168.161/dataset_cpu_mem.json', allow_redirects=True)
    with open(tmp_filename, 'w+') as tmp_file:
        tmp_file.write(resp.text)
        tmp_file.seek(0)
        file = open(actual_filename, 'w+')
        for line in tmp_file:
            line = line.replace('_time', '"_time"').replace('CPU', '"CPU"').replace('MEM', '"MEM"')
            file.write(line)
        file.seek(0)
        os.remove(tmp_filename)
        return file


def get_list_from_dataset() -> []:
    if os.path.exists(actual_filename):
        with open(actual_filename, 'r') as file:
            return parse_dataset(file)
    else:
        with download_file() as file:
            return parse_dataset(file)


""""http://paulbourke.net/geometry/pointlineplane/"""


def perpendicular_distance(x1, y1, x2, y2, x3, y3):  # x3,y3 координаты точки
    px = x2 - x1
    py = y2 - y1

    norm = px * px + py * py

    if norm is 0:
        return 0

    u = ((x3 - x1) * px + (y3 - y1) * py) / norm

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    dist = (dx * dx + dy * dy)

    return dist


""""оптимизация по времени"""


def compress_data_wrapper(original_value, original_time, compressed_value, compressed_time, scale=2):
    begin = 0
    # чем больше step тем точнее алгоритм, но тем дольше по времени он исполняется
    step = 100
    end = step
    while begin < len(original_value):
        tmp_compressed_value = []
        tmp_compressed_time = []
        compress_data(original_value[begin:end], original_time[begin:end], tmp_compressed_value, tmp_compressed_time,
                      scale)
        compressed_value += tmp_compressed_value
        compressed_time += tmp_compressed_time
        begin += step
        end += step


def find_insert_pos(array, val):
    i = 0
    while i < len(array):
        if array[i] > val:
            return i
        i += 1
    return i


""""https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm"""


def compress_data(original_value, original_time, compressed_value, compressed_time, scale=2):
    limit = len(original_value) - len(original_value) // scale
    compressed_value.append(original_value[0])
    compressed_time.append(original_time[0])
    compressed_value.append(original_value[len(original_value) - 1])
    compressed_time.append(original_time[len(original_time) - 1])
    while len(compressed_value) < limit:
        i = 0
        j = 0
        d_max = 0
        index = 0
        jndex = 0
        while i < len(original_value) - 1:
            if original_time[i] == compressed_time[j + 1]:
                j += 1
            if original_time[i] == compressed_time[j]:
                i += 1
                continue
            d = perpendicular_distance(compressed_value[j], compressed_time[j],
                                       compressed_value[j + 1], compressed_time[j + 1],
                                       original_value[i], original_time[i])
            if d > d_max:
                d_max = d
                index = i
                jndex = j
            i += 1
        compressed_value.insert(jndex + 1, original_value[index])
        compressed_time.insert(jndex + 1, original_time[index])


def main():
    try:
        dh = DConverter.DatasetConverter(get_list_from_dataset())
        plt.style.use('dark_background')

        plt.xlabel('time')
        plt.ylabel('cpu')
        plt.title('cpu usage')
        plt.plot(dh.time, dh.cpu)
        plt.show()

        plt.xlabel('time')
        plt.ylabel('mem')
        plt.title('memory usage')
        plt.plot(dh.time, dh.mem)
        plt.show()

        time_cpu = []
        time_mem = []
        cpu = []
        mem = []

        compress_data_wrapper(dh.cpu, dh.time, cpu, time_cpu)

        plt.xlabel('time')
        plt.ylabel('cpu')
        plt.title('cpu usage rdp')
        plt.plot(time_cpu, cpu)
        plt.show()

        compress_data_wrapper(dh.mem, dh.time, mem, time_mem)

        plt.xlabel('time')
        plt.ylabel('mem')
        plt.title('memory usage rdp')
        plt.plot(time_mem, mem)
        plt.show()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
