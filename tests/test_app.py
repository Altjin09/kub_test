# tests/test_app.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

def test_home():
    tester = app.test_client()
    response = tester.get('/', follow_redirects=True)  # redirect дагана
    assert response.status_code == 200
    assert "Нууц үг" in response.data.decode("utf-8")
  # login.html доторх үгсийн нэг байж болно
