from datetime import datetime
import sys
import pygame
import serial as conecta
from PyQt5 import uic, QtWidgets, QtCore
import requests

qtCreatorFile = "ProyectoFinal.ui"  # Nombre del archivo aquí.
url_base = "http://localhost:3000/api"
fecha_hora = datetime.now()
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_accion.clicked.connect(self.accion)
        self.arduino = None

        self.HS_1.setMinimum(0)
        self.HS_1.setMaximum(1)
        self.HS_1.setSingleStep(1)
        self.HS_1.setValue(0)
        self.HS_1.valueChanged.connect(self.apagar)
        self.HS_1.setEnabled(False)

        self.segundoPlano = QtCore.QTimer()
        self.segundoPlano.timeout.connect(self.control)
        self.Lista = []
        self.apagar = "1"

    def apagar(self):
        if self.HS_1.value() == 1:
            pygame.mixer.music.stop()
        elif self.HS_1.value() == 0:
            self.apagar = "1"

    def accion(self):
        try:
            if not self.txt_puerto.text() == "":
                txt_btn = self.btn_accion.text()
                if txt_btn == "CONECTAR":
                    self.txt_estado.setText("CONECTADO")
                    self.btn_accion.setText("DESCONECTAR")
                    puerto = "COM" + self.txt_puerto.text()
                    self.arduino = conecta.Serial(puerto, baudrate=9600, timeout=1)
                    self.segundoPlano.start(100)
                elif txt_btn == "DESCONECTAR":
                    self.txt_estado.setText("DESCONECTADO")
                    self.btn_accion.setText("RECONECTAR")
                    self.segundoPlano.stop()
                else:
                    self.txt_estado.setText("RECONECTADO")
                    self.btn_accion.setText("DESCONECTAR")
                    self.segundoPlano.start(100)
        except Exception as error:
            print(error)

    def control(self):
        if not self.arduino == None:
            if self.arduino.isOpen():
                variable = self.arduino.readline().decode()
                variable = variable.replace("\r", "")
                variable = variable.replace("\n", "")
                if variable != "":
                    for i in range(50):
                        self.Lista.append(int(variable))

                    def Cuartiles(lista):
                        n = len(lista)
                        q1 = 1 * (n + 1) / 4 - 1
                        if isinstance(q1, float):
                            q1 = lista[int(q1)] + q1 % 1 * (lista[int(q1 + 1)] - lista[int(q1)])
                        else:
                            q1 = lista[q1]
                        q2 = 2 * (n + 1) / 4 - 1
                        if isinstance(q2, float):
                            q2 = lista[int(q2)] + q2 % 1 * (lista[int(q2 + 1)] - lista[int(q2)])
                        else:
                            q2 = lista[q2]
                        q3 = 3 * (n + 1) / 4 - 1
                        if isinstance(q3, float):
                            q3 = lista[int(q3)] + q3 % 1 * (lista[int(q3 + 1)] - lista[int(q3)])
                        else:
                            q3 = lista[q3]
                        return q1, q2, q3

                    def Outliers_Suave(Q1, Q3, IQR, lista):
                        min_val = Q1 - (1.5 * IQR)
                        max_val = Q3 + (1.5 * IQR)
                        outliers = [x for x in lista if x < min_val or x > max_val]
                        return min_val, max_val, outliers

                    def Outliers_Extremo(Q1, Q3, IQR, lista):
                        min_val = Q1 - (3.0 * IQR)
                        max_val = Q3 + (3.0 * IQR)
                        outliers = [x for x in lista if x < min_val or x > max_val]
                        return min_val, max_val, outliers

                    print("Lista:")
                    print("Original: ", self.Lista)
                    self.Lista.sort()
                    print("Ordenada: ", self.Lista)
                    Q1, Q2, Q3 = Cuartiles(self.Lista)
                    IQR = Q3 - Q1
                    min_s, max_s, suave = Outliers_Suave(Q1, Q3, IQR, self.Lista)
                    min_e, max_e, extremo = Outliers_Extremo(Q1, Q3, IQR, self.Lista)
                    print("Q1: ", Q1)
                    print("Q2: ", Q2)
                    print("Q3: ", Q3)
                    print("IQR: ", IQR)
                    print("Min suave: ", min_s, "Max suave: ", max_s)
                    print("Min extremo: ", min_e, "Max extremo: ", max_e)
                    print("Outliers Suave: ", suave)
                    print("Outliers extremo: ", extremo)

                    outliers_indices = []
                    if len(suave) > 0 or len(extremo) > 0:
                        print("Hay Outliers")
                        print("Outliers Eliminados")
                        for outlier in suave:
                            if outlier in self.Lista:
                                outlier_index = self.Lista.index(outlier)
                                outliers_indices.append(outlier_index)
                                self.Lista.remove(outlier)
                        for outlier in extremo:
                            if outlier in self.Lista:
                                outlier_index = self.Lista.index(outlier)
                                outliers_indices.append(outlier_index)
                                self.Lista.remove(outlier)
                    else:
                        pass
                        print("No hay Outliers")

                    print(self.Lista)
                    V = mediana(self.Lista)
                    self.txt_2.setText(str(V))

                    obtenervalor = self.txt_2.text()
                    val = obtenervalor + "," + self.apagar + ","
                    self.arduino.write(val.encode())
                    self.Lista = []

                    if V < 6:
                        insertRecord(1, V)

                    if V < 6 and self.apagar == "1":
                        self.apagar = "2"
                        self.HS_1.setEnabled(True)
                        pygame.mixer.init()
                        pygame.mixer.music.load("alarma.mp3")
                        pygame.mixer.music.play(-1)

def mediana(datos):
    data = sorted(datos)
    index = len(data) // 2
    if len(datos) % 2 != 0:
        return data[index]
    return (data[index - 1] + data[index]) / 2

def insertRecord(id_sensor, current_value):
    # Post
    print("\n\nPOST")
    import json
    Id_sensor = id_sensor
    Current_value = current_value
    fecha_horafmt = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    url = url_base + "/"
    headers = {"Content-Type": "application/json"}
    body = {
        "id_sensor": Id_sensor,
        "valor_actual": Current_value,
        "fecha_record": fecha_horafmt
    }
    response = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
