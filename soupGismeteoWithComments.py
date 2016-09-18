from bs4 import BeautifulSoup
import os
import wget

url = 'https://www.gismeteo.ru/city/hourly/4445/#wdaily2'
exeFolder = os.getcwd()
fileName = 'download.wget'
path = exeFolder + '\\' + fileName

if fileName in os.listdir(exeFolder):
	os.remove(path)

wget.download(url, exeFolder)

with open(path, 'r', encoding='utf-8') as htmlFile:
		file = htmlFile.read()

soup = BeautifulSoup(file, "html.parser")

soupDates = soup.findAll("div", "wtab")
dates = []
for date in soupDates:
	dates.append(date.dd.text)

tableRows = soup.findAll("tr", "wrow")
forecast = []
for trow in tableRows:
	forecast.append([trow.th.text.strip(), trow.find("td", "cltext").text, trow.find("span", "value m_temp c").text])

for f in range(len(forecast)):
	forecast[f][0] = dates[f // 8] + ' ' + forecast[f][0]
# print(forecast)

with open(exeFolder + "\\forecast_table.csv", "w") as table:
	table.write(";".join(['Дата и время', 'Характеристика погоды', 'Температура']) + '\n')
	for i in forecast:
		table.write(";".join(i) + '\n')
	print(table.name)