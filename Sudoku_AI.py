#### Методы ИИ ###################################
def AI_medium(Pole):
        """
        Принимает: Поле значений (Весь граф)
        Функция: Вычисляет (по осям) один набор возможных значений
        """
        number_of_values_from = 1
        while number_of_values_from:
            number_of_values_from = 0 # Обнуляем переменную (resetting the variable)
            for vertex in Pole:
                if vertex.get_value(): continue # у этой вершины уже есть значение
                
                # перебираем все смежные вершины
                for axis in vertex.search_for_adjacent_vertices_by_axes():
                    # Создаем матрицу смежности (Вершины,Значения)
                    adjacency_matrix_by_axis = {}
                    for count,vertex_count in enumerate(axis):
                        for num in vertex_count.get_possible_values():
                            if adjacency_matrix_by_axis.get(num,0):
                                adjacency_matrix_by_axis[num].append(axis[count])
                            else:
                                adjacency_matrix_by_axis[num] = [axis[count]]
                    
                    # Поиск вершин с единственно повторяющимися значениями
                    axis_by_adjacency_matrix = {}
                    for value, list_vertex in adjacency_matrix_by_axis.items():
                        if len(list_vertex) == list(adjacency_matrix_by_axis.values()).count(list_vertex):
                            if axis_by_adjacency_matrix.get(tuple(list_vertex),0):
                                axis_by_adjacency_matrix[tuple(list_vertex)].append(value)
                            else:
                                axis_by_adjacency_matrix[tuple(list_vertex)] = [value]

                    # Записываем возможные варианты
                    for list_vertex, values in axis_by_adjacency_matrix.items():
                        for vertex_count in list_vertex:
                            vertex_count.set_possible_values(values)
                            if len(values) == 1:
                                number_of_values_from += 1
            #print("Количество сделанных действий: ",number_of_values_from)


def AI_hard(N,P, Pole):
    """
    Принимает: Размер поля,Размер подматрицы, Поле значений (Весь граф)
    Функция: Вычисляет линию (в подматрице P) единственных возможных значений, для сокращения этих значений на линии 
    """
    def vertex_sorting_by_axis(list_possible_value):
        """
        Принимает: Подматицу поля с пустыми ячейками (вершинами)
        Функция: сортирует полученные вершины по линиям (линия х, линия у)
        """
        # направление линии поиска (по какой оси ведется поиск)
        lines_x = [ [ list_possible_value[0] ] ]        # получаем первую вершину
        lines_y = [ [ list_possible_value.pop(0) ] ]    # вырезаем первервую вершину

        # перебираем оставшиеся вершины
        for vertex in list_possible_value:
            # Вершины идут слева-направа, сверху-вниз (цикл for не обязателен)
            for line in lines_x:
                if vertex.y == line[-1].y:
                    line.append(vertex)
                    break
            else:
                lines_x.append([vertex])

            # Вершины идут по порядку столбцов потом смена строчки (цикл for обязателен)
            for line in lines_y:
                if vertex.x == line[-1].x:
                    line.append(vertex)
                    break
            else: 
                lines_y.append([vertex])
        return (lines_x, lines_y)

    def axis_checking(P, matrix,matrix_lines, yx, kf_1,kf_2):
        """
        """
        # перебираем все подматрицы построчно
        for y in range(P):
            # перебираем все повторения
            for count in range(P):
                if not matrix[y][count] or matrix[y][count] == P: continue    # нулевое значение или все значения - нечего сокращать

                # получаем последовательность повторений
                list_lines = [matrix_lines[y][count]]
                for x in range(count+1,P):
                    if matrix[y][count] == matrix[y][x]:
                        list_lines.append(matrix_lines[y][x])
                        matrix[y][x] = 0  # Обнуляем значение чтобы больше не было повторений

                # Поиск соотвествий по Осям
                for line_i in range(len(list_lines)):
                    list_of_matches = [list_lines[line_i]] # список соотвесвий

                    for line_j in range(line_i+1,len(list_lines)):
                        for line_y in range(matrix[y][count]):
                            # выходим из цикла если ,линии расположены на разных уровнях, не совподают
                            list_lines_yx_i = list_lines[line_i][line_y][0].y if yx else list_lines[line_i][line_y][0].x
                            list_lines_yx_j = list_lines[line_j][line_y][0].y if yx else list_lines[line_j][line_y][0].x
                            if list_lines_yx_i != list_lines_yx_j: break
                        else:
                            list_of_matches.append(list_lines[line_j])


                    # проверяем совподение соотвествий
                    if len(list_of_matches) == matrix[y][count]:    
                        # на каких уровнях распологаются соответствия
                        temp_p = [ (ur[0][0].x if yx else ur[0][0].y)//P for ur in list_of_matches ]
                        temp_ur = [ (ur[0].y if yx else ur[0].x) for ur in list_of_matches[0] ]

                        for p in range(P):
                            if p in temp_p: continue

                            for axis in range(P):
                                for ur in temp_ur:
                                    if Pole[p*P*kf_1+axis*kf_1+ur*kf_2].get_value(): continue
                                
                                    Pole[p*P*kf_1+axis*kf_1+ur*kf_2].remove_possible_values(None,num,False)

                matrix[y][count] = 0  # Обнуляем значение чтобы больше не было повторений




    # Перебираем все возможные значения
    for num in range(1,N+1):
        matrix_x = tuple( [] for count in range(P) )    # Матрица количество линий в подматрицах по X 
        matrix_y = tuple( [] for count in range(P) )    # Матрица количество линий в подматрицах по Y
        matrix_lines_x = tuple( [] for count in range(P) )    # Список линий по Х
        matrix_lines_y = tuple( [] for count in range(P) )    # Список линий по Y

        # Поиск всех вершин (без значения) в подматрицах
        for Xp,Yp in ((count%P,count//P) for count in range(N)):
            # список вершин имеющих возможное значение num
            list_possible_value = [ vertex for vertex,weight in Pole[Yp*N*P + Xp*P].get_heirs() if not vertex.get_value() and vertex._possible_values.count(num) and (Xp == vertex.x//P and Yp == vertex.y//P) ]
            if not Pole[Yp*N*P + Xp*P].get_value() and Pole[Yp*N*P + Xp*P]._possible_values.count(num):
                list_possible_value.insert(0,Pole[Yp*N*P + Xp*P])   # добавляем недостающую деталь
            
            # поиск линии единственных вероятных значений
            if len(list_possible_value) >= 2:
                lines_x, lines_y = vertex_sorting_by_axis(list_possible_value)  # сортируем вершины по линиям

                # Собираем данные
                matrix_x[Yp].append( len(lines_x) )
                matrix_y[Xp].append( len(lines_y) )
                matrix_lines_x[Yp].append( lines_x )
                matrix_lines_y[Xp].append( lines_y )
            else:
                matrix_x[Yp].append( 0 )
                matrix_y[Xp].append( 0 )
                matrix_lines_x[Yp].append( None )
                matrix_lines_y[Xp].append( None )
        
        # Проверка по оси Х
        axis_checking(P, matrix_x,matrix_lines_x, True, 1,N)
        # Проверка по оси Y
        axis_checking(P, matrix_y,matrix_lines_y, False, N,1)
        
        
def AI_very_hard(N,Pole):
    """
    Принимает:
    Функция: Решает судоку алгоритмом раскарски вершин графа (не жадный)
    """
    return # недоделан алгоритм раскраски графа
    def check(Pole,count,search_in_wight,temp_matrix):
        """
        """
        if Pole[count] in search_in_wight: # Такая вершина уже есть
            return True
        elif Pole[count].get_value():           # Добавляем уже закрашенные вершины
            search_in_wight.append(Pole[count])
            temp_matrix[Pole[count].y][Pole[count].x] = Pole[count].value
            return True
        return False

    # Начальные данные
    search_in_wight = []   # Список последовательности алгоритма поиска в ширину
                        # (содержит уже разукрашенные вершины)
    count = 0       # указатель на текущую вершину
    color = []
    ####
    temp_matrix = tuple([None for _ in range(N)] for y in range(N))
    ####

    while count < N*N-1:
        if check(Pole,count,search_in_wight,temp_matrix):
            count+=1
            continue

        # Поиск НЕ связных вершин
        not_adj_vertices = [Pole[count]]
        #possible_values_not_adj = [Pole[count].get_possible_values()]
        for vertex_count in range(count+1,N*N):
            if check(Pole,vertex_count,search_in_wight,temp_matrix): continue

            # Проверяем связность вершин
            for parent in not_adj_vertices:
                if Pole[vertex_count] in tuple(v for v,w in parent.get_heirs() ):
                    break
            else:
                not_adj_vertices.append(Pole[vertex_count])

        print([(v.x,v.y) for v in not_adj_vertices ])
        search_in_wight += not_adj_vertices
        count += 1

        

        
    for y in temp_matrix:
        print(y)
    print([(v.x,v.y) for v in search_in_wight])
    print(color)


