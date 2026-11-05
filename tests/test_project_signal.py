import unittest
from datetime import date
from project_signal import evaluate
class Tests(unittest.TestCase):
    def test_score(self):
        self.assertEqual(evaluate([{"status":"done"},{"status":"todo"}])["score"],50)
    def test_overdue(self):
        result=evaluate([{"status":"todo","due":"2026-01-01"}],date(2026,2,1))
        self.assertEqual(result["overdue"],1)
    def test_completed_not_overdue(self):
        result=evaluate([{"status":"done","due":"2026-01-01"}],date(2026,2,1))
        self.assertEqual(result["overdue"],0)
    def test_blocked(self):
        self.assertEqual(evaluate([{"status":"blocked"}])["blocked"],1)
    def test_bad_state(self):
        with self.assertRaises(ValueError): evaluate([{"status":"maybe"}])
if __name__=="__main__": unittest.main()
