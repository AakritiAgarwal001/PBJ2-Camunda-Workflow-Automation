import json
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mock_api import Handler

class MockApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(timeout=2)

    def post(self, path, body):
        req=Request(self.base+path,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        try:
            with urlopen(req,timeout=3) as response: return response.status,json.loads(response.read())
        except HTTPError as e: return e.code,json.loads(e.read())

    def test_credit_approval_response(self):
        status, body=self.post("/api/credit-assessment",{"creditScore":760})
        self.assertEqual(status,200); self.assertEqual(body["creditScore"],760)

    def test_credit_failure_can_be_simulated(self):
        status, body=self.post("/api/credit-assessment",{"simulateFailure":True})
        self.assertEqual(status,503); self.assertEqual(body["error"],"simulated_service_failure")

    def test_payment_approved_and_declined(self):
        self.assertEqual(self.post("/api/payments/charge",{"paymentToken":"tok_test_approved"})[1]["paymentStatus"],"APPROVED")
        self.assertEqual(self.post("/api/payments/charge",{"paymentToken":"tok_test_declined"})[1]["paymentStatus"],"DECLINED")

    def test_no_slots(self):
        status,body=self.post("/api/appointments/check",{"forceNoSlots":True})
        self.assertEqual(status,200); self.assertFalse(body["available"]); self.assertEqual(body["slots"],[])


    def test_health_endpoint(self):
        with urlopen(self.base + "/health", timeout=3) as response:
            body = json.loads(response.read())
            self.assertEqual(response.status, 200)
            self.assertEqual(body["status"], "UP")

    def test_payment_failure_can_be_simulated(self):
        status, body = self.post("/api/payments/charge", {"paymentToken": "tok_test_approved", "simulateFailure": True})
        self.assertEqual(status, 503)
        self.assertEqual(body["error"], "simulated_service_failure")

    def test_scheduling_failure_can_be_simulated(self):
        status, body = self.post("/api/appointments/check", {"simulateFailure": True})
        self.assertEqual(status, 503)
        self.assertEqual(body["error"], "simulated_service_failure")

    def test_invalid_appointment_slot_is_rejected(self):
        status, body = self.post("/api/appointments/book", {"selectedSlot": "22:00"})
        self.assertEqual(status, 409)
        self.assertEqual(body["bookingStatus"], "UNAVAILABLE")

    def test_appointment_booked(self):
        status,body=self.post("/api/appointments/book",{"selectedSlot":"09:00"})
        self.assertEqual(status,200); self.assertEqual(body["bookingStatus"],"BOOKED")

if __name__ == "__main__": unittest.main(verbosity=2)
