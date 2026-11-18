"""Synthetic DOCX round trip; does not claim full Word-feature preservation."""
import hashlib
import tempfile
import unittest
from pathlib import Path

from docx import Document


class SyntheticWordTests(unittest.TestCase):
    def test_copy_preserves_original_numbers_and_table(self):
        with tempfile.TemporaryDirectory() as directory:
            original = Path(directory) / "original.docx"
            revised = Path(directory) / "revision.docx"
            doc = Document()
            doc.add_paragraph("La muestra incluyó 120 personas y 15 eventos.")
            table = doc.add_table(rows=1, cols=2)
            table.cell(0, 0).text = "Eventos"
            table.cell(0, 1).text = "15"
            doc.save(original)
            before = hashlib.sha256(original.read_bytes()).hexdigest()
            copy = Document(original)
            copy.paragraphs[0].text = "La muestra comprendió 120 personas y 15 eventos."
            copy.save(revised)
            self.assertEqual(before, hashlib.sha256(original.read_bytes()).hexdigest())
            reopened = Document(revised)
            self.assertIn("120", reopened.paragraphs[0].text)
            self.assertIn("15", reopened.paragraphs[0].text)
            self.assertEqual(reopened.tables[0].cell(0, 1).text, "15")


if __name__ == "__main__":
    unittest.main()
