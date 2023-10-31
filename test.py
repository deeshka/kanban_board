import unittest
from app import app, db, Task

#unit tests to test the functionality of the app
class TestKanbanApp(unittest.TestCase):
    #setting up the test database and the app
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_tasks.sqlite3'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    #tearing down the test database
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    #testing the add task functionality
    def test_add_task(self):
        with app.app_context():
            response = self.app.post('/add', data=dict(title='Test task'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            task = Task.query.filter_by(title='Test task').first()
            self.assertIsNotNone(task)
            self.assertFalse(task.complete)
            self.assertFalse(task.inprogress)
            self.assertTrue(task.notstarted)

    #testing the update task functionality
    def test_update_task(self):
        with app.app_context():
            task = Task(title='Test task', complete=False, inprogress=False, notstarted=True)
            db.session.add(task)
            db.session.commit()
            response = self.app.get(f'/update/{task.id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            updated_task = Task.query.get(task.id)
            self.assertFalse(updated_task.notstarted)
            self.assertTrue(updated_task.inprogress)
            self.assertFalse(updated_task.complete)
            response = self.app.get(f'/update/{task.id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            updated_task = Task.query.get(task.id)
            self.assertFalse(updated_task.notstarted)
            self.assertFalse(updated_task.inprogress)
            self.assertTrue(updated_task.complete)

    #testing the delete task functionality
    def test_delete_task(self):
        with app.app_context():
            task = Task(title='Test task', complete=False, inprogress=False, notstarted=True)
            db.session.add(task)
            db.session.commit()
            response = self.app.get(f'/delete/{task.id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            deleted_task = Task.query.get(task.id)
            self.assertIsNone(deleted_task)

#running the tests
if __name__ == '__main__':
    unittest.main()
