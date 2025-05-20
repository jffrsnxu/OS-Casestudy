import tkinter as tk
from tkinter import messagebox, scrolledtext
import random

class PageReplacementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FIFO, LRU, and Optimal (OPT) Page-Replacement Algorithms")
        self.root.geometry("950x600")
        self.root.configure(bg="#E8ECF1")  

        # Fonts
        font_label = ("Segoe UI", 12)
        font_entry = ("Segoe UI", 12)
        font_button = ("Segoe UI", 11)
        font_output = ("Consolas", 11)

        # Header
        header = tk.Label(
            root,
            text="Page Replacement Simulator",
            font=("Segoe UI", 18, "bold"),
            bg="#E8ECF1",
            fg="#333"
        )
        header.pack(pady=(20, 10))

        # Input "Card"
        input_card = tk.Frame(root, bg="white", bd=1, relief="solid")
        input_card.pack(pady=10, padx=20, fill=tk.X, ipadx=10, ipady=10)

        tk.Label(input_card, text="Number of Page Frames:", font=font_label, bg="white").pack(side=tk.LEFT, padx=(10, 5))
        self.frame_input = tk.Entry(input_card, font=font_entry, width=5, bd=1, relief="solid")
        self.frame_input.pack(side=tk.LEFT, padx=5)

        self.run_button = tk.Button(
            input_card,
            text="Run Simulation",
            font=font_button,
            bg="#4CAF50",
            fg="white",
            activebackground="#45A049",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=self.run_simulation
        )
        self.run_button.pack(side=tk.LEFT, padx=10)

        # Output area in styled container
        output_container = tk.Frame(root, bg="#E8ECF1", padx=20, pady=10)
        output_container.pack(fill=tk.BOTH, expand=True)

        self.output_area = scrolledtext.ScrolledText(
            output_container,
            wrap=tk.WORD,
            font=font_output,
            bg="white",
            fg="#000",
            relief="flat",
            borderwidth=5
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)

    def run_simulation(self):
        self.output_area.delete("1.0", tk.END)

        try:
            frames = int(self.frame_input.get())
            if not (1 <= frames <= 9):
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of frames (1–9).")
            return

        reference = [random.randint(0, 9) for _ in range(20)]


        self.output_area.insert(tk.END, f"📄 Page Reference String:\n{reference}\n\n")

        self.output_area.insert(tk.END, "📦 FIFO Simulation\n")
        fifo_faults = self.fifo(reference, frames)
        self.output_area.insert(tk.END, f"Page Faults: {fifo_faults}\n\n")

        self.output_area.insert(tk.END, "📦 LRU Simulation\n")
        lru_faults = self.lru(reference, frames)
        self.output_area.insert(tk.END, f"Page Faults: {lru_faults}\n\n")

        self.output_area.insert(tk.END, "📦 Optimal Simulation\n")
        opt_faults = self.optimal(reference, frames)
        self.output_area.insert(tk.END, f"Page Faults: {opt_faults}\n\n")

    def display_frames(self, ref, frame_history, frame_count):
        self.output_area.insert(tk.END, "\nFrames ↓ |" + "".join(f" {p:>5} |" for p in ref) + "\n")
        self.output_area.insert(tk.END, "-" * (8 + 7 * len(ref)) + "\n")
        for i in range(frame_count):
            self.output_area.insert(tk.END, f"Frame {i+1:<2} |")
            for val in frame_history[i]:
                self.output_area.insert(tk.END, f" {val:>5} |")
            self.output_area.insert(tk.END, "\n")

    def fifo(self, ref, frame_count):
        from collections import deque
        frames = deque()
        frame_history = [[] for _ in range(frame_count)]
        faults = 0

        for page in ref:
            if page not in frames:
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    frames.popleft()
                    frames.append(page)
                faults += 1
            # Create snapshot for display
            snap = [str(frames[i]) if i < len(frames) else " " for i in range(frame_count)]
            for j in range(frame_count):
                frame_history[j].append(snap[j])

        self.display_frames(ref, frame_history, frame_count)
        return faults



    def lru(self, ref, frame_count):
        frames = []
        usage = {}
        frame_history = [[] for _ in range(frame_count)]
        faults = 0

        for i, page in enumerate(ref):
            if page not in frames:
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    # Find least recently used page
                    lru_page = min(usage, key=usage.get)
                    lru_index = frames.index(lru_page)
                    frames[lru_index] = page
                    del usage[lru_page]
                faults += 1
            # Update usage info
            usage[page] = i

            snap = [str(frames[i]) if i < len(frames) else " " for i in range(frame_count)]
            for j in range(frame_count):
                frame_history[j].append(snap[j])

        self.display_frames(ref, frame_history, frame_count)
        return faults


    def optimal(self, ref, frame_count):
        frames = []
        frame_history = [[] for _ in range(frame_count)]
        faults = 0

        for i in range(len(ref)):
            page = ref[i]

            if page not in frames:
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    future_uses = {}
                    for f in frames:
                        try:
                            next_use = ref[i+1:].index(f)
                            future_uses[f] = next_use
                        except ValueError:
                            future_uses[f] = float("inf")
                    page_to_replace = max(future_uses, key=future_uses.get)
                    replace_index = frames.index(page_to_replace)
                    frames[replace_index] = page
                faults += 1

            snap = [str(frames[j]) if j < len(frames) else " " for j in range(frame_count)]
            for j in range(frame_count):
                frame_history[j].append(snap[j])

        self.display_frames(ref, frame_history, frame_count)
        return faults

    
# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementGUI(root)
    root.mainloop()
