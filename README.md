# Примеры работы с e-Ink и RPI

"Пробы пера", а вернее, попытки найти применение 2.13" e-Ink дисплею для Raspberry PI Zero. Поскольку Python для меня язык новый, код может выглядеть уж очень "непричесанным", но он работает и выполняет те задачи,для которых писался.

## Содержимое репозитория
Итак, результатом моих экспериментов стали следующие три скрипта (в папке examples):
* pictest.py - отображение BMP-картинок (прототип бейджика или ценника на электронных чернилах)
* stats.py - вывод текущей даты/времени, системной информации, текущей погоды (с weatherstack.com)
* COVID.py - отображение текущей статистики по заболеваемости COVID'19 в Украине (с covid19api.com)

Выглядит все это, в принципе, очень даже неплохо!

## Источники
* Официальная вики https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT
* https://github.com/waveshare/e-Paper
* https://github.com/headHUB/waveshare-2.13-epaper-hat
