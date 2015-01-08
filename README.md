Техносфера. Data Mining 
========

Слайды и материалы курса Data Mining для проекта Техносфера (семестр 3)

## Программа курса

### Модуль 1. Задачи кластеризации

#### Занятие 1. Задачи Data Mining

**Теоретическа часть.** Обзор задач Data Mining. Стандартизация подхода к решению задач Data Mining. Процесс CRISP-DM. Виды данных. Машинное обучение. Кластеризация, классификация, регрессия. Понятие модели и алгоритма обучения.

**Практическая часть.** Обзор данных задачи на kaggle. Краткий обзор зыка Python. Библиотека Pandas. Использование внешинх REST API.

**ДЗ 1.** Сбор данных для проекта

#### Занятие 2. Задача кластеризации и EM-алгоритм

**Теоретическая часть.** Постановка задачи кластеризации. Функции расстояния. Критерии качества кластеризации. EM-алгоритм и смесь гауссовских распределений. Алгоритм K-means и его модификации.

**Практическая часть.** Выделение признаков. Различные виды признаков. Преобразование признаков. Zipf's law.

**ДЗ 2.** Выделение нескольких данных заранее признаков из данных проекта

#### Занятие 3. Алгоритмы кластеризации

**Теоретическая часть.** Иерархическая кластеризация. Agglomerative и Divisive алгоритмы. Различные виды расстояний между кластерами. Stepwise-optimal hierarchical clustering. Случай неэвклидовых пространств. Критерии выбора количества кластеров: rand index, silhouette. Алгоритм DBSCAN.

**Практическая часть.** Похоже, что это должно быть сравнение различных алгоритмов кластеризации.

**ДЗ 3.** Реализация одного из алгоритмов кластеризации, применение на данных семестрового проекта и визуализация результатов.

#### Занятие 4. Визуализация результатов кластеризации

**Теоретическая часть.** (Предварительное содержание) Алгоритмы снижения размерности. Алгоритм T-SNE.

**Практическая часть.**

#### Занятие 5. Коллоквиум по методам кластеризации + сдача третьего ДЗ

#### Занятие 6. Задача классификации

**Теоретическая часть.** Постановка задач классификации и регрессии. Теория принятия решений. Виды моделей. Примеры функций потерь. Переобучение. Метрики качества классификации. MDL.

**Практическая часть.** Использование дерева решений для предсказания категории дохода пользователя.

#### Занятие 6. Решающие деревья

**Теоретическая часть.** Решающие деревья. Алгоритм CART.

**Практическая часть.**

#### Занятие 7. Naive Bayes

**Теоретическая часть.** Условная вероятность и теорема Байеса. Нормальное распределение. Naive Bayes: multinomial, binomial, gaussian. Сглаживание. Генеративная модель NB и байесовский вывод. Графические модели.

**Практическая часть.**

#### Занятие 6. Линейные модели

**Теоретическая часть.** Обобщенные линейные модели. Постановка задачи оптимизации. Примеры критериев. Градиентный спуск. Регуляризация. Метод Maximum Likelihood. Логистическая регрессия.

**Практическая часть.**

#### Занятие 8. Метод опорных векторов

**Теоретическая часть.** Разделяющая поверхность с максимальным зазором. Формулировка задачи оптимизации для случаев линейно-разделимых и линейно-неразделимых классов. Сопряженная задача. Опорные векторы. KKT-условия. SVM для задач классификации и регрессии. Kernel trick. Теорема Мерсера. Примеры функций ядра.

**Практическая часть.**

### Литература

[bishop] Pattern Recognition and Machine Learning // Cristopher M. Bishop (http://research.microsoft.com/en-us/um/people/cmbishop/prml/)

[duda] Pattern Classification // Richard O. Duda, Peter E. Hart, David G. Stork (http://eu.wiley.com/WileyCDA/WileyTitle/productCd-0471056693.html)

[rajaraman] Mining of Massive Datasets // Anand Rajaraman, Jeffrey Ullman (http://infolab.stanford.edu/~ullman/mmds/book.pdf)

[hastie] The Elements of Statistical Learning: Data Mining, Inference, and Prediction // Trevor Hastie, Robert Tibshirani, Jerome Friedman  (http://web.stanford.edu/~hastie/local.ftp/Springer/OLD/ESLII_print4.pdf)

[murphy] Machine Learning: a Probabilistic Perspective // Kevin Patrick Murphy (http://www.cs.ubc.ca/~murphyk/MLbook/)
