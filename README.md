0) Установить зависимости:

   - Перейти в директорию где лежит requirements.txt 

   - pip install -r requirements.txt


1)Server (Запустить тестовый сервер в папке src)
скрипт -> server_socketio_for_test 
 -  python server_socketio_for_test.py или через pycharm (run)

socketio commands (just type in console):
> start_selector - запускает поиск селектора
> ,далее должно появиться окошко выбора uia or win32 

2) Client (Запустить клиента в папке src)

- socket_io_client.py --e "http://localhost:8008/"

Взаимодействие: 
1) Они должны законнектиться 
2) От сервера нужно отправить команду: start_selector 
3)Выбрать backend в сплывающем окне
4) Навести на нужный элемент 
5) Зажать ctrl + левая кнопка мыши 

6)Далее он отправляет его на сервер (ТУТ нужно изменить поведение по послед тех требованию)
   main.py - храниться парсинг селектора и запуск окна qt 
   UIDesktop - вспомогательный модуль  (специфик для windows10)
   
        