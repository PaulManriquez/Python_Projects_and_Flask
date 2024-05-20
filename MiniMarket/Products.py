import mysql.connector

class ProductsTestClass():
    def __init__(self):#Constructor
        self.cnn = mysql.connector.connect(host="localhost", user="root",
                                      passwd="password", database="MiniMarketDataBase")

    def __str__(self):#Special
        datos = self.GetProducts()
        aux = ""
        for row in datos:
            aux += str(row) + '\n'
        return aux #Return a string

    def GetProducts(self):  # Private
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM ProductTest")
        datos = cur.fetchall() #Get a touple list
        # self.cnn.close()
        # cur.close()
        return datos

    def ReadCodes(self): #Return the current products readed by
        try:

            with open('ScannerCodesLectures.txt', 'r') as file:
                # Read all lines from the file and store them in a list
                lines = [line.strip() for line in file]  # Get the codes

            # Make the query
            cur = self.cnn.cursor()
            ListProducts = []
            for code in lines:
                # Using parameterized query to prevent SQL injection
                sqlSentence = "SELECT Producto, Precio FROM producttest WHERE ID = %s"
                cur.execute(sqlSentence, (code,))
                result = cur.fetchone()  # Assuming you expect only one result
                if result:
                    ListProducts.append(result)

            return ListProducts
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def GetIDProduct(self,Pname:str):
        cur = self.cnn.cursor()
        sqlSentence = "SELECT ID FROM producttest WHERE Producto = %s"
        cur.execute(sqlSentence, (Pname,))
        return cur.fetchone()

    def DeleteLecture(self,Code:str):
        with open('ScannerCodesLectures.txt','r') as file:
            lines = file.readlines()

        #Search for the code
        found = False
        for i,line in enumerate(lines):
            if Code in line:
                found = True
                del lines[i]
                break
        #Re write if the line was founded
        if found:
            with open('ScannerCodesLectures.txt','w') as File:
                File.writelines(lines)

    def InsertNewProduct(self, Id, producto, precio):
        cur = self.cnn.cursor()
        sqlSentence = '''INSERT INTO producttest (ID, Producto, Precio) VALUES('{}','{}',{})'''.format(Id, producto,precio)
        cur.execute(sqlSentence)
        self.cnn.commit()  # Commit changes to the database
        cur.close()
        #print("Exito")

    def ModifyProduct(self, Id: str, producto: str, precio: str):
        cur = self.cnn.cursor()
        sqlSentence = '''UPDATE producttest SET Producto='{}',Precio='{}' WHERE ID ={} '''.format(producto, precio, Id)
        cur.execute(sqlSentence)
        self.cnn.commit()
        cur.close()
        #print("Exito")



