import random
import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox,\
    QMessageBox, QTextEdit, QDialog, QTabWidget, QTableWidget, QTableWidgetItem, QHBoxLayout

class YoneticiInfoDialog(QDialog):
    def __init__(self, username, conn):
        super().__init__()
        self.username = username
        self.conn = conn
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Öğrenci Bilgileri - {self.username}")
        self.setGeometry(500, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel(f"Merhaba, {self.username}!")
        self.layout.addWidget(self.label)

        self.student_info_table = QTableWidget()
        self.layout.addWidget(self.student_info_table)

        self.update_button = QPushButton("Bilgileri Güncelle")
        self.layout.addWidget(self.update_button)

        self.deleteAllData_button = QPushButton("Tablo Temizle")
        self.layout.addWidget(self.deleteAllData_button)

        self.randomStudent_button = QPushButton("Random Student")
        self.layout.addWidget(self.randomStudent_button)

        self.update_button.clicked.connect(self.update_student_info)
        self.deleteAllData_button.clicked.connect(self.deleteAllData_student_info)
        self.randomStudent_button.clicked.connect(self.randomData_student_info)

        # Yeni veriler eklemek için metin kutuları
        self.new_data_lineedits = []

        for label in ["talep_Sayisi:", "öğrenci id:", "rasgele belirtilen sayi:"]:
            row_layout = QHBoxLayout()
            row_label = QLabel(label)
            row_layout.addWidget(row_label)
            row_lineedit = QLineEdit()
            row_layout.addWidget(row_lineedit)
            self.new_data_lineedits.append(row_lineedit)
            self.layout.addLayout(row_layout)

        self.setLayout(self.layout)

        # Öğrenci bilgilerini görüntüle
        self.display_student_info()

    def display_student_info(self):
        cursor = self.conn.cursor()
        print("usernameDisplaystudentinfo:",self.username)
        cursor.execute(f"SELECT * FROM ogrenci")
        student_info = cursor.fetchall()
        cursor.close()

        labels = ["Ogrenci_id", "Ad", "gpa", "talep_sayısı", "password","Secilen_Ders_id"]

        self.student_info_table.setRowCount(len(student_info) + 1)
        self.student_info_table.setColumnCount(len(labels) + 1)


        for i, label in enumerate(labels):
            self.student_info_table.setItem(0, i, QTableWidgetItem(label))

        for k, student in enumerate(student_info):
            for j, data in enumerate(student):
                self.student_info_table.setItem(k + 1, j, QTableWidgetItem(str(data)))


    def update_student_info(self):
        # Tablodaki verileri güncelleme işlemi
        updated_data = []


        for row in range(len(self.new_data_lineedits)):
            item = self.new_data_lineedits[row]
            if item:
                updated_data.append(item.text())
                # print(item.text())
            else:
                updated_data.append("")  # Eksik veri yerine boş bir dize ekleyin

        cursor = self.conn.cursor()
        # print(updated_data)
        cursor.execute(f"""
            UPDATE ogrenci SET 
                talep_sayisi = %s
                WHERE ogrenci_id = %s   
        """, tuple((updated_data[0],updated_data[1])))
        self.conn.commit()
        cursor.close()
        self.display_student_info()
        # Güncelleme tamamlandığında bilgi ver
        QMessageBox.information(self, "Bilgiler Güncellendi", "Bilgileriniz güncellendi!")

    def deleteAllData_student_info(self):
        cursor = self.conn.cursor()

        cursor.execute(f"""
            DELETE FROM ogrenci;
        """)
        self.conn.commit()
        cursor.close()
        self.display_student_info()
        # Güncelleme tamamlandığında bilgi ver
        QMessageBox.information(self, "Tablo Güncellendi", "Bilgileriniz silindi!")

    def randomData_student_info(self):
        # Tablodaki verileri güncelleme işlemi
        updated_data = []
        isimler = ["Ahmet", "Mehmet", "Samet", "Taha", "İrfan", "Yunus", "Hasan", "Ali", "Murat", "Fatih","Buğra"]
        # print("Bravo",self.new_data_lineedits[0].text())

        for row in range(int(self.new_data_lineedits[2].text())):
            cursor = self.conn.cursor()
            # print(updated_data)
            cursor.execute(f"""
                                INSERT INTO ogrenci
                                    (first_name,
                                    gpa,
                                    talep_sayisi,
                                    password) VALUES (%s, %s, %s, %s )
                            """, tuple((random.choice(isimler),random.randint(1, 4),1,"123")))
            self.conn.commit()
            cursor.close()
        print(updated_data)

        self.display_student_info()
        # Güncelleme tamamlandığında bilgi ver
        QMessageBox.information(self, "Random Güncellendi", "Random Veri Eklendi!")

class StudentInfoDialog(QDialog):
    def __init__(self, username, conn):
        super().__init__()
        self.username = username
        self.conn = conn
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Öğrenci Bilgileri - {self.username}")
        self.setGeometry(500, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel(f"Merhaba, {self.username}!")
        self.layout.addWidget(self.label)

        self.student_info_table = QTableWidget()
        self.layout.addWidget(self.student_info_table)

        self.label = QLabel("Ders seçin:")
        self.ders_combo = QComboBox()
        self.ders_combo.addItem("YAPAY ZEKA")
        self.ders_combo.addItem("GÖRÜNTÜ İŞLEME")
        self.ders_combo.addItem("KRİPTOGRAFİ")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.ders_combo)
        
        
        self.update_button = QPushButton("SEÇ")
        self.layout.addWidget(self.update_button)

        self.mesagge_button = QPushButton("MESAJLAR")
        self.layout.addWidget(self.mesagge_button)

        self.update_button.clicked.connect(self.update_student_info)
        self.mesagge_button.clicked.connect(self.message_call_student_info)
        # Yeni veriler eklemek için metin kutuları
       
        self.setLayout(self.layout)

        # Öğrenci bilgilerini görüntüle
        
        self.display_student_info()
    

    def update_student_info(self):
        cursor = self.conn.cursor()
        if self.ders_combo.currentText() == "YAPAY ZEKA":
            
            cursor.execute(f"""UPDATE ogrenci SET sectigi_ders_id = 1 WHERE ogrenci_id = {self.username} """)
            self.conn.commit()
            QMessageBox.information(self, "Tablo Güncellendi", "Ders Seçimi Başarılı")
        if self.ders_combo.currentText() == "GÖRÜNTÜ İŞLEME":
            
            cursor.execute(f"""UPDATE ogrenci SET sectigi_ders_id = 2 WHERE ogrenci_id = {self.username} """)
            self.conn.commit()
            QMessageBox.information(self, "Tablo Güncellendi", "Ders Seçimi Başarılı")
        if self.ders_combo.currentText() == "KRİPTOGRAFİ":
            
            cursor.execute(f"""UPDATE ogrenci SET sectigi_ders_id = 3 WHERE ogrenci_id = {self.username} """)
            self.conn.commit()   
            QMessageBox.information(self, "Tablo Güncellendi", "Ders Seçimi Başarılı")
    def message_call_student_info(self):
        
        teacher_info_dialog = MessageBoxInfoSys(self.username,"ogrenci", self.conn)
        teacher_info_dialog.exec_()

    def display_student_info(self):
        cursor = self.conn.cursor()
        
        cursor.execute(f"SELECT first_name, talep_sayisi, sectigi_ders_id FROM ogrenci WHERE ogrenci_id = {self.username}")
        student_info = cursor.fetchall()
        cursor.close()

        labels = ["Ad",  "talep_sayısı", "sectigi_ders_id"]

        self.student_info_table.setRowCount(len(student_info) + 1)
        self.student_info_table.setColumnCount(len(labels) )

        for i, label in enumerate(labels):
            self.student_info_table.setItem(0, i, QTableWidgetItem(label))

        for k, student in enumerate(student_info):
            for j, data in enumerate(student):
                self.student_info_table.setItem(k + 1, j, QTableWidgetItem(str(data)))
        
class TeacherInfoDialog(QDialog):
    def __init__(self, username, conn):
        super().__init__()
        self.username = username
        self.conn = conn
        self.talep_onay_count = 0 
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Öğretmen Bilgileri - {self.username}")
        self.setGeometry(500, 100, 400, 300)
        cursor = self.conn.cursor()
        self.layout = QVBoxLayout()
        cursor.execute(f"SELECT ogretmen_adi, ilgi_alani,kota FROM ogretmen WHERE ogretmen_id ={int(self.username)} ")
        ogretmen = cursor.fetchall()
        self.label = QLabel(f"Merhaba, {ogretmen[0][0]}!")
        self.layout.addWidget(self.label)

        self.label1 = QLabel(f"Ders adı, {ogretmen[0][1]}!")
        self.layout.addWidget(self.label1)

        self.label2 = QLabel(f"Kota, {ogretmen[0][2]}!")
        self.layout.addWidget(self.label2)

        self.student_info_table = QTableWidget()
        self.layout.addWidget(self.student_info_table)
        '''
        print(self.username)
        cursor.execute(f"SELECT * FROM ogrenci WHERE sectigi_ders_id ={int(self.username)} ")
        user = cursor.fetchall()
        '''

        self.message_button = QPushButton("MESAJLAR")
        self.layout.addWidget(self.message_button)

        self.update_button = QPushButton("Kabul et")
        self.layout.addWidget(self.update_button)

        self.talep_onay_button = QPushButton("Talep/Onay")
        self.layout.addWidget(self.talep_onay_button)

        self.ogrenci_listele = QPushButton("Ders Seçmemiş Öğreci Listesi")
        self.layout.addWidget(self.ogrenci_listele)

        self.new_data_lineedits = []

        for label in ["Kabul edilecek ogrenci id:"]:
            row_layout = QHBoxLayout()
            row_label = QLabel(label)
            row_layout.addWidget(row_label)
            row_lineedit = QLineEdit()
            row_layout.addWidget(row_lineedit)
            self.new_data_lineedits.append(row_lineedit)
            self.layout.addLayout(row_layout)
        
        self.setLayout(self.layout)

        self.update_button.clicked.connect(self.update_student_info)
        self.talep_onay_button.clicked.connect(self.talep_onay_student_info)
        self.ogrenci_listele.clicked.connect(self.onaysiz_ogrenci_listesi)
        self.message_button.clicked.connect(self.message_call_student_info)
        self.display_student_info()

    def display_student_info(self):
        cursor = self.conn.cursor()
        print("usernameDisplaystudentinfo:",self.username)
        if self.talep_onay_count % 2 == 0:
            cursor.execute(f"""SELECT * FROM ogrenci WHERE sectigi_ders_id = '{self.username}' AND talep_sayisi != 0 """)
            QMessageBox.information(self, "Talep Tablosuna Geçildi", "Talep Tablosuna Geçildi!")    
        else:
            cursor.execute(f"""SELECT * FROM ogrenci WHERE sectigi_ders_id = '{self.username}' """)
            QMessageBox.information(self, "Onay Tablosuna Geçildi", "Onay Tablosuna Geçildi!")    
        student_info = cursor.fetchall()
        cursor.close()

        labels = ["Ogrenci_id", "Ad", "gpa", "talep_sayısı", "password"]

        self.student_info_table.setRowCount(len(student_info) + 1)
        self.student_info_table.setColumnCount(len(labels) + 1)


        for i, label in enumerate(labels):
            self.student_info_table.setItem(0, i, QTableWidgetItem(label))

        for k, student in enumerate(student_info):
            for j, data in enumerate(student):
                self.student_info_table.setItem(k + 1, j, QTableWidgetItem(str(data)))

    def message_call_student_info(self):
        
        teacher_info_dialog = MessageBoxInfoSys(self.username,"ogretmen", self.conn)
        teacher_info_dialog.exec_()

    def onaysiz_ogrenci_listesi(self):

        cursor = self.conn.cursor() 
        cursor.execute(f"""SELECT * FROM ogrenci WHERE talep_sayisi != 0 AND sectigi_ders_id = '0' """)
        student_info = cursor.fetchall()
        cursor.close()

        labels = ["Ogrenci_id", "Ad", "gpa", "talep_sayısı", "password","Secilen_Ders_id"]

        self.student_info_table.setRowCount(len(student_info) + 1)
        self.student_info_table.setColumnCount(len(labels) + 1)


        for i, label in enumerate(labels):
            self.student_info_table.setItem(0, i, QTableWidgetItem(label))

        for k, student in enumerate(student_info):
            for j, data in enumerate(student):
                self.student_info_table.setItem(k + 1, j, QTableWidgetItem(str(data)))

    def talep_onay_student_info(self):
        self.talep_onay_count += 1
        self.display_student_info()

    def update_student_info(self):
        # Tablodaki verileri güncelleme işlemi
        updated_data = []
        cursor = self.conn.cursor()
        cursor.execute(f"""SELECT talep_sayisi,ogrenci_id FROM ogrenci WHERE sectigi_ders_id = '{self.username}' AND ogrenci_id = {self.new_data_lineedits[0].text()}  """)
        
        user = cursor.fetchall()
        self.conn.commit()
        cursor.execute(f"""SELECT kota FROM ogretmen WHERE ogretmen_id = '{self.username}'  """)
        ogretmen = cursor.fetchall()
        self.conn.commit()
        
        cursor = self.conn.cursor()
        cursor.execute(f"""
            UPDATE ogrenci SET 
                talep_sayisi = %s
                WHERE ogrenci_id = %s
        """, tuple((user[0][0]-1,user[0][1])))
        self.conn.commit()
        cursor.execute(f"""
            UPDATE ogretmen SET 
                kota = %s
                WHERE ogretmen_id = %s
        """, tuple((ogretmen[0][0]-1,self.username)))
        self.label2.setText("kota:"+str(ogretmen[0][0]-1))
        self.label2.update()
        self.conn.commit()
        cursor.close()
        self.display_student_info()
        # Güncelleme tamamlandığında bilgi ver
        QMessageBox.information(self, "Bilgiler Güncellendi", "Bilgileriniz güncellendi!")

    
class MessageBoxInfoSys(QDialog):
    def __init__(self, username,user_role, conn):
        super().__init__()
        self.username = username
        self.user_role = user_role
        self.conn = conn
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Öğrenci Bilgileri - {self.username}")
        self.setGeometry(500, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel(f"Merhaba, {self.username}!")
        self.layout.addWidget(self.label)

        self.student_info_table = QTableWidget()
        self.layout.addWidget(self.student_info_table)
        
        self.update_button = QPushButton("GÖNDER")
        self.layout.addWidget(self.update_button)
        
        self.new_data_lineedits = []
 
        if self.user_role == "ogretmen":
            
            for label in ["ogrenci_id: ", "mesaj: "]:
                row_layout = QHBoxLayout()
                row_label = QLabel(label)
                row_layout.addWidget(row_label)
                row_lineedit = QLineEdit()
                row_layout.addWidget(row_lineedit)
                self.new_data_lineedits.append(row_lineedit)
                self.layout.addLayout(row_layout)
        else :
            for label in ["ogretmen_id: ", "mesaj: "]:
                row_layout = QHBoxLayout()
                row_label = QLabel(label)
                row_layout.addWidget(row_label)
                row_lineedit = QLineEdit()
                row_layout.addWidget(row_lineedit)
                self.new_data_lineedits.append(row_lineedit)
                self.layout.addLayout(row_layout)
        self.update_button.clicked.connect(self.message_process_student_info)
       
        self.setLayout(self.layout)
        self.message_display()

    def message_display(self):

        cursor = self.conn.cursor() 
        if self.user_role == "ogretmen":
            cursor.execute(f"""SELECT * FROM message WHERE ogretmen_id = {self.username}  """)
        else :
            cursor.execute(f"""SELECT * FROM message WHERE ogrenci_id = {self.username}  """)
    
        student_info = cursor.fetchall()
        cursor.close()

        labels = ["Ogretmen_id", "ogrenci_id", "mesaj"]

        self.student_info_table.setRowCount(len(student_info) + 1)
        self.student_info_table.setColumnCount(len(labels) + 1)


        for i, label in enumerate(labels):
            self.student_info_table.setItem(0, i, QTableWidgetItem(label))

        for k, student in enumerate(student_info):
            for j, data in enumerate(student):
                self.student_info_table.setItem(k + 1, j, QTableWidgetItem(str(data)))

    def message_process_student_info(self):
        cursor = self.conn.cursor()

        cursor.execute(f"""
                                    INSERT INTO message
                                        (ogretmen_id,
                                        ogrenci_id,
                                        message
                                        ) VALUES (%s, %s, %s )
        """, tuple((self.username,self.new_data_lineedits[0].text(),self.new_data_lineedits[1].text())))    

        

        self.conn.commit()
        QMessageBox.information(self, "Mesaj Başarılı", "Mesaj gönderme Başarılı!")
        self.message_display()
class UserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Kullanıcı Girişi ve Kaydı")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.username_input)

        self.label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.password_input)

        self.label = QLabel("Rol Seçin:")
        self.role_combo = QComboBox()
        self.role_combo.addItem("Yonetici")
        self.role_combo.addItem("Ogrenci")
        self.role_combo.addItem("Ogretmen")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.role_combo)

        self.login_button = QPushButton("Giriş")
        

        self.layout.addWidget(self.login_button)
        

        self.login_button.clicked.connect(self.login)
        

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

    

        # PostgreSQL veritabanı bağlantısı
        self.conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432"
        )
        self.create_users_table()

    def create_users_table(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dersler (
                ders_id SERIAL ,
                ogretmen_id INTEGER NOT NULL,
                ders_name VARCHAR(20) NOT NULL
            );
        """)
        self.conn.commit()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ogretmen (
                ogretmen_id SERIAL PRIMARY KEY ,
                ogretmen_adi VARCHAR(20),
                ilgi_alani VARCHAR(20)
                
            );
        """)
        self.conn.commit()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS message (
                ogretmen_id INTEGER ,
                ogrenci_id INTEGER,
                message VARCHAR(100)
                
            );
        """)
        self.conn.commit()
        cursor.execute(f"""
                                CREATE TABLE IF NOT EXISTS ogrenci (
                                    ogrenci_id SERIAL PRIMARY KEY,
                                    first_name VARCHAR(50),
                                    gpa VARCHAR(50),
                                    talep_sayisi INTEGER
                                );
                            """)
        self.conn.commit()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS yonetici (
                yonetici_id SERIAL               
            );
        """)
        self.conn.commit()
        cursor.close()

    def create_student_info_tab(self):
        student_tab = QWidget()
        layout = QVBoxLayout()

    

        student_tab.setLayout(layout)
        return student_tab

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()  # Seçilen rolü al

        
        if role == "Yonetici":
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM yonetici WHERE yonetici_id = %s AND password=%s ", (username,"123"))
                user = cursor.fetchone()
                cursor.close()
                if user:
                    yonetici_info_dialog = YoneticiInfoDialog(self.username_input.text(), self.conn)
                    QMessageBox.information(self, "Giriş Başarılı", "Giriş Başarılı!")
                    yonetici_info_dialog.exec_()
                    
                else:
                    QMessageBox.warning(self, "Giriş Başarısız", "Giriş Başarısız!")
        elif role == "Ogrenci":
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM ogrenci WHERE ogrenci_id = %s AND password=%s ", (username,"123"))
                user = cursor.fetchone()
                cursor.close()
                if user:
                    ogrenci_info_dialog = StudentInfoDialog(self.username_input.text(), self.conn)
                    QMessageBox.information(self, "Giriş Başarılı", "Giriş Başarılı!")
                    ogrenci_info_dialog.exec_()
                    
                else:
                    QMessageBox.warning(self, "Giriş Başarısız", "Giriş Başarısız!")
        elif role == "Ogretmen":
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM ogretmen WHERE ogretmen_id = %s AND password=%s", (username,"123"))
                user = cursor.fetchone()
                cursor.close()
                if user:
                    teacher_info_dialog = TeacherInfoDialog(self.username_input.text(), self.conn)
                    QMessageBox.information(self, "Giriş Başarılı", "Giriş Başarılı!")
                    teacher_info_dialog.exec_()
                    
                else:
                    QMessageBox.warning(self, "Giriş Başarısız", "Giriş Başarısız!")
                    

def main():
    app = QApplication(sys.argv)
    window = UserApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
