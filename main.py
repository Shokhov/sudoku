from tkinter import Tk, Button, Entry, LabelFrame, Label, CENTER, END, Text, WORD, Toplevel
import Sudoku_AI                    # подгружаем функции ИИ 
from Vertex import Vertex           # подгружаем класс Вершин


class App:
    """
    Класс: содержит графическую оболочку приложения Судоку:
    """

    def __init__(self, root, N, P):
        """
        Принимает: root, Размерность поля, размерность внутрених полей
        Метод: Инициализирует изначальных данных
        , инициализирует поле представленное ввиде кортежа вершин
        , создает графическую оболочку
        """
        # Основные данные
        self.root = root
        self.N = N
        self.P = P

        # Работа с вершинами
        # представляем поле судоку в виде кортежа вершин 
        self.Pole = tuple( Vertex(i%N,i//N,P,self) for i in range(N**2) )
        # задаем возможные значения значений вершин
        # перебираем все вершины, связываем вершины друг с другом
        for i in range(N*N):
            self.Pole[i].set_dimension(N)    # разрядность матрицы
            for j in range(i+1,N*N):
                if (i != j) and ((i%N == j%N) or (i//N == j//N) or ((i%N//P == j%N//P) and (i//N//P == j//N//P))):
                    self.Pole[i].set_heirs((self.Pole[j],1))
                    self.Pole[j].set_heirs((self.Pole[i],1))

        self.creation_a_graphical_shell(root, N,P)

    def creation_a_graphical_shell(self, root, N,P):
        """
        Принимает: размерность поля, размерность подматрицы
        Метод: Инициализирует виджеты
        , размещает виджеты на форме
        """
        # Размещение поля на форму
        frame_pole = LabelFrame(root, text = "Поле судоку")
        frame_pole.grid(row=1, column=0, rowspan=N, columnspan=N)
        self.widget_Pole = tuple( Button(frame_pole,text="",width=1,justify=CENTER,bd=1, command=lambda v = vertex: self.Button_click_pole(v), bg="#{0}{0}{0}{0}{0}{0}".format("E" if vertex.y//P%2 and not vertex.x//P%2 or vertex.x//P%2 and not vertex.y//P%2 else "C")) for vertex in self.Pole )
        for count,widget_vertex in enumerate(self.widget_Pole):
            widget_vertex.grid(row=count//N, column=count%N)        
        
        # Размещение кнопок с ИИ
        frame_AI = LabelFrame(root, text = "AI - помошники") 
        frame_AI.grid(row=1, column=N, rowspan=4)
        Button(frame_AI,text="AI - medium", width=12,command=lambda:Sudoku_AI.AI_medium(self.Pole)).grid(row=0, column=0)
        Button(frame_AI,text="AI - hard", width=12,command=lambda:Sudoku_AI.AI_hard(self.N,self.P, self.Pole)).grid(row=1, column=0)
        Button(frame_AI,text="AI - very_hard", width=12,command=lambda:Sudoku_AI.AI_very_hard(self.N,self.Pole)).grid(row=2, column=0)
        
        # Размещение матрицы возможных вариантов ячейки
        self.frame_possible_values = LabelFrame(root, text="Ячейка №-1")
        self.frame_possible_values.grid(row = N-P+1, column = N, rowspan=P, columnspan=P)
        self.widget_possible_values = tuple(Button(self.frame_possible_values,text="",width=1,justify=CENTER,bd=1, command = lambda count=count:self.Button_click_possible_value(count)) for count in range(P*P))
        # размещаем на фрэйме кнопки
        for count,button in enumerate(self.widget_possible_values):
            button.grid(row = count//P, column=count%P)

        # размещаем виджет ошибок
        self.widget_Error = Label(root,text="Ошибок нет",fg="#55CC55")
        self.widget_Error.grid(row=0, column=0, columnspan=self.N+self.P)
        
        

    #### Эвенты ##################################################################################
    def Button_click_pole(self,vertex):
        """
        Принимает: вершину
        Метод: выводит возможные значения вершины
        """
        # У ячеек получивших значение нет вероятных значений
        if vertex.get_value(): return None
        
        num = vertex.y*self.N+vertex.x                            # номер текщей ячейки
        num_prev = int((self.frame_possible_values["text"])[8:])  # поиск номера прошлой ячейки
        temp_list = ()
        # Запись новой ячейки
        if num == num_prev:
            self.frame_possible_values["text"] = "Ячейка №-1"
            # Меняем цвет текущей кнопки
            self.widget_Pole[num]["bg"] = "#{0}{0}{0}{0}{0}{0}".format("E" if (num_prev//self.N)//self.P%2 and not (num_prev%self.N)//self.P%2 or (num_prev%self.N)//self.P%2 and not (num_prev//self.N)//self.P%2 else "C")
        else:
            self.frame_possible_values["text"] = "Ячейка №{}".format(num)
            
            # меняем цвет предыдущей и текущей кнопки            
            if num_prev != -1: # если это первое нажатие
                self.widget_Pole[num_prev]["bg"] = "#{0}{0}{0}{0}{0}{0}".format("E" if (num_prev//self.N)//self.P%2 and not (num_prev%self.N)//self.P%2 or (num_prev%self.N)//self.P%2 and not (num_prev//self.N)//self.P%2 else "C")
            self.widget_Pole[num]["bg"] = "#55CC55"

            # список возможных вариантов
            temp_list = tuple(vertex.get_possible_values())
        
        for count in range(1,self.N+1):
            self.widget_possible_values[count-1]["text"] = str(count) if count in temp_list else ""

    
    def Button_click_possible_value(self,count):
        """
        Принимает: Координаты в матрице возможных значений
        Метод: записывает выбранное значение в вершину и выводит его на поле
        """
        value = self.widget_possible_values[count]["text"]
        if value:
            num = int((self.frame_possible_values["text"])[8:]) # поиск номера текущей ячейки
            self.Pole[num].set_value(int(value))                # записываем значение в вершину
            self.widget_Pole[num]["text"] = value               # выводим значение на поле
            
            # обнуляем матрицу возможных значений
            for widget in self.widget_possible_values:
                widget["text"] = ""



# Точка входа
if __name__ == "__main__":
    # Графическое приожение
    root = Tk()
    #root.title = "Sudoku"
    sudoku = App(root, 9, 3) # передаем (Экземпляр класса Tk, Разрядность поля, размер внутрених полей)
    root.mainloop()