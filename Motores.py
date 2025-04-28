import clr
import os
import sys

# Ruta donde están las DLLs de Kinesis
dll_path = r"C:\Program Files\Thorlabs\Kinesis"

# Agregarlas al sistema
sys.path.append(dll_path)
os.chdir(dll_path)

# Importar las DLLs principales
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
clr.AddReference("Thorlabs.MotionControl.Benchtop.StepperMotorCLI")  # Depende del dispositivo

# Importar clases específicas
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import BenchtopStepperMotor

# Inicializar el Device Manager
DeviceManagerCLI.BuildDeviceList()

serial_numbers = DeviceManagerCLI.GetDeviceList()
print("Motores detectados:")
for sn in serial_numbers:
    print(f" - Serial: {sn}")
serial_number = "701749"  # <-- PON AQUÍ EL SERIAL DE TU MOTOR

# Crear el objeto motor
motor = BenchtopStepperMotor.CreateBenchtopStepperMotor(serial_number)
motor.Connect(serial_number)

# Esperar a que el motor esté listo
if not motor.IsSettingsInitialized():
    motor.WaitForSettingsInitialized(10000)

# Empezar a escuchar eventos del motor
motor.StartPolling(250)
motor.EnableDevice()

# Hacer "home" (llevarlo al origen mecánico)
print("Haciendo Home...")
motor.Home(60000)

# Mover 1 mm hacia adelante
current_position = motor.Position
print(f"Posición actual: {current_position:.3f} mm")

new_position = current_position + 1.0  # Mover 1 mm
motor.SetMoveAbsolutePosition(new_position)
motor.MoveAbsolute(60000)

print(f"Motor movido a {new_position:.3f} mm")

# Finalmente, detener el polling y desconectar
motor.StopPolling()
motor.Disconnect(True)









