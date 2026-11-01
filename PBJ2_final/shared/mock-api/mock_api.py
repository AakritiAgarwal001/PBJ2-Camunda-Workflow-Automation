#!/usr/bin/env python3
"""Synthetic mock APIs for the PBJ-2 Camunda 8 workflows. No real payment or patient data."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json, time

HOST, PORT = "127.0.0.1", 8081

class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "UP", "service": "pbj2-synthetic-mock-api"})
        else:
            self._send(404, {"error": "not_found", "path": self.path})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._send(400, {"error": "invalid_json"})
            return

        # All services use the same deliberate service-failure toggle. Simulated timeout
        # is slow enough to exceed the connector read timeout configured in the BPMN.
        if data.get("simulateTimeout") is True:
            time.sleep(25)
            self._send(504, {"error": "simulated_timeout", "message": "Synthetic timeout for incident/recovery testing."})
            return
        if data.get("simulateFailure") is True:
            self._send(503, {"error": "simulated_service_failure", "message": "Synthetic 503. Set simulateFailure=false and retry the connector job."})
            return

        if self.path == "/api/credit-assessment":
            try:
                score = int(data.get("creditScore", 700))
            except (ValueError, TypeError):
                self._send(400, {"error": "invalid_credit_score"})
                return
            if not 300 <= score <= 900:
                self._send(400, {"error": "credit_score_out_of_range", "expected": "300..900"})
                return
            band = "LOW" if score >= 750 else ("MEDIUM" if score >= 600 else "HIGH")
            self._send(200, {"creditScore": score, "riskBand": band, "assessmentStatus": "SUCCESS", "assessmentReference": "SYN-CREDIT-001"})
            return

        if self.path == "/api/payments/charge":
            token = data.get("paymentToken", "")
            declined = token == "tok_test_declined" or data.get("forceDecline") is True
            self._send(200, {"paymentStatus": "DECLINED" if declined else "APPROVED", "transactionRef": "SYN-TXN-001", "amount": data.get("amount"), "currency": "INR"})
            return

        if self.path == "/api/appointments/check":
            no_slots = data.get("forceNoSlots") is True
            slots = [] if no_slots else ["09:00", "11:30", "14:00"]
            self._send(200, {"available": not no_slots, "slots": slots, "bookingStatus": "AVAILABLE" if slots else "NO_SLOTS", "scheduleReference": "SYN-SCHED-001"})
            return

        if self.path == "/api/appointments/book":
            slot = data.get("selectedSlot")
            valid_slots = {"09:00", "11:30", "14:00"}
            if slot not in valid_slots:
                self._send(409, {"bookingStatus": "UNAVAILABLE", "message": "Selected slot is not in the synthetic slot list."})
                return
            self._send(200, {"bookingStatus": "BOOKED", "bookingReference": "SYN-BOOK-001", "selectedSlot": slot})
            return

        self._send(404, {"error": "not_found", "path": self.path})

    def log_message(self, fmt, *args):
        print("[mock-api] " + fmt % args)

if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"PBJ-2 synthetic mock APIs listening on http://{HOST}:{PORT}")
    print("POST endpoints: /api/credit-assessment, /api/payments/charge, /api/appointments/check, /api/appointments/book")
    print("GET /health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping mock APIs...")
        server.server_close()
