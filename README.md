# **Infinity Castle**

## **Концепция:**

   **Жанр:** 2D рогалик с видом сверху.  
   **Платформа:** ПК.   
   **Геймплей:** Персонаж появляется в замке, около главного входа. Далее следует прохождение бесконечно генерируемые уровней, при постоянном усилении врагов. Оно сопровождается улучшением персонажа и нахождением или покупкой за монеты нового оружия и магии, которые, как и манну, которую тратит персонаж при использовании магии, можно выбить из монстров. Каждый уровень имеет случайное количество разных комнат. Расположение комнат на уровне также генерируется самостоятельно. Переход с уровня на уровень осуществляется по лестнице, где может произойти случайное событие.   
   **Цель:** пройти как можно больше уровней. 

## **Дизайн:**

   **Стиль:** средневековье.   
   **Главный герой:** рыцарь.    
   **Враги:** 3 вида: ближники (скелеты, зомби, духи), дальники (скелеты-лучники, маги), призыватели под вопросом.   
   **Оружие:** разнообразие холодного оружия и видов магии.   
   **Характеристики:** здоровье, количество манны.   
   **Комнаты:** комната располагается на весь экран. Смена комнат происходит при открытии двери для перехода в другую комнату.   

## **Структура проекта**:

  1.1) Папка data хранит в себе всю визуальную и аудио часть проекта. В ней находятся:
  
    1) *Папка music_and_sounds* хранит в себе всю музыку и звуки игры
    2) *Папка pictures* хранит в себе все изображения для проекта. Сюда входят анимации, окружение, спрайты героя и врагов, оружия и кнопки
    3) *Папка shrifts* хранит в себе шрифты для красивого текста
    4) *База данных InfinityCastle_db* хранит в себе несколько таблиц для хранения разной информации:
      1.1) Таблица accounts содержит в себе информацию о всех зарегистрированных пользователях в формате: Id, игровое имя, пароль.
      1.2) Таблица achievenment содержит в себе информацию о полученных достижениях каждого пользователя в формате: id, достижение №1, достижение №2...
      1.3) Таблица leaderboard_level содержит в себе информацию о рекордах по количеству пройдённых этажей в формате: Id, этаж
    
  1.2) Папка src хранит в себе файлы с кодом:
  
    1) *InputBox.py* содержит в себе два класса: InputBox и One_Symbol_InputBox:
      1.1) Класс InputBox используется для ввода текста пользователем. У него есть методы для получения введённого текста и его полного удаления.
      1.2) Класс One_Symbol_InputBox наследуется от класса InputBox. Данный класс нужен для ограничения длины текста до 1 символа.
    2) *func.py* содержит в себе все полезные функции, используемые в других файлах:
      1.1) Функция load_image используется для загрузки изображения
      1.2) Функция terminate нужна для полной остановки приложения
      1.3) Функция show_image оторбражает изображения
      1.4) Функции map_generation, room_generation, count_rooms создают эскиз этажа из случайных блоков в виде списка
    3) *main.py* содержит в себе полное меню приложения:
      1.1) Класс Button - основной класс файла для создания кнопки и отображения кнопки по заданным параметрам
      1.2) Остальные функции файла отображают отдельные части меню
    4) *game.py* является самой игрой:
      1.1) Класс Player - ключевой класс игрока, нужен для обработки кнопок, отображения персонажа и его анимаций
      1.2) Класс Room управляет комнатами, нужен для правильной обработки перемещений между комнатами
      1.3) Функция Interface используется для отображения всего интерфейса (маны, здоровья оружия и т. д.)
      1.4) Функция load_settings используется для загрузки и обновления глобальных настроек управления
      1.5) функция update_mana_hp_coins используется для отображения динамичных параметров маны, здоровья и монет
      1.6) Функция start запускает саму игру
    5) *game_load.py* загрузка картинок в игре
    6) *account_info.txt* имя аккаунта, который запущен в данный момент

  Все функции и классы распределены между файлами специально для чистоты кода и недопущения циклического import. Соответственно и сама связь между файлами осуществляется при помощи import.
