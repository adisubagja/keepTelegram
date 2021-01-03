import os
import requests
import unittest

from bot import dbWorker


class Parent:
    """Parent class with need variables"""
    path = './database.db'
    token = os.getenv('TELEGRAM_TOKEN')
    url = f'https://api.telegram.org/bot{token}/'
    ok_status_code = 200
    bot_name = 'Telegram Keep'


class DBTest1(unittest.TestCase, Parent):
    """First class for testing work with database"""

    def test_create(self):
        """Test creation of database"""
        self.assertTrue(dbWorker.create_db(self.path))
        self.assertFalse(dbWorker.create_db(self.path))

    def test_conn(self):
        """Test connection to database"""
        self.assertIsNotNone(dbWorker.connect(self.path))


class DBTest2(unittest.TestCase, Parent):
    """First class for testing work with database"""

    def test_add(self):
        """Test adding data to database"""
        conn = dbWorker.connect(self.path)
        cursor = conn.cursor()
        data = ['test_id', 'test_header', 'test_text', 1, 'test_time']
        self.assertTrue(dbWorker.add_note(conn, cursor, data))

    def test_get(self):
        """Test getting data from database"""
        conn = dbWorker.connect(self.path)
        cursor = conn.cursor()
        data = 'test_id'
        self.assertIsNotNone(dbWorker.get_notes(cursor, data))
        self.assertListEqual(dbWorker.get_notes(cursor, data),
                             [('test_id', 'test_header', 'test_text', 1, 'test_time')])
        self.assertListEqual(dbWorker.get_notes(cursor, ''), [])


class TelegramTest(unittest.TestCase, Parent):
    def setUp(self):
        self.getMe = requests.get(self.url + 'getMe')

    def test_conn(self):
        self.assertEqual(self.getMe.status_code, self.ok_status_code)

    def test_fields(self):
        self.assertTrue(self.getMe.json()["ok"])
        self.assertTrue(self.getMe.json()["result"]["is_bot"])
        self.assertFalse(self.getMe.json()["result"]["can_read_all_group_messages"])
        self.assertFalse(self.getMe.json()["result"]["supports_inline_queries"])
        self.assertEqual(self.getMe.json()["result"]["first_name"], self.bot_name)
