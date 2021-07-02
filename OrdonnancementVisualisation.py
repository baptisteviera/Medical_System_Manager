# coding=utf-8
# !/bin/python
# author: Chenghao WANG
# Contact: chenghao.wang@hds.utc.fr
# institute: Heudiasyc, université de technologie de compiègne
# 28/09/2020
####################
import random
import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename


def color_list(my_patients):
    color = {my_patients[i].index: "#" + ''.join([random.choice('3456789ABCDEF') for _ in range(6)])
             for i in range(len(my_patients))}
    return color


class Treatment:
    def __init__(self, index_therapist, index_patient, treatment_start, treatment_end, travel_from):
        self.index_therapist = index_therapist
        self.index_patient = index_patient
        self.treatment_start = treatment_start
        self.treatment_end = treatment_end
        self.travel_from = travel_from


class Therapist:
    def __init__(self, index, my_treatments):
        self.index = index
        self.treatments = [item for item in my_treatments if item.index_therapist == self.index]
        self.treatments.sort(key=lambda x: x.treatment_start)


class Patient:
    def __init__(self, index, my_treatments):
        self.index = index
        self.treatments = [item for item in my_treatments if item.index_patient == self.index]
        self.treatments.sort(key=lambda x: x.treatment_start)


class GanttScheduling(tk.Frame):
    def __init__(self, root, factor=0.4):
        tk.Frame.__init__(self, root)

        # the height for a rectangle.
        self.rectangle_height = 5
        self.factor = factor
        # the slackness between two machine.
        self.inter_machine = int(0.4 * self.rectangle_height)
        self.delta_x = self.inter_machine
        self.delta_m = 10
        self.delta_y = self.rectangle_height
        # width and height for main windows.
        self.width_window = root.winfo_screenwidth()
        self.height_window = root.winfo_screenheight()
        self.canvas = tk.Canvas(self, width=self.width_window, height=self.height_window, background="white")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # my patient lists.
        self.my_patients = []
        # my therapist lists.
        self.my_therapists = []
        # my_treatment_lists.
        self.my_treatments = []
        self.my_color = []
        self.tipwindow = None
        # self.tipwindow_patient = None
        self.my_items = []

        self.pack()
        # Plot my scheduling figure.
        self.filename = askopenfilename(filetypes=(("solution files", "*.txt"), ("all files", "*.*")))
        if not self.filename:
            root.destroy()
        else:
            self.read_from_file()

            self.my_color = color_list(self.my_patients)
            posy = self.inter_machine

            for line in range(self.delta_m + self.delta_x,
                              self.delta_m + self.delta_x + int(1440 * self.factor),
                              5):  # range(start, stop, step)
                self.canvas.create_line([(line, posy + self.inter_machine), (
                    line, posy + len(self.my_therapists) * (self.rectangle_height + self.inter_machine))],
                                        dash=(3, 5), fill='black',
                                        tags='grid_line_w')
            # design for therapists.
            for therapist in self.my_therapists:
                posy += self.rectangle_height + self.inter_machine
                self.canvas.create_line(
                    self.delta_m + self.delta_x + 0 * self.factor, posy,
                    self.delta_m + self.delta_x + 1440 * self.factor, posy, width=3,
                    tag=("ML" + str(therapist.index)))

                self.canvas.create_text(self.delta_x, posy - self.rectangle_height / 2,
                                        text='Therapist' + str(therapist.index), tag=("M" + str(therapist.index)))

                for treatment in therapist.treatments:
                    fred = self.canvas.create_rectangle(
                        self.delta_m + self.delta_x + treatment.treatment_start * self.factor,
                        posy - 0.5 - self.rectangle_height,
                        self.delta_m + self.delta_x + treatment.treatment_end * self.factor,
                        posy - 0.5,
                        fill=self.my_color[treatment.index_patient], width=2, stipple='gray50', tag=(
                            "T" + str(treatment.index_therapist), "P" + str(treatment.index_patient),
                            "\ntreatment starts at:" + str(
                                treatment.treatment_start) + "\ntreatment terminates at:" + str(
                                treatment.treatment_end) + "\ntreatment duration:" + str(
                                treatment.treatment_end - treatment.treatment_start) + "\ntravelling time from previous treatment:" + str(
                                treatment.travel_from), "TM", str(treatment.treatment_start)))
                    self.canvas.tag_bind(fred, "<Any-Enter>", self.mouseEnter)
                    self.canvas.tag_bind(fred, "<Any-Leave>", self.mouseLeave)
                    self.canvas.tag_bind(fred, "<Button-3>", self.rightClick)
                    self.canvas.tag_bind(fred, "<Button-1>", self.leftClick)
                    self.my_items.append(fred)
                    fred = self.canvas.create_rectangle(
                        self.delta_m + self.delta_x + (
                                treatment.treatment_start - treatment.travel_from) * self.factor,
                        posy - 0.5 - self.rectangle_height,
                        self.delta_m + self.delta_x + treatment.treatment_start * self.factor,
                        posy - 0.5, fill=self.my_color[treatment.index_patient], width=2, state="hidden",
                        tag=("T" + str(treatment.index_therapist), "P" + str(treatment.index_patient),
                             "\ntreatment starts at:" + str(
                                 treatment.treatment_start) + "\ntreatment terminates at:" + str(
                                 treatment.treatment_end) + "\ntreatment duration:" + str(
                                 treatment.treatment_end - treatment.treatment_start) + "\ntravelling time from previous treatment:" + str(
                                 treatment.travel_from), "HI"))
                    self.canvas.tag_bind(fred, "<Any-Enter>", self.mouseEnter)
                    self.canvas.tag_bind(fred, "<Any-Leave>", self.mouseLeave)
                    self.canvas.tag_bind(fred, "<Button-3>", self.rightClick)
                    self.canvas.tag_bind(fred, "<Button-1>", self.leftClick)
                    self.my_items.append(fred)
        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        # linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        # windows scroll
        self.canvas.bind("<MouseWheel>", self.zoomer)

    def mouseEnter(self, event):
        # the CURRENT tag is applied to the object the cursor is over.
        # this happens automatically.
        my_tag = self.canvas.gettags(tk.CURRENT)

        self.tipwindow = tw = tk.Toplevel(self.canvas)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (event.x + self.canvas.winfo_rootx(), event.y + self.canvas.winfo_rooty() + 20))
        label = tk.Label(tw, text="treatment of patient " + my_tag[1] + " at therapist " + my_tag[0] + my_tag[2],
                         justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "12", "normal"))
        label.pack(ipadx=1)

    def leftClick(self, event):
        # the CURRENT tag is applied to the object the cursor is over.
        # this happens automatically.
        my_tag = self.canvas.gettags(tk.CURRENT)

        related_items = self.canvas.find_withtag(my_tag[1])
        for i in related_items:
            self.canvas.itemconfig(i, state="normal")

        rest_items = list(set(self.my_items) - set(related_items))
        for i in rest_items:
            self.canvas.itemconfig(i, state="hidden")

    def mouseLeave(self, event):

        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def rightClick(self, event):
        # the CURRENT tag is applied to the object the cursor is over.
        # this happens automatically.
        my_tag = self.canvas.gettags(tk.CURRENT)

        related_items = self.canvas.find_withtag(my_tag[1])
        rest_items = list(set(self.my_items) - set(related_items))
        for i in rest_items:
            if "HI" not in self.canvas.gettags(i):
                self.canvas.itemconfig(i, state="normal")
        for i in related_items:
            if "HI" in self.canvas.gettags(i):
                self.canvas.itemconfig(i, state="hidden")

    # read from file
    def read_from_file(self):
        with open(self.filename, "r") as fic:
            nb_pat_thr = fic.readline().split()
            therapists = []
            for _ in range(int(nb_pat_thr[0])):
                tmp_i = fic.readline().split()
                id_patient = tmp_i[0]
                my_nb_therapists_per_patient = int(tmp_i[1])
                for _ in range(my_nb_therapists_per_patient):
                    vn_i = fic.readline().split()
                    therapists.append(vn_i[0])
                    self.my_treatments.append(
                        Treatment(vn_i[0], id_patient, int(vn_i[1]), int(vn_i[2]), int(vn_i[3])))
                self.my_patients.append(Patient(id_patient, self.my_treatments))
            distinct_therapists = list({x: 1 for x in therapists}.keys())
            for i in range(len(distinct_therapists)):
                self.my_therapists.append(Therapist(distinct_therapists[i], self.my_treatments))

    # move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # windows zoom
    def zoomer(self, event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # linux zoom
    def zoomerP(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoomerM(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Scheduling of treatments")
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='icon_thp.png'))
    if len(sys.argv) < 2:
        GanttScheduling(root).pack(fill="both", expand=50)
    else:
        GanttScheduling(root, float(sys.argv[1])).pack(fill="both", expand=50)
    root.mainloop()
