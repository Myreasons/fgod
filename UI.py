import tkinter as tk
from tkinter import ttk
import fgod as fg
import SARIMA
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import xlsxwriter
import os



plt.style.use('fivethirtyeight')
mpl.rcParams['lines.linewidth'] = 0.5

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self._buisnessLogicHandlers = [
            self.cleaner,
            self.cleaner_aht,
            self.get_ind,
            self.save_n_exit
        ]
        self._currentHandler = 0
        self.init_main()

    clean_method = ''
    step = ''
    df11 = pd.DataFrame
    df_vol_clear = pd.DataFrame
    df_aht_clear = pd.DataFrame
    df_vol_clear_aht = pd.DataFrame
    df_aht_clear_aht = pd.DataFrame
    week_indexes = pd.DataFrame
    day_indexes = pd.DataFrame
    day_indexes_aht = pd.DataFrame
    week_indexes_aht = pd.DataFrame
    Forecast_Volume = pd.DataFrame
    Forecast_AHT = pd.DataFrame
    Forecast = pd.DataFrame
    end_path = ''


    def get_ind(self):
        plt.style.use('fivethirtyeight')
        mpl.rcParams['lines.linewidth'] = 0.5

        Main.day_indexes = SARIMA.dw_indexes(y=Main.df_vol_clear, measure='Clear VOL_ACT')
        Main.day_indexes_aht = SARIMA.dw_indexes(y=Main.df_aht_clear, measure='Clear AHT_ACT')
        Main.week_indexes = SARIMA.wm_indexes(y=Main.df_vol_clear, measure='Clear VOL_ACT')
        Main.week_indexes_aht = SARIMA.dw_indexes(y=Main.df_aht_clear, measure='Clear AHT_ACT')

        Main.df_for_sarima = Main.df_vol_clear

        Main.df_for_sarima['Clear AHT_ACT'] = Main.df_aht_clear['Clear AHT_ACT']
        Main.df_for_sarima= Main.df_for_sarima.loc[:, Main.df_for_sarima.columns.isin(['Clear VOL_ACT', 'Clear AHT_ACT'])]



        Main.Forecast_Volume = SARIMA.forecast_gad('Clear VOL_ACT',Main.day_indexes,Main.week_indexes,
                                                  Main.df_for_sarima)

        Main.Forecast_AHT = SARIMA.forecast_gad('Clear AHT_ACT', Main.day_indexes_aht, Main.week_indexes_aht,
                                                   Main.df_for_sarima)

        Main.Forecast = Main.Forecast_Volume
        Main.Forecast['AHT']=Main.Forecast_AHT['Volume']

        print(Main.Forecast_Volume)
        self.clear_monitor()

        figure1 = plt.Figure(figsize=(12, 5), dpi=100)
        ax1 = figure1.add_subplot()

        newax = figure1.add_axes(ax1.get_position())
        newax.patch.set_visible(False)
        newax.yaxis.set_label_position('right')
        newax.yaxis.set_ticks_position('right')

        # newax.legend(loc='upper left', handle ='Aht')

        Main.monitor = FigureCanvasTkAgg(figure1, root)
        Main.monitor.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

        Main.Forecast['Volume'].plot(legend=True, ax=ax1)
        Main.Forecast['AHT'].plot(legend=False, ax=newax, color='red')

        ax1.set_title('Прогноз')

    monitor = FigureCanvasTkAgg

    def save_n_exit(self):
        writer = pd.ExcelWriter('forecast.xlsx', engine='xlsxwriter')
        Main.Forecast.to_excel(writer, 'Forecast')
        os.chdir(Main.end_path)
        writer.save()
        self.clear_monitor()


    def clear_monitor(self):

        Main.monitor.get_tk_widget().pack_forget()
        Main.monitor.get_tk_widget().destroy()
        #Main.monitor1.get_tk_widget().pack_forget()

        try:
            Main.monitor.get_tk_widget().pack_forget()
        except AttributeError:
            pass

    def cleaner(self):
        self.clear_monitor()
        #ax1.clear()

        rez = self.clean_method(self.df11, 'VOL_ACT')
        #rez = rez.drop(['AHT_ACT', 'Filter_Anomaly'], axis = 1)
        rez = rez.loc[:,rez.columns.isin(['VOL_ACT','Clear VOL_ACT','Filter_Anomaly'])]




        #rez = fg.isolation_forest_anomaly_detection(self.df11, 'VOL_ACT')
        Main.df_vol_clear = rez



        figure1 = plt.Figure(figsize=(12, 5), dpi=100)
        ax1 = figure1.add_subplot()

        rez.plot(legend=True, ax=ax1)
        ax1.set_title('Очистка Volume')


        Main.monitor = FigureCanvasTkAgg(figure1, root)
        Main.monitor.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)




        Main.step = self.cleaner_aht
        ax1.clear

    def cleaner_aht(self):

        self.clear_monitor()
        rez2 = self.clean_method(self.df11, 'AHT_ACT')
        #rez2 = rez2.drop(['VOL_ACT','Filter_Anomaly','Clear VOL_ACT'], axis = 1)
        #print(rez2)
        rez2 = rez2.loc[:, rez2.columns.isin(['AHT_ACT', 'Clear AHT_ACT','Filter_Anomaly'])]





        #rez = fg.isolation_forest_anomaly_detection(self.df11, 'VOL_ACT')
        Main.df_aht_clear = rez2

        figure1 = plt.Figure(figsize=(12, 5), dpi=100)
        ax1 = figure1.add_subplot()


        Main.monitor = FigureCanvasTkAgg(figure1, root)
        Main.monitor.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        rez2.plot(legend=True, ax=ax1)
        ax1.set_title('Очистка AHT')
        ax1.clear




    def init_main(self):

        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)




        btn_open_dialog = tk.Button(toolbar, text='Настройки', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP)
        btn_open_dialog.pack(side=tk.LEFT)

        '''
        cleanb = tk.Button(toolbar, text='Очистка звонков', command=self.cleaner, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP)
        cleanb.pack(side=tk.LEFT)

        cleanba = tk.Button(toolbar, text='Очистка AHT', command=self.cleaner_aht, bg='#d7d8e0', bd=0,
                          compound=tk.TOP)
        cleanba.pack(side=tk.LEFT)

        cleanall = tk.Button(toolbar, text='Очистка all', command=self.clear_monitor, bg='#d7d8e0', bd=0,
                            compound=tk.TOP)
        cleanall.pack(side=tk.LEFT)

        cleanall = tk.Button(toolbar, text='NEW OPT', command=self.get_ind, bg='#d7d8e0', bd=0,
                             compound=tk.TOP)



        cleanall.pack(side=tk.LEFT)'''

        tk.Button(toolbar, text='NEXT', command=self.ivoke_handler, bg='#d7d8e0', bd=0,
          compound=tk.TOP).pack(side=tk.LEFT)


    def open_dialog(self):
        Child()

    def ivoke_handler(self):
        if self._currentHandler < len(self._buisnessLogicHandlers):
            self._buisnessLogicHandlers[self._currentHandler]()
            self._currentHandler = self._currentHandler + 1


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()

    def start(self,event):
        #Main.clear_monitor(self)

        if self.combobox.get() == "Изоляция Леса":

            Main.clean_method = fg.isolation_forest_anomaly_detection
        elif self.combobox.get() == "Фильтр нижних частот":
            Main.clean_method = fg.low_pass_filter_anomaly_detection

        else:
            Main.clean_method = ''
        if self.entry_path != '':
            Main.starter_path = self.entry_path
        else:
            Main.starter_path = r'C:\Users\aleksandr_balov\Desktop\fgod\venv\datas.xlsx'
        self.value = fg.starter(self.entry_path.get())

        Main.df11 = fg.starter(self.entry_path.get())
        Main.step = Main.cleaner
        Main.end_path = self.exit_path.get()

        #Main.clean_method = fg.isolation_forest_anomaly_detection



        figure1 = plt.Figure(figsize=(12, 5), dpi=100)
        ax1 = figure1.add_subplot()


        newax = figure1.add_axes(ax1.get_position())
        newax.patch.set_visible(False)
        newax.yaxis.set_label_position('right')
        newax.yaxis.set_ticks_position('right')


        #newax.legend(loc='upper left', handle ='Aht')


        Main.monitor = FigureCanvasTkAgg(figure1, root)
        Main.monitor.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

        self.value['VOL_ACT'].plot(legend=True, ax=ax1)
        self.value['AHT_ACT'].plot(legend=False, ax=newax, color='red')


        ax1.set_title('Исходные данные')

        print(Main.step)







    def init_child(self):
        self.title('Настройки')
        self.geometry('400x220+400+300')
        self.resizable(False, False)
        self.value = pd.DataFrame

        label_description = tk.Label(self, text='Путь к файлу:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Метод очистки')
        label_select.place(x=50, y=80)
        label_exp = tk.Label(self, text='Экспортировать в')
        label_exp.place(x=50, y=110)

        self.exit_path = ttk.Entry(self)
        self.exit_path.place(x=200, y=50)


        self.entry_path = ttk.Entry(self)
        self.entry_path.place(x=200, y=110)

        self.entry_path.insert(0, r'C:\Users\aleksandr_balov\Desktop\fgod\venv\datas.xlsx')
        self.exit_path.insert(0,r'C:\Users\aleksandr_balov\Desktop')


        self.combobox = ttk.Combobox(self, values=[u"Изоляция Леса", u"Фильтр нижних частот"])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='Загрузить')
        btn_ok.place(x=220, y=170)


        btn_ok.bind('<Button-1>',func = self.start)


        self.grab_set()
        self.focus_set()





if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("AFM")
    root.geometry("1200x600+300+200")
    root.resizable(True, True)
    root.mainloop()


