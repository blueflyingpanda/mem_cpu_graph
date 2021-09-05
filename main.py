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


def main():
    thin_out = 2
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

        plt.xlabel('time')
        plt.ylabel('cpu')
        plt.title('cpu usage x' + str(thin_out))
        plt.plot(dh.time[::thin_out], dh.cpu[::thin_out])
        plt.show()

        plt.xlabel('time')
        plt.ylabel('mem')
        plt.title('memory usage x' + str(thin_out))
        plt.plot(dh.time[::thin_out], dh.mem[::thin_out])
        plt.show()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
