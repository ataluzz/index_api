## API для индексации папок и файлов

Данное приложение предоставляет совокупную статистику для папок и файлов по следующим показателям:
- Список вложенных папок *(только при сканировании папки)*
- Список вложенных файлов *(только при сканировании папки)*
- Общее количество файлов *(только при сканировании папки)*
- 5 наиболее часто встречающихся слов
- 5 слов из числа наиболее редко встречающихся слов
- Средняя длина слова
- Процент гласных букв от их общего количества
- Процент согласных букв от их общего количества
- Количество слогов

Также можно получить статистику для конкретного слова:
- Сколько раз слово встречается в папке или файле
- Количество гласных и согласных
- Количество слогов в слове

### Установка и запуск
Для корректной работы приложения необходимо установить библиотеку Flask и python-docx:
`pip install flask`
`pip install python-docx`

Для запуска необходимо ввести в командной строке `python api.py` и открыть в браузере адрес `localhost:5000/statsapi`, далее следовать инструкциям на странице.

#### Реализация проекта
Проект реализован с помощью языка Python и библиотеки Flask. Для вёрстки страниц были использованы CSS и HTML.

#### Содержание репозитория
- Функции, используемые в приложении, описаны в файле `defs.py`
- Тесты на основные API-запросы запускаются с помощью `python test.py`
- Файлы для теста находятся в папке *testfiles*
- HTML-файлы находятся в папке *templates*
- CSS-файлы находятся в папке *static*