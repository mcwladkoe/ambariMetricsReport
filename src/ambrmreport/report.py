import os
import sys
import argparse

import pandas as pd

from .constants import (
    COLUMNS_DICT,
    COLUMNS_RANGE,
)


class MetricsData:
    def __init__(self, input_path):
        self.data = None
        self.input_path = input_path

    def get_data_from_folder(self):
        file_list = os.listdir(self.input_path)
        for file in file_list:
            name, ext = os.path.splitext(file)
            if ext == '.csv':
                self.get_data_from_file(os.path.join(self.input_path, file))

        # self.data.append(pd.DataFrame.from_records([COLUMNS_DICT]))
        # print(pd.DataFrame.from_records([COLUMNS_DICT]))
        # self.data.loc[len(self.data)] = COLUMNS_DICT
        self.data = self.data.reindex(columns=COLUMNS_DICT.keys())
        self.data = pd.concat([pd.DataFrame.from_records([COLUMNS_DICT]), self.data])

    def get_data_from_file(self, file_path):
        dat = pd.read_csv(file_path)
        if self.data is None:
            self.data = dat
            prev = 0
            step = 0
            for i in range(len(dat['Timestamp'])):
                if i == 0:
                    step = dat['Timestamp'][1] - dat['Timestamp'][0]
                    dat['Timestamp'][i] = 0
                else:
                    dat['Timestamp'][i] = prev + step
                    prev = dat['Timestamp'][i]
        else:
            del dat['Timestamp']
            self.data = pd.concat([self.data, dat], axis=1)


def write_results(data, output_path):
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    workbook = writer.book
    data.to_excel(writer, sheet_name='ambari', index=False)

    worksheet = writer.sheets['ambari']

    data_length = len(data)

    for index, col in enumerate(COLUMNS_RANGE):
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'values': '=ambari!${col}$3:${col}${length}'.format(
                col=col,
                length=data_length
            ),
            'categories': '=ambari!$A$3:$A${length}'.format(
                length=data_length
            ),
            'name': '=ambari!${col}$2'.format(col=col),
            })
        chart.set_x_axis({'name': 'Имя Теста', 'rotate': 90})
        chart.set_legend({'position': 'none'})
        offset = index % 4
        if offset == 0:
            worksheet.insert_chart('A{}'.format(data_length + (index // 4) * 15), chart)
        elif offset == 1:
            worksheet.insert_chart('I{}'.format(data_length + (index // 4) * 15), chart)
        elif offset == 2:
            worksheet.insert_chart('Q{}'.format(data_length + (index // 4) * 15), chart)
        elif offset == 3:
            worksheet.insert_chart('Y{}'.format(data_length + (index // 4) * 15), chart)

    writer.save()


def main(argv=sys.argv):
    description = """
        Get report for SparkMeasure metrics in XLS format with graphs.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input_path', metavar='input_path',
        help='Path to results folder')

    parser.add_argument('-o', '--output', dest='output_path',
        default='results.xlsx',
        help='Output file path')

    args = parser.parse_args(argv[1:])

    data = MetricsData(args.input_path)
    data.get_data_from_folder()

    if data.data is None:
        print('Input data folder is empty or no data found.')
        return
    write_results(data.data, args.output_path)


if __name__ == '__main__':
    main()
