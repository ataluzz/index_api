import unittest
import api
import defs
from flask import Flask, abort, render_template, request, send_file

class MyTestCase(unittest.TestCase):
	def setUp(self):
		self.app = api.app.test_client()
		self.app.testing = True

	def test_home(self):
		res = self.app.get('/statsapi')
		self.assertEqual(res.status_code, 200)

	def test_results_for_directory_no_word_or_ext(self):
		sent = {'path':'testfiles/', 'extensions':'', 'word':''}
		res = self.app.post('/result', data=sent)
		self.assertEqual(res.status_code, 200)

	def test_results_for_directory_word_no_ext(self):
		sent = {'path':'testfiles/', 'extensions':'', 'word':'the'}
		res = self.app.post('/result', data=sent)
		self.assertEqual(res.status_code, 200)

	def test_results_for_directory_no_word_ext(self):
		sent = {'path':'testfiles/', 'extensions':'.txt', 'word':''}
		res = self.app.post('/result', data=sent)
		self.assertEqual(res.status_code, 200)

	def test_results_for_directory_word_ext(self):
		sent = {'path':'testfiles/', 'extensions':'', 'word':''}
		res = self.app.post('/result', data=sent)
		self.assertEqual(res.status_code, 200)

	def test_results_for_file(self):
		sent = {'path':'testfiles/second.txt', 'extensions':'', 'word':''}
		res = self.app.post('/result', data=sent)
		self.assertEqual(res.status_code, 200)

	def test_results_for_file_word(self):
		sent = {'path':'testfiles/second.txt', 'extensions':'', 'word':'день'}
		res = self.app.post('/result', data=sent)
		self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
	unittest.main()