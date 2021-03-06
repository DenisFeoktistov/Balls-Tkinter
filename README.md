## Симулятор движения шаров на Python/tkinter

Программа симулирует движение шаров трёх цветов, различающихся по плотности. Масса шаров одного цвета пропорциональна их
площади. Реализованы идеально упругие столкновения шаров со стенами и друг с другом. Также стрелочками визуализированы
векторы скоростей шаров.

Пользователю доступны следующие настройки (все параметры от 0 до 100):
- size: максимальный размер шаров
- velocity: максимлаьная начальная скорость шаров
- count: количество шаров
- vector scale: масштаб стрелочек относительно модуля скорости
- red/green/blue density: плотность красных/зелёных/синих шаров соответственно

По нажатию кнопки `Save & regenerate` шары генерируются на поле в соответствии с настройками, а сами настройки
сохраняются в файл `settings.json`.

![picture](https://i.imgur.com/zJ0Bjoo.png)