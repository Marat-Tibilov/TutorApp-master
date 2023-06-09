from kivy.lang import Builder
from kivymd.uix.card import MDCard

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from objects.widgets.StudentCardContent import *

Builder.load_file("./objects/widgets/StudentCard.kv")

class StudentCard(MDCard): 
    def __init__ (self, cols, **kwargs):
        self.cols = cols
        super(StudentCard, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def on_touch(self, instance): # вызывается при нажатии на урок 
        self.dialog = MDDialog(
            title="Сведения об уроке",
            type="custom",
            radius=[20],
            content_cls=StudentCardContent(self),
            buttons=[
                MDFlatButton(
                    text="Закрыть",
                    on_release=self.close
                ),
                MDFlatButton(
                    text="Удалить",
                    on_release=self.remove
                ),
                MDFlatButton(
                    text="Сохранить изменения",
                    on_release=self.save
                )
            ]
        )
        self.dialog.open()

    def remove(self, instance): # событие удаления 

        with self.app.con().cursor() as cursor:
            sql = """DELETE FROM lessons WHERE id=%s"""
            cursor.execute(sql, (self.cols.get("id")))
        self.parent.parent.parent.parent.update()
        self.dialog.dismiss()
    
    def close(self, instance):
        self.dialog.dismiss()
    
    def save(self, instance): # сохраняет ,когда мы вносим изменения 
        with self.app.con().cursor() as cursor:
            sql = """UPDATE lessons SET date=%s, time=%s, student_id=%s, lesson_type_id=%s, payment_type_id=%s WHERE id=%s"""
            cursor.execute(sql, (str(self.cols.get("date")), str(self.cols.get("time")), self.cols.get("student_id"),
                self.cols.get("lesson_type_id"), self.cols.get("payment_type_id"), self.cols.get("id")))
        self.parent.parent.parent.parent.parent.get_screen("schedule").update_content()
        self.dialog.dismiss()