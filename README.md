<h2>Справочник по c++ на основе LLM с использованием технологии RAG</h2>

<div style="font-size: 15px; font-family: sans-serif">

<p> Данное приложение представляет собой чат для общения с моделью по тематике c++. </p>

<p> Запуск осуществляется через docker. </p>

<p> В файле <ins><i>backend/backend/config/config.yml</i></ins> содержатся необходимые настройки. Там нужно указать имя модели и api-ключ, можно задать дополнительные параметры. </p>

<p> В файле <ins> <i>backend/backend/template/template.txt</i></span></ins> находится шаблон запроса, также подлежащий изменению, но с сохранением параметров в фигурных скобках.</p>

Инструкция для сборки:

```bash
cd build
docker-compose up -d
```

Для более быстрого запуска:

```bash
docker-compose up -d
```

Приложение будет доступно на 3000 локальном порте.

Есть также файл <ins><i>backend/backend/scripts/test.py</i></ins> с несколькими тестами, использующий langsmith. Для его запуска требуется указать в нём api-ключ для langsmith.

<i> После изменения конфигурациии нужно перезапустить приложение: </i>

```bash
docker-compose restart
```
<h3> ${\color{red} Важно:}$ </h3>
<p> После запуска приложения внутри server-контейнера необходимо задать правильные настройки для модели в файле <ins><i>/home/backend/config/config.yml</i></span></ins> и сделать restart.</p>
</div>

____
<div>
<h3> Этапы создания </h3>

<ul>
  <li> Сбор данных с cppreference </li>
  <li> Настройка взаимодействия с моделью через api </li>
  <li> Подключение базы данных и извлечение документов </li>
  <li> Добавление web-интерфейса </li>
  <li> Соединение frontend и backend </li>
  <li> Простое тестирование </li>
</ul>
</div>


<div>
<h3> Пример результатов </h3>

<h4> Работа с mistral </h4>
<img width="1920" height="1080" alt="2025-11-15_11-45-13" src="https://github.com/user-attachments/assets/90b0417e-99d4-4c2b-b5f2-48066dfd157a" />

<h4> Работа с openai </h4>
<img width="1920" height="1080" alt="2025-11-14_17-34-14" src="https://github.com/user-attachments/assets/97f133fb-72f0-49db-88f6-a88abd3aead0" />

<img width="1920" height="1080" alt="2025-11-14_17-08-57" src="https://github.com/user-attachments/assets/83c72501-a08a-44a5-9db5-cb5412900f2b" />

<h4> Тестирование </h4>
<img width="1808" height="780" alt="2025-11-14_17-52-13" src="https://github.com/user-attachments/assets/e314167b-3766-48e1-af36-be3ea44f5289" />

</div>

