from bs4 import BeautifulSoup # импортируем библиотеку для работы с HTML страницы, для поиска тегов и информации в них
import os # библиотека для работы с системными функциями и переменными
import wget # библиотека, которая скачивает любой документ из интернета по прямой ссылке

url = 'https://www.gismeteo.ru/city/hourly/4445/#wdaily2' # адрес страницы с прогнозом погоды
exeFolder = os.getcwd() # получение папки, из которой была запущена программа
fileName = 'download.wget' # название файла, в который будет сохранен HTML страницы
path = exeFolder + '\\' + fileName # полный путь к файлу

if fileName in os.listdir(exeFolder):
	os.remove(path) # удалить файл с разверткой страницы, если он был заранее для того, чтобы получить актуальную информацию 

wget.download(url, exeFolder) # скачиваем файл с разверткой с url в exeFolder

with open(path, 'r', encoding='utf-8') as htmlFile: # открываем файл с разверткой в режиме чтения (r) с нужной кодировкой
		file = htmlFile.read() # записываем в file всю разметку

soup = BeautifulSoup(file, "html.parser") # создаем объект парсера bs4 и указываем файл разметки

soupDates = soup.findAll("div", "wtab") # поиск в разметке всех тегов div с классом "wtab"
dates = []
for date in soupDates:
	dates.append(date.dd.text) # в каждом результате ищем тег <dd> и записываем его содержимое в список, в итоге получаем список дат

tableRows = soup.findAll("tr", "wrow") # получаем основную таблицу, в которой находятся весь прогноз (каждые 3 часа на 3 дня)
forecast = []
for trow in tableRows: # проходясь по каждому ряду в таблице, добавляем в список: время, характеристику и температуру
	forecast.append([trow.th.text.strip(), trow.find("td", "cltext").text, trow.find("span", "value m_temp c").text])

for f in range(len(forecast)):
	forecast[f][0] = dates[f // 8] + ' ' + forecast[f][0] # добавляем к каждой ячейке времени дату
# print(forecast)

with open(exeFolder + "\\forecast_table.csv", "w") as table: # открываем в папке, из которой запущена программа, файл на запись
	table.write(";".join(['Дата и время', 'Характеристика погоды', 'Температура']) + '\n') # выводим заголовки таблицы
	for i in forecast:
		table.write(";".join(i) + '\n') # выводим каждый элемент списка-результата в файл
	print(table.name) # выводим путь к сохраненному файлу