class Vertex:
    """
    Класс: является вершиной графа
    , содержит значения: вида графа, координаты, значение вершины, родители и наследников вершины
    """
    _graph_orientation = False   # Вид графа: НЕ Ориентированный/Ориентированный (view graph: Not Orientation/Orientation)
    _number_of_vertices = None   # Количество вершин (number of vertices)
    _dimension = None            # Размерность матрицы смежности
    _dimention_P = None          # Размерность под матрицы
    _possible_values = []         # Список возможных вариантов
    
    Error = []                  # Список ошибок

    def __init__(self, x,y,P, app=None, value=None):
        """
        Принимает: координаты вершины, значение
        Метод: инициализирует основные значение
        , инициализирует переменные родителей и наследников
        """
        # Изначальные значения
        self.x = x          # координаты по x (x coordinates)
        self.y = y          # координаты по y (y coordinates)
        self.value = value  # значение вершины (vertex value) (вычисляется в на основе других вершин)
        self._dimention_P = P # размерность под матрицы

        # Даём возможность обращаться из вершине выводить своё значение на поле
        self.app = app
        
        # Связи графа
        self.parents = []   # Родители, от какой вершины идет стрелочка (parent vertices)
        self.heirs = []     # Наследники, до какой вершины идет стрелочка (heirs vertices)

    def set_parents(self, parent, clear=False):
        """
        Принимает: список родителей вершины, рубильник очищения переменной
        Метод: записывает список родителей [(v1,weight),(v2,weight)...,(wn,weight)]
        """
        if clear: self.parents.clear()  # Очищаем переменную (clear the variable)
        self.parents.append(parent)    # Записываем родителей (write parent)
    def get_parents(self): return self.parents

    def set_heirs(self, heir, clear=False):
        """
        Принимает: список наследников вершины, рубильник очищения переменной
        Метод: записывает списк наследников [(v1,weight),(v2,weight)...,(vn,weight)]
        """
        if clear: self.heirs.clear()    # Очищаем переменную (clear the variable)
        self.heirs.append(heir)         # Записываем наследника (write heir)
    def get_heirs(self): return self.heirs
    
    def set_dimension(self,value):
        """
        Получает: Разрядности матрицы (Количество вершин)
        Метод: записывает количество возможных значений
        """
        self._dimension = value
        # Записываем возможние значения
        self._possible_values = list(range(1,value+1))

    def set_value(self,value):
        """
        Получает: значение вершины
        , производится проверка повторения значений на осях
        , оповещает наследников о полученном значении
        """
        self.value = value

        # оповещаем наследников
        for vertex, weight in self.heirs:
            vertex.remove_possible_values(self,self.value)

        # поиск одинаковых значений на осях
        for vertex,xyp in self.parents:
            if vertex.get_value() == self.value:
                Vertex.Error.append("Vertex[{}][{}] = Vertex[{}][{}]({}) == {}: Repeat_values".format(self.x,self.y,vertex.x,vertex.y,xyp,self.value))
                with open("Error.txt","a") as fail:
                    fail.write("Vertex[{}][{}] = Vertex[{}][{}]({}) == {}: Repeat_values\n".format(self.x,self.y,vertex.x,vertex.y,xyp,self.value))
                self.app.widget_Error["fg"] = "#CC5555"
                self.app.widget_Error["text"] = "Repeat_values"
    def get_value(self): return self.value
    
    def set_possible_values(self,list_values):
        """
        Получает: Лист значений
        Метод: Записывает значения
        """
        self._possible_values = list_values.copy()
        
        if self.value: return # если значение есть то вычислять нечего
        # пытаемся вычислить значение
        self.value_calculation()
    def get_possible_values(self): return self._possible_values


    #### Методы обработки данных ############################################################################
    def value_calculation(self):
        """
        Метод: выбирает оставшийся вариант
        , проверяет на отсустви вариантов и записывает в начальный класс ошибки
        """
        if len(self._possible_values) == 1:
            self.set_value(self._possible_values.pop())
            # выводим результат на поле
            self.app.widget_Pole[self.y*self._dimension+self.x]["text"] = self.value
        elif len(self._possible_values) == 0:
            Vertex.Error.append("Vertex[{}][{}] = {}: Not possibl_values".format(self.x,self.y,self.value))
            with open("Error.txt","a") as fail:
                fail.write("Vertex[{}][{}] = {}: Not possibl_values\n".format(self.x,self.y,self.value))
            self.app.widget_Error["fg"] = "#CC5555"
            self.app.widget_Error["text"] = "Not possibl_values"
    def remove_possible_values(self,vertex,value,write_parents=True):
        """
        Активируется: при получении значения у соседних вершин
        Получает: соседнюю вершину и вес связи между ними
        Метод: удаляет возможное значение
        , перемещаем наследника в родители
        , пытаемся вычислить значение вершины
        """
        if self._dimension:  # вычисляем, если есть возможные значения
            if self._possible_values.count(value):
                self._possible_values.remove(value)
            # удаление наследника возможно сократит вычисление
            # , но появляется логический баг
            #  (не может определить ошибку повторение значений по осям)
            
            # перемещаем наследника в родители
            if write_parents:
                if   vertex.x == self.x:    # на горизонте
                    self.parents.append((vertex,1))
                elif vertex.y == self.y:    # на вертикали
                    self.parents.append((vertex,2))
                else:                       # в матричном блоке
                    self.parents.append((vertex,3))
                
            if self.value: return # выходим, если уже есть значение
            # Пытаемся вычислить значение
            self.value_calculation()
            

    def search_for_adjacent_vertices_by_axes(self):
        """
        Метод: проводит сортировку смежных вершин по их осям
        """
        axis_x = [self] # По x
        axis_y = [self] # По y
        axis_p = [self] # По матрице p

        for heir,weight in self.get_heirs():
            if heir.get_value(): continue   # у этой вершины нет возможных вариантов

            # сортировка по осям
            if heir.x == self.x:
                axis_y.append(heir)
            if heir.y == self.y:
                axis_x.append(heir)
            if heir.x//self._dimention_P == self.x//self._dimention_P and heir.y//self._dimention_P == self.y//self._dimention_P:
                axis_p.append(heir)

        return [axis_x,axis_y,axis_p]