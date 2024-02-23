import tkinter as tk

from util.summarizer import Summarizer

class TextSummarizationApp():
    def __init__(self, master):
        self.summarizer = Summarizer()
        self.master = master
        self.master.title("Sumaryzator")
        self.master.geometry("1000x600")
        self.master.resizable(False, False)

        # Input Textbox
        self.input_textbox = tk.Text(master, wrap="word", height=15)
        self.input_textbox.config(font=("Helvetica", 10))
        self.input_textbox.pack(fill="x", expand=True)

        # Frame for Slider, Button and Label
        self.horizontal_frame = tk.Frame(master)
        self.horizontal_frame.pack(padx=50, fill="x", expand=True)

        # Slider
        self.slider_value = tk.DoubleVar()
        self.slider = tk.Scale(self.horizontal_frame, from_=20, to=80, orient="horizontal", length=400, label="Część tekstu do pozostawienia (%):", variable=self.slider_value)
        self.slider.set(50)
        self.slider.pack(side="left")

        # Button
        self.button = tk.Button(self.horizontal_frame, width=30, height=2, text="Wykonaj!", command=self.handle_button_click)
        self.button.pack(padx=50, side="left")

        # Label
        self.label = tk.Label(self.horizontal_frame)
        self.label.pack(side="left")

        # Output Textbox
        self.output_textbox = tk.Text(master, wrap="word", state="disabled", height=15)
        self.output_textbox.config(font=("Helvetica", 10))
        self.output_textbox.pack(fill="x", expand=True)

    def set_label(self, words_count):
        minutes = words_count / 250
        seconds = round((minutes - int(minutes)) * 60)
        self.label.config(text="Liczba słów: {:d}\nCzas czytania: {:d} min {:02d} s".format(words_count, int(minutes), int(seconds)))

    def handle_button_click(self):
        input_text = self.input_textbox.get("1.0", "end-1c")
        output_text, words_count = self.summarizer.summarize(input_text, self.slider_value.get() / 100.)
        self.output_textbox.config(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", output_text)
        self.output_textbox.config(state="disabled")
        self.set_label(words_count)

def main():
    root = tk.Tk()
    TextSummarizationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()