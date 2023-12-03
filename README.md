# TulaHackDays2023
## Инструкция по запуску

Фронтенд нашего сервиса доступен по ссылке:  
[app](http://84.201.128.245/)

Однако, есть возможность развернуть локально.

### Локальный запуск

  CWD = <корень проекта>
  py version = 3.11

  Устанавливаем зависимости для всего проекта
  ```
  pip install -r requirements.txt
  ```

  Сетапим мл-модель
  ```
  cd ml/model
  ./setup.sh
  ```
  Скачать файл https://disk.yandex.ru/d/zR-GaFxQWhKvPQ и поместить в `ml/model/classifier.pt`

  запускаем фронтенд
  ```
  cd ../..
  python3 -m flask --app stand/backend/app run --host 127.0.0.1 --port 5000
  ```

  запускаем бэкенд
  ```
  python3 -m streamlit run stand/streamlit_form/form.py
  ```

