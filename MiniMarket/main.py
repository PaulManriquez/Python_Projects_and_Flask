from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Products import ProductsTestClass
from datetime import datetime

class Interface(Frame):
    Myproducts = ProductsTestClass()
    def __init__(self,master=None):
        super().__init__(master,width=850, height=600)
        self.master = master
        self.pack()
        self.CreateInterface()
        self.FillData()
        self.CurrentTotalSell = self.GetCurrentTotalSell()
        self.ShowingTotalSells.insert(0,str(self.CurrentTotalSell))
        self.ShowingTotal.configure(state='normal')
        self.ShowingTotal.insert(0, '0.0')
        self.ShowingTotal.configure(state="disabled")
        self.ShowingTotalSells.configure(state="disabled")
        self.TotalToPay = 0.0
        #
        self.EnableModifyDB_TXT('disabled')
        self.ModifyOrAdd = -1 #Key to know what operation to perform

    def GetCurrentTotalSell(self):
        try:
            with open('TotalSellsDay.txt','r') as file:
                content = file.read()
            return float(content)
        except Exception as e:
            return 0.00

    def FillData(self):#Fill data base
        data = self.Myproducts.GetProducts() #Get a list of touples
        RowNumber = 0
        for row in data:
            self.grid.insert("",END,text=str(RowNumber), values=(row[0],row[1],row[2]))
            RowNumber+=1

        #Try to each time you start select the first data selected
        #if len(self.grid.get_children()) > 0:
        #    self.grid.selection_set(self.grid.get_children()[0])

    def FillDataCurrentProductsToBuy(self):
        data = self.Myproducts.ReadCodes() #Get a list of touples
        RowNumber = 0
        Total = 0.0
        for row in data:
            self.Topgrid.insert("",END,text=str(RowNumber), values=(row[0],row[1]))
            RowNumber+=1
            Total += float(row[1])

        return Total

    def ClearUpperGrid(self):
        for item in self.Topgrid.get_children():
            self.Topgrid.delete(item)

    def ClearDatabaseGrid(self):
        for item in self.grid.get_children():
            self.grid.delete(item)
    def GetEntry(self,PlaceIn,X,Y,W,H):
        Maketxt = Entry(PlaceIn)
        Maketxt.place(x=X,y=Y,width=W,height=H)
        return Maketxt

    def GetFrame(self,Bg,X,Y,W,H):
        MyFrame = Frame(self, bg=Bg)
        MyFrame.place(x=X, y=Y, width=W, height=H)
        return MyFrame


    def GetLabel(self, PlaceIn, TXT, X, Y, width=None, height=None,anch=None):
        lbl1 = Label(PlaceIn, text=TXT, width=width, height=height)
        lbl1.place(x=X, y=Y,anchor=anch)
        return lbl1

    def GetCenterLabel(self, PlaceIn, TXT, width=None, height=None):
        lbl1 = Label(PlaceIn, text=TXT, width=width, height=height)
        lbl1.place(relx=0.5, rely=0.5, anchor='center')
        return lbl1

    def GetButton(self,Place,TxtB,Action,Bg,Fg,X,Y,W,H):
        NewB = Button(Place,text=TxtB,command=Action,bg=Bg,fg=Fg)
        NewB.place(x=X,y=Y,width=W,height=H)
        return NewB

    def EnableModifyDB_TXT(self,Enable:str):
        self.ClaveTXT.config(state='normal')
        self.PrecioTXT.config(state='normal')
        self.ProductoTXT.config(state='normal')
        self.ClaveTXT.delete(0,END)
        self.PrecioTXT.delete(0, END)
        self.ProductoTXT.delete(0, END)
        self.ClaveTXT.config(state=Enable)
        self.PrecioTXT.config(state=Enable)
        self.ProductoTXT.config(state=Enable)


    def CreateInterface(self):
        #====================== Top Frame work =============================================
        Frame0 = self.GetFrame("red", 0, 0, 850, 30)
        Frame1 = self.GetFrame("#bfdaff",0,30,850,200)
        Label1 = self.GetCenterLabel(Frame0,"Productos a Pagar",width=130,height=2)

        # =======Grid
        self.Topgrid = ttk.Treeview(Frame1, columns=("col1", "col2"))
        self.Topgrid.column("#0", width=40)
        self.Topgrid.column("col1", width=600, anchor=CENTER)
        self.Topgrid.column("col2", width=180, anchor=CENTER)


        self.Topgrid.heading("#0", text="No:" )
        self.Topgrid.heading("col1", text="Producto", anchor=CENTER)
        self.Topgrid.heading("col2", text="Precio", anchor=CENTER)


        self.Topgrid.pack(side=LEFT, fill=Y)
        sb2 = Scrollbar(Frame1, orient=VERTICAL, width=30)
        sb2.pack(side=RIGHT, fill=Y)
        self.Topgrid.config(yscrollcommand=sb2.set)
        sb2.config(command=self.Topgrid.yview)

        #====================== Left Frame work =============================================
        Frame2 = self.GetFrame("red", 0, 230, 450, 30)
        Frame3 = self.GetFrame("#bfdaff", 0, 260, 450, 240)
        Label2 = self.GetCenterLabel(Frame2, "Mostrando base de datos", width=450, height=2)

        #=======Grid
        self.grid = ttk.Treeview(Frame3, columns=("col1", "col2", "col3"))
        self.grid.column("#0", width=40)
        self.grid.column("col1", width=80, anchor=CENTER)
        self.grid.column("col2", width=160, anchor=CENTER)
        self.grid.column("col3", width=150, anchor=CENTER)

        self.grid.heading("#0", text="Id", anchor=CENTER)
        self.grid.heading("col1", text="Clave", anchor=CENTER)
        self.grid.heading("col2", text="Producto", anchor=CENTER)
        self.grid.heading("col3", text="Precio", anchor=CENTER)

        self.grid.pack(side=LEFT, fill=Y)
        sb = Scrollbar(Frame3, orient=VERTICAL, width=17)
        sb.pack(side=RIGHT, fill=Y)
        self.grid.config(yscrollcommand=sb.set)
        sb.config(command=self.grid.yview)


        #====================== Upper right Frame ============================================
        Frame4 = self.GetFrame("red", 450, 230, 400, 30)
        Frame5 = self.GetFrame("#D5DAD9", 450, 260, 400, 100)#170
        Label3 = self.GetCenterLabel(Frame4, "Control de base de datos", width=400, height=2)

        self.btnLaser = self.GetButton(Frame5,"Leer\nCodigos",self.Shoot,"Red","white",185,10,50,50)
        self.btnEliminar = self.GetButton(Frame5, "Eliminar producto a pagar", self.DeleteP, "#F82C2C", "white", 245, 5, 150, 30)

        self.btnFinishSellsDay = self.GetButton(Frame5, "Realizar Corte", self.FSellsDay, "#D2D225", "white", 245, 40, 150, 25)
        self.btnFinishSellsDay.config(font=('Arial', 12))

        #Set on id data base / search product
        self.btnSearchInDB = self.GetButton(Frame5, "Buscar producto", self.SearchProduct, "#51927D", "white",30, 10, 120, 30)
        self.btnSearchInDB.configure(font=('Arial', 12))

        self.SearchInDBTXT = self.GetEntry(Frame5, 3, 43, 170, 20)
        self.SearchInDBTXT.config(font=('Arial', 12))

        # ====================== Lower right Frame ============================================
        Frame6 = self.GetFrame("red", 450, 330, 400, 30)
        Frame7 = self.GetFrame("#D5DAD9", 450, 360, 400, 140)  # 170
        Label4 = self.GetCenterLabel(Frame6, "Total de productos", width=400, height=2)
        #
        self.ShowingTotal = self.GetEntry(Frame7,320,100,70,30)
        self.ShowingTotal.config(font=('Arial',14))
        self.LabelTotal = self.GetLabel(Frame7," Total a pagar $",185,104)
        self.LabelTotal.configure(font=('Arial',13))
        self.LabelTotal.configure(bg="#D5DAD9")

        self.ExtraMount = self.GetEntry(Frame7, 320, 10, 70, 37)
        self.ExtraMount.config(font=('Arial', 12))
        self.btnExtraM = self.GetButton(Frame7, "Agregar monto\n extra a total $", self.AddExtra,"#51927D","white",185,10,120,37)
        self.btnExtraM.configure(font=('Arial', 12))

        self.SubtractM = self.GetEntry(Frame7, 320, 55, 70, 37)
        self.SubtractM.config(font=('Arial', 12))
        self.btnSubstM = self.GetButton(Frame7, "Eliminar monto\n a total $", self.SubtractMEx, "#51927D", "white", 185, 55, 120, 37)
        self.btnSubstM.configure(font=('Arial', 12))

        #
        self.btnFinishSell = self.GetButton(Frame7, "Finalizar venta", self.FinishSell, "#2BCE0E", "white", 35, 101,120, 30)
        self.btnFinishSell.config(font=('Arial',12))

        #
        self.ShowingTotalSells = self.GetEntry(Frame7, 55, 38, 70, 20)
        self.ShowingTotalSells.config(font=('Arial', 11))
        self.LabelTotalSells = self.GetLabel(Frame7, "Ventas totales del dia", 5, 10)
        self.LabelTotalSells.configure(font=('Arial', 12))
        self.LabelTotalSells.configure(bg='#D5DAD9')
        self.LabelS = self.GetLabel(Frame7, "$", 35, 37)
        self.LabelS.config(bg='#D5DAD9')
        self.LabelS.configure(font=('Arial', 11))

        #============================LOWER LOWER FRAME==================================================================
        Frame8 = self.GetFrame("red", 0, 500, 850, 30)
        Frame9 = self.GetFrame("#D5DAD9", 0, 530, 850, 80)
        Label5 = self.GetCenterLabel(Frame8, "Modificar base de datos", width=850, height=2)
        #TXT boxs entries
        self.ClaveTXT = self.GetEntry(Frame9, 10, 40, 100, 20)
        self.ClaveTXT.config(font=('Arial', 11))
        self.LabelClave = self.GetLabel(Frame9, "Clave", 40, 10)
        self.LabelClave.configure(font=('Arial', 12))
        self.LabelClave.config(bg='#D5DAD9')

        self.ProductoTXT = self.GetEntry(Frame9, 120, 40, 100, 20)
        self.ProductoTXT.config(font=('Arial', 11))

        self.LabelProducto = self.GetLabel(Frame9, "Producto", 135, 10)
        self.LabelProducto.configure(font=('Arial', 12))
        self.LabelProducto.config(bg='#D5DAD9')

        self.PrecioTXT = self.GetEntry(Frame9, 230, 40, 100, 20)
        self.PrecioTXT.config(font=('Arial', 11))
        self.LabelPrecio = self.GetLabel(Frame9, "Precio", 250, 10)
        self.LabelPrecio.configure(font=('Arial', 12))
        self.LabelPrecio.configure(bg='#D5DAD9')
        #Buttons
        self.btnModify = self.GetButton(Frame9, "Modificar", self.ModifyDataBase, "#3194B9", "white", 350,30, 120, 35)
        self.btnModify.configure(font=('Arial', 13))

        self.btnAgregar = self.GetButton(Frame9, "Agregar producto", self.AddNewProduct, "#3194B9", "white", 480, 30, 140, 35)
        self.btnAgregar.configure(font=('Arial', 13))

        self.btnGuardar = self.GetButton(Frame9, "Guardar", self.fGuardar, "#2BCE0E", "white", 730, 5,100, 30)
        self.btnGuardar.configure(font=('Arial', 13))

        self.btnCancelar = self.GetButton(Frame9, "Cancelar", self.fCancelar, "#F82C2C", "white", 700, 38, 100, 30)
        self.btnCancelar.configure(font=('Arial', 13))


    def Shoot(self):
        self.ClearUpperGrid()
        self.ShowingTotal.configure(state="normal")
        self.ShowingTotal.delete(0,END)
        Total = self.FillDataCurrentProductsToBuy() + self.TotalToPay

        FTotal = "{:.2f}".format(Total)
        self.ShowingTotal.insert(0,FTotal)
        self.ShowingTotal.configure(state="disabled")  # Only lecture mode



    def DeleteP(self):#Delete product
        selected = self.Topgrid.focus()
        clave = self.Topgrid.item(selected,'values')
        if clave == '':
            messagebox.showwarning("Eliminar","Selecciona un elemento")
        else:
            ans = messagebox.askquestion('Eliminar',"Desea eliminar el registro?")
            if ans == messagebox.YES:
                #get the id of clave with a sql sentence
                ID = self.Myproducts.GetIDProduct(clave[0])
                #Delete from the txt ScannerCodesLectures
                IDCode = str(ID[0])
                self.Myproducts.DeleteLecture(IDCode)
                #Update current products list
                self.Shoot()


    def FinishSell(self):
        #Add message box
        ans = messagebox.askquestion('Finalizar compra', "Desea finalizar la compra?")
        if ans == messagebox.YES:
            #Clear current total to pay
            self.ShowingTotal.configure(state="normal")
            self.ShowingTotal.delete(0,END)
            #Clear and save the current total sell
            self.ClearUpperGrid()
            self.CurrentTotalSell += self.FillDataCurrentProductsToBuy() + self.TotalToPay
            self.ClearUpperGrid()
            #Delete the codes readed in ScannerCodesLectures
            with open('ScannerCodesLectures.txt','w') as file:
                pass
            #Show the current total sells
            self.ShowingTotalSells.configure(state="normal")
            self.ShowingTotalSells.delete(0,END)
            self.ShowingTotalSells.insert(0,round(self.CurrentTotalSell,3))
            self.ShowingTotalSells.configure(state="disabled")
            self.ShowingTotal.configure(state="disabled")

            self.TotalToPay = 0.0
            #Write in the file TotalSellsDay
            with open('TotalSellsDay.txt','w') as File:
                File.write(str(self.CurrentTotalSell))

    def AddExtra(self):
        try:
            ans = messagebox.askquestion('Agregar extra', "Desea agregar monto extra la compra?")
            if ans == messagebox.YES:
                data = self.ExtraMount.get()
                self.TotalToPay += float(data)
                self.Shoot()

            self.ExtraMount.delete(0, END)
        except ValueError:
            self.ExtraMount.delete(0, END)
            messagebox.showwarning("Error","Introduce un numero")

    def SubtractMEx(self):
        try:
            ans = messagebox.askquestion('Restar monto a compra', "Desea restar un monto a la compra?")
            if ans == messagebox.YES:
                data = self.SubtractM.get()
                self.TotalToPay -= float(data)
                self.Shoot()
            self.SubtractM.delete(0, END)
        except ValueError:
            self.SubtractM.delete(0, END)
            messagebox.showwarning("Error","Introduce un numero")

    def FSellsDay(self):
        ans = messagebox.askquestion('Realizar corte', "Desea terminar el corte del dia?")
        if ans == messagebox.YES:
            CurrentDateTime = datetime.now()
            DateTime = CurrentDateTime.strftime("%Y-%m-%d %H:%M:%S")
            with open('TotalSellsDay.txt','w') as f:#Delete the content of the current total sells
                pass
            SaveData = "Total $" + str(self.CurrentTotalSell) + " Fecha: " + DateTime + "\n"
            #write in the TotalSellsDay
            with open('AllMySells.txt','a') as F:
                F.write(SaveData)

            self.CurrentTotalSell = 0.0
            self.ShowingTotalSells.configure(state="normal")
            self.ShowingTotalSells.delete(0, END)
            self.ShowingTotalSells.configure(state="disabled")

    def ModifyDataBase(self):
        selected = self.grid.focus()
        id = self.grid.item(selected, 'text')  # Get the id of the selected element
        if id == '':
            messagebox.showwarning("Modificar","Selecciona un elemento de la base de datos")
        else:
            self.EnableModifyDB_TXT('normal')
            values = self.grid.item(selected,'values')
            self.ClaveTXT.insert(0,values[0])
            self.ProductoTXT.insert(0, values[1])
            self.PrecioTXT.insert(0, values[2])
            self.btnAgregar.configure(state='disabled')
            self.ClaveTXT.config(state='disabled')
            self.ModifyOrAdd = id #To know what operation to perform

    def AddNewProduct(self):
        self.EnableModifyDB_TXT('normal')#Enable txts to enter data
        self.btnModify.config(state='disabled')#Current opeation not abailable


    def fGuardar(self):
        if self.ModifyOrAdd == -1:#Add a new product case
            if(self.ClaveTXT.get() and self.ProductoTXT.get() and self.PrecioTXT.get() != None):#If all the data was satisfied
                ans = messagebox.askquestion("Agregar producto","Estas seguro de agregar este producto?")
                if ans == messagebox.YES:
                    self.Myproducts.InsertNewProduct(self.ClaveTXT.get(),self.ProductoTXT.get(),self.PrecioTXT.get())
                    self.EnableModifyDB_TXT('disabled')
                    # Update data base
                    self.ClearDatabaseGrid()
                    self.FillData()
                    self.btnModify.config(state='normal')
                    messagebox.showinfo("Agregado", "Se ha agregado un nuevo producto")


        else:#Modify a product
            ans =messagebox.askquestion('Modificar','esta seguro de modificar de la base de datos?')
            if ans == messagebox.YES:
                self.ClaveTXT.config(state='normal')
                self.Myproducts.ModifyProduct(self.ClaveTXT.get(),self.ProductoTXT.get(),self.PrecioTXT.get())
                self.EnableModifyDB_TXT('disabled')
                self.ModifyOrAdd = -1 #return to base case
                #Update data base
                self.ClearDatabaseGrid()
                self.FillData()
                messagebox.showinfo("Modificado","Se han realizado los cambios")
                #Enable button
                self.btnAgregar.configure(state='normal')

    def fCancelar(self):
        ans = messagebox.askquestion("Cancelar","Cancelar operacion?")
        if ans == messagebox.YES:
            self.EnableModifyDB_TXT("disabled")
            self.btnModify.configure(state='normal')
            self.btnAgregar.configure(state='normal')
            self.ModifyOrAdd = -1 #Normal state

    def SearchProduct(self):
        data = self.Myproducts.GetProducts()  # Get a list of touples
        productToSearch = self.SearchInDBTXT.get()
        IdRow = 0 #Found in row
        Found = False
        for row in data:
            if row[1] == productToSearch:
                Found = True
                self.grid.selection_set(self.grid.get_children()[IdRow])
                break
            else:
                IdRow+=1

        if(Found):
            messagebox.showinfo('Encontrado',f"El producto se encuentra en la linea {IdRow}")
        else:
            messagebox.showinfo('No encontrado','El producto no se encuentra en la base de datos')
        self.SearchInDBTXT.delete(0,END)
def main():
    root = Tk()
    root.wm_title("Mini market Paul")
    app = Interface(root)
    app.mainloop()

if __name__ == "__main__":
    main()