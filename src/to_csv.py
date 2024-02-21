import os
import csv


def find_report_files(p, suffix):
    content = ""

    suffix += ".txt"

    data_directory = os.path.join(p, 'data')

    if os.path.exists(data_directory):
        filenames = os.listdir(data_directory)

        filenames = [file for file in filenames if
                     file.lower().endswith(suffix)]

        for file_name in filenames:
            file_path = os.path.join(data_directory, file_name)
            with open(file_path, 'r') as file:
                file_content = file.read()
                content += file_content

    return content


def process_ratings(txt):
    dictionary = dict({'Hidde': [], 'Max': [], 'Gabriel': []})
    for line in txt.splitlines():
        name, rating = line.split(": ")
        if name in dictionary:
            dictionary[name].append(int(rating))
        else:
            dictionary[name] = [int(rating)]

    return dictionary


def process_reports(txt):
    dictionary = dict({'Hidde': [], 'Max': [], 'Gabriel': []})
    name = None
    result = None
    for line in txt.splitlines():
        line = line.split(' ')
        if len(line) > 0:
            if line[0] == "Match":
                name = line[2]
            if line[0] == "Result:":
                result = line[1]
                if name in dictionary:
                    dictionary[name].append(result)
                else:
                    dictionary[name] = [result]
                name = None
                result = None
    return dictionary


def write_to_csv(dictionary, file_name):
    with open(f'csv/{file_name}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(dictionary.keys())
        writer.writerows(zip(*dictionary.values()))


def main():
    ratings = find_report_files(os.getcwd(), "rating")
    reports = find_report_files(os.getcwd(), "report")

    ratings = process_ratings(ratings)
    reports = process_reports(reports)

    write_to_csv(ratings, 'ratings')
    write_to_csv(reports, 'reports')


if __name__ == '__main__':
    main()
