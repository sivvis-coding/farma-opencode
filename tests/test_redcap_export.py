import importlib.util
import unittest
from pathlib import Path
from urllib.parse import parse_qs

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


if __name__ == "__main__":
    unittest.main()
