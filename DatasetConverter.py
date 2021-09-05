class DatasetConverter:

    def __init__(self, data: []):
        self.time = []
        self.cpu = []
        self.mem = []
        if len(data) > 0:
            self.start_time = data[0]['_time']

        for element in data:
            self.time.append(element['_time'] - self.start_time)  # Можно перевести в человеческую дату, если это
            # значение unix_time (Aug 05 2021). В задании явно не было сказано, поэтому я сделал от нуля. На вид
            # графика это никак не влияет
            self.cpu.append(element['CPU'])
            self.mem.append(element['MEM'])
