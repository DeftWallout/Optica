import customtkinter as ctk
import clr
import sys
import os

# Ruta donde están las DLLs de Kinesis
dll_path = r"C:\Program Files\Thorlabs\Kinesis"
sys.path.append(dll_path)
os.chdir(dll_path)

# Cargar las DLLs de Kinesis
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
clr.AddReference("Thorlabs.MotionControl.Benchtop.StepperMotorCLI")

# Importar las clases necesarias
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import BenchtopStepperMotor

# Inicializar Device Manager y obtener lista de dispositivos
DeviceManagerCLI.BuildDeviceList()

# Clase para manejar el motor con Kinesis
class MotorKinesis:
    def __init__(self, serial_number):
        self.serial_number = str(serial_number)
        self.motor = BenchtopStepperMotor.CreateBenchtopStepperMotor(self.serial_number)
        self.motor.Connect(self.serial_number)

        if not self.motor.IsSettingsInitialized():
            self.motor.WaitForSettingsInitialized(10000)

        self.motor.StartPolling(250)
        self.motor.EnableDevice()
        print(f"Motor {self.serial_number} conectado.")

    def move_by(self, distance_mm):
        current_pos = self.motor.Position
        target_pos = current_pos + distance_mm
        self.motor.SetMoveAbsolutePosition(target_pos)
        self.motor.MoveAbsolute(60000)
        print(f"Motor movido a {target_pos:.2f} mm.")

    def move_to(self, position_mm):
        self.motor.SetMoveAbsolutePosition(position_mm)
        self.motor.MoveAbsolute(60000)
        print(f"Motor movido a {position_mm:.2f} mm.")

    @property
    def position(self):
        return self.motor.Position

    def close(self):
        self.motor.StopPolling()
        self.motor.Disconnect(True)
        print(f"Motor {self.serial_number} desconectado.")


# --- Funciones de la interfaz gráfica ---
def move_forward(motor):
    motor.move_by(1)

def move_backward(motor):
    motor.move_by(-1)

def move_to_position(motor, entry):
    try:
        pos = float(entry.get())
        motor.move_to(pos)
    except ValueError:
        print("Entrada inválida")

def update_position(label, motor):
    pos = motor.position
    label.configure(text=f"Posición: {pos:.2f} mm")
    label.after(500, update_position, label, motor)

def close_motors():
    motor1.close()
    motor2.close()
    app.quit()

# --- Crear la ventana de la interfaz gráfica ---
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema de color

# Inicializar motores
motor1 = MotorKinesis("701749")  # Usa el número de serie de tu motor
motor2 = MotorKinesis("701794")  # Otro motor, si tienes

# Crear la ventana principal
app = ctk.CTk()
app.title("Control de Motores Thorlabs")

# Crear un marco para el primer motor
frame1 = ctk.CTkFrame(app)
frame1.pack(padx=20, pady=20, side="left")

# Crear un marco para el segundo motor
frame2 = ctk.CTkFrame(app)
frame2.pack(padx=20, pady=20, side="right")

# --- Motor 1 ---
ctk.CTkLabel(frame1, text="Motor 1").pack(pady=10)

pos_label1 = ctk.CTkLabel(frame1, text="Posición: --- mm")
pos_label1.pack(pady=5)

entry1 = ctk.CTkEntry(frame1, placeholder_text="Posición (mm)")
entry1.pack(pady=5)

ctk.CTkButton(frame1, text="Mover Adelante", command=lambda: move_forward(motor1)).pack(pady=5)
ctk.CTkButton(frame1, text="Mover Atrás", command=lambda: move_backward(motor1)).pack(pady=5)
ctk.CTkButton(frame1, text="Mover a Posición", command=lambda: move_to_position(motor1, entry1)).pack(pady=5)

# --- Motor 2 ---
ctk.CTkLabel(frame2, text="Motor 2").pack(pady=10)

pos_label2 = ctk.CTkLabel(frame2, text="Posición: --- mm")
pos_label2.pack(pady=5)

entry2 = ctk.CTkEntry(frame2, placeholder_text="Posición (mm)")
entry2.pack(pady=5)

ctk.CTkButton(frame2, text="Mover Adelante", command=lambda: move_forward(motor2)).pack(pady=5)
ctk.CTkButton(frame2, text="Mover Atrás", command=lambda: move_backward(motor2)).pack(pady=5)
ctk.CTkButton(frame2, text="Mover a Posición", command=lambda: move_to_position(motor2, entry2)).pack(pady=5)

# Botón de cierre
exit_btn = ctk.CTkButton(app, text="Cerrar y Salir", command=close_motors)
exit_btn.pack(pady=20)

# Actualizar la posición en tiempo real
update_position(pos_label1, motor1)
update_position(pos_label2, motor2)

# Ejecutar la app
app.mainloop()