import importlib.util
import unittest
import io
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from urllib.parse import parse_qs
from unittest.mock import patch

path = Path(__file__).resolve().parents[1] / "tools" / "redcap_export.py"
spec = importlib.util.spec_from_file_location("redcap_export", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RequestTests(unittest.TestCase):
    def test_metadata(self):
        request = module.prepare_request("https://redcap.example/api/", "secret", "metadata", [])
        self.assertEqual(parse_qs(request.data.decode())["content"], ["metadata"])
        self.assertNotIn("secret", request.full_url)

    def test_record_requires_fields(self):
        with self.assertRaises(ValueError):
            module.prepare_request("https://redcap.example/api/", "secret", "record", [])

    def test_fields(self):
        request = module.prepare_request("https://redcap.example/api/", "secret", "record", ["age", "group"])
        self.assertEqual(parse_qs(request.data.decode())["fields[]"], ["age", "group"])

    def test_reject_unsafe_urls(self):
        for url in ["http://redcap.example/api/", "https://user:pass@redcap.example/",
                    "https://redcap.example/api/?token=secret"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                    module.prepare_request(url, "secret", "metadata", [])


class SyntheticExportTests(unittest.TestCase):
    def run_export(self, output, response_type="text/csv"):
        class Response(io.BytesIO):
            headers = {"Content-Type": response_type}

        class Opener:
            def open(self, request, timeout):
                self.request = request
                return Response(b"id,grupo,evento\n1,A,1\n")

        args = ["redcap_export.py", "--url", "https://redcap.example/api/",
                "--tipo", "record", "--campo", "grupo", "--salida", str(output)]
        with patch.object(sys, "argv", args), patch("builtins.input", return_value="SI"), \
             patch.object(module.getpass, "getpass", return_value="synthetic-token"), \
             patch.object(module.urllib.request, "build_opener", return_value=Opener()), \
             redirect_stdout(io.StringIO()) as stdout, redirect_stderr(io.StringIO()) as stderr:
            result = module.main()
        self.assertNotIn("synthetic-token", stdout.getvalue() + stderr.getvalue())
        return result

    def test_synthetic_csv_and_original_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "export.csv"
            self.assertEqual(self.run_export(output), 0)
            before = output.read_bytes()
            self.assertEqual(before, b"id,grupo,evento\n1,A,1\n")
            self.assertEqual(self.run_export(output), 1)
            self.assertEqual(output.read_bytes(), before)

    def test_non_csv_response_removes_partial_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "error.csv"
            self.assertEqual(self.run_export(output, "application/json"), 1)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
