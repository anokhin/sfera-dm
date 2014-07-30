Техносфера. Data Mining 
========

Слайды и материалы курса Data Mining для проекта Техносфера (семестр 2)

## Программа курса

### Модуль 1. Введение в Data Mining

#### Занятие 1. Задачи Data Mining (Николай Анохин)

**Теоретическа часть.** Обзор задач Data Mining. Стандартизация подхода к решению задач Data Mining. Процесс CRISP-DM. Виды данных. Кластеризация, классификация, регрессия. Понятие модели и алгоритма обучения.

**Практическая часть.** Библиотека numpy. Exploratory data analysis.

#### Занятие 2. Задача кластеризации и EM-алгоритм (Николай Анохин)

**Теоретическая часть.** Постановка задачи кластеризации. Функции расстояния. Критерии качества кластеризации. EM-алгоритм. K-means и модификации.

**Практическая часть.** Исследование свойства локальности алгоритма k-means. 

#### Занятие 3. Различные алгоритмы кластеризации (Николай Анохин)

**Теоретическая часть.** Иерархическая кластеризация. Agglomerative и Divisive алгоритмы. Различные виды расстояний между кластерами. Stepwise-optimal алгоритм. Случай неэвклидовых пространств. Критерии выбора количества кластеров: rand, silhouette. DBSCAN.

**Практическая часть.** Исследование влияния функции расстояния между кластерами на результат кластеризации.

#### Занятие 4. Задача классификации (Николай Анохин)

**Теоретическая часть.** Постановка задач классификации и регрессии. Теория принятия решений. Виды моделей. Примеры функций потерь. Переобучение. Метрики качества классификации. MDL. Решающие деревья. Алгоритм CART. 

**Практическая часть.** Использование дерева решений для предсказания категории дохода пользователя.

#### Занятие 5. Naive Bayes (Николай Анохин) 

**Теоретическая часть.** Условная вероятность и теорема Байеса. Нормальное распределение. Naive Bayes: multinomial, binomial, gaussian. Сглаживание. Генеративная модель NB и байесовский вывод. Графические модели.

**Практическая часть.** Использование NB для определения языка текста.

#### Занятие 6. Линейные модели (Николай Анохин)

**Теоретическая часть.** Обобщенные линейные модели. Постановка задачи оптимизации. Примеры критериев. Градиентный спуск. Регуляризация. Метод Maximum Likelihood. Логистическая регрессия.

**Практическая часть.**

#### Занятие 7. Метод опорных векторов (Николай Анохин)

**Теоретическая часть.** Разделяющая поверхность с максимальным зазором. Формулировка задачи оптимизации для случаев линейно-разделимых и линейно-неразделимых классов. Сопряженная задача. Опорные векторы. KKT-условия. SVM для задач классификации и регрессии. Kernel trick. Теорема Мерсера. Примеры функций ядра.

**Практическая часть.** Выбор подходящей функции ядра для различных наборов данных. Grid search.
### Модуль 2. Дополнительные главы Data Mining

#### Занятие 1. Снижение размерности пространства  (Владимир Гулин)

**Теоретическая часть.** Проблема проклятия размерности. Отбор и выделение признаков. Методы выделения признаков (feature extraction). Метод главных компонент (PCA). Метод независимых компонент (ICA). Методы основанные на автоэнкодерах. Методы отбора признаков. Метод mRMR. Методы основанные на взаимной корреляции признаков. Методы основанные на деревьях решений.

**Практическая часть.** Визуализация многомерных данных. Анализ признаков на информативность.

#### Занятие 2. Алгоритмические композиции 1 (Владимир Гулин)

**Теоретическая часть.** Комбинации классификаторов. Модельные деревья решений. Ансамбли слабых моделей. Смесь экспертов. Bagging. RSM. Алгоритм RandomForest.

**Практическая часть.** Сравнительный анализ алгоритмов с алгоритмом RandomForest.
#### Занятие 3. Алгоритмические композиции 2 (Владимир Гулин)

**Теоретическая часть.** Буcтинг. Алгорим AdaBoost. Градиентный бустинг (Алгоритм TreeNet). Алгоритм AnyBoost. Мета-алгоритмы над алгоритмическими композициями. Алгоритм Aditive Grooves. Алгоритм BagBoo.

**Практическая часть.** Сравнительный анализ алгоритмов с алгоритмом TreeNet.

#### Занятие 4. Нейросети, обучение с учителем (Павел Нестеров)

**Теоретическая часть.** Биологический нейрон и нейронные сети. Искусственный нейрон Маккалока-Питтса и искусственная нейронная сеть. Персептрон Розенблатта и Румельхарта. Алгоритм обратного распространения ошибки. Момент обучения, регуляризация в нейросети, локальная скорость обучения, softmax слой. Различные режимы обучения.

**Практическая часть.** Распознавание печатных букв на двуслойном персептроне.

#### Занятие 5. Нейросети, обучение без учителя (Павел Нестеров)

**Теоретическая часть.** Нейросетейвой автоэнкодер. Стохастические и рекурентные нейронные сети. Машина Больцмана и ограниченная машина Больцмана. Распределение Гиббса. Алгоритм contrastive divergence для обучения РБМ. Сэмплирование данных из РБМ. Бинарная РБМ и гауссово-бинарная РБМ. Влияние регуляризации, нелинейное сжатие размерности, извлечение признаков. Semantic hashing.

**Практическая часть.** Извлечение признаков, используя РБМ; генерация расширенного обучающего множества. Semantic hashing.

#### Занятие 6. Нейросети, глубокие сети (Павел Нестеров)

**Теоретическая часть.** Трудности обучения многослойного персептрона. Предобучение используя РБМ. Глубокий автоэнкодер, глубокая многослойная нейросеть. Deep belief network и deep Boltzmann machine. Устройство человеческого глаза и зрительной коры головного мозга. Сверточные сети.

**Практическая часть.** Распознавание печатных и рукописных символов на глубокой сети.

### Литература

[bishop] Pattern Recognition and Machine Learning // Cristopher M. Bishop (http://research.microsoft.com/en-us/um/people/cmbishop/prml/)

[duda] Pattern Classification // Richard O. Duda, Peter E. Hart, David G. Stork (http://eu.wiley.com/WileyCDA/WileyTitle/productCd-0471056693.html)

[rajaraman] Mining of Massive Datasets // Anand Rajaraman, Jeffrey Ullman (http://infolab.stanford.edu/~ullman/mmds/book.pdf)

[hastie] The Elements of Statistical Learning: Data Mining, Inference, and Prediction // Trevor Hastie, Robert Tibshirani, Jerome Friedman  (http://web.stanford.edu/~hastie/local.ftp/Springer/OLD/ESLII_print4.pdf)

[haykin] Neural Networks and Learning Machines // Simon O.Haykin (http://www.ib.cnea.gov.ar/~redneu/2013/BOOKS/Haykin.pdf)

[Peng] Feature selection based on mutual information: criteria of max-dependency, max-relevance, and min-redundancy // Hanchuan Peng, Fuhui Long, Chris Ding (http://penglab.janelia.org/papersall/docpdf/2005_TPAMI_FeaSel.pdf)

[hinton_pgrbm] A Practical Guide to Training Restricted Boltzmann Machines // Geoffrey Hinton (http://www.cs.toronto.edu/~hinton/absps/guideTR.pdf)

[hinton_red] Reducing the Dimensionality of Data with Neural Networks // Geoffrey Hinton (http://www.cs.toronto.edu/~hinton/science.pdf)

[lecun_cn] Gradient-based learning applied to document recognition // Yann LeCun (http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)
