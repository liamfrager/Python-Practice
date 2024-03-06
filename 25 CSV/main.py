import csv
import pandas

# with open("./weather_data.csv", mode='r') as data_file:
#     data = csv.reader(data_file)
#     next(data, None)
#     temperatures = []
#     for row in data:
#         temperatures.append(int(row[1]))
# print(temperatures)

# data = pandas.read_csv('./weather_data.csv')
# avg_temp = data.temp.mean()
# hottest_temp = data.temp.max()

# hottest_day = data[data.temp == hottest_temp]
# # print(hottest_day)


# monday_temp_c = data[data.day == 'Monday'].temp
# monday_temp_f = (monday_temp_c * 9/5) + 32
# print(monday_temp_f)


data = pandas.read_csv(
    './2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv')

fur_colors = data['Primary Fur Color'].unique()[1:]

squirrel_counts = []
for color in fur_colors:
    count = len(data[data['Primary Fur Color'] == color])
    squirrel_counts.append(count)

squirrel_data = {
    "Fur Color": fur_colors,
    "Count": squirrel_counts,
}

squirrel_colors_csv = pandas.DataFrame(squirrel_data)
squirrel_colors_csv.to_csv('./squirrel_count.csv')
print(squirrel_colors_csv)
