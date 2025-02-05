import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import ffmpeg
import os

# Функция для выбора исходного файла
def choose_input_file():
    input_file = filedialog.askopenfilename(filetypes=[("Video files", "*.mkv")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_file)

# Функция для выбора пути и названия выходного файла
def choose_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video files", "*.mp4")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_file)

# Функция для выполнения конвертации с использованием ffmpeg-python
def run_ffmpeg_conversion():
    input_file = input_entry.get()
    output_file = output_entry.get()

    if not input_file or not output_file:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите исходный и выходной файлы.")
        return

    try:
        # Используем ffmpeg-python для выполнения конвертации
        (
            ffmpeg
            .input(input_file)
            .output(output_file, c='copy', strict='-2')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        # Если конвертация успешна, запрашиваем подтверждение удаления исходного файла
        if messagebox.askyesno("Удаление файла", "Удалить исходный файл после конвертации?"):
            os.remove(input_file)
            messagebox.showinfo("Успешно", "Конвертация завершена успешно и исходный файл удален.")
        else:
            messagebox.showinfo("Успешно", "Конвертация завершена успешно.")
    except ffmpeg.Error as e:
        # Обработка ошибки, если что-то пошло не так
        error_message = e.stderr.decode('utf-8') if e.stderr else str(e)
        messagebox.showerror("Ошибка", f"Ошибка при конвертации: {error_message}")

# Создаем главное окно приложения
app = tk.Tk()
app.title("Конвертер видео")

# Создаем и настраиваем элементы управления
input_label = tk.Label(app, text="Исходный файл:")
input_label.pack()
input_entry = tk.Entry(app)
input_entry.pack()
input_button = tk.Button(app, text="Выбрать файл", command=choose_input_file)
input_button.pack()

output_label = tk.Label(app, text="Выходной файл:")
output_label.pack()
output_entry = tk.Entry(app)
output_entry.pack()
output_button = tk.Button(app, text="Выбрать файл", command=choose_output_file)
output_button.pack()

convert_button = tk.Button(app, text="Конвертировать", command=run_ffmpeg_conversion)
convert_button.pack()

# Запускаем главный цикл приложения
app.mainloop()
