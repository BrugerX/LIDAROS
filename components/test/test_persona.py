import unittest
from components.components.persona import Persona, Criteria

class TestPersona(unittest.TestCase):
    def test_persona_doubleslash(self):
        doubles_slash_path = r"D:\LIDAROS\interfaces\profiles\test\testpersona_persona_type_doubleslash.json"
        with self.assertRaises(ValueError) as err:
            Persona(doubles_slash_path)
        self.assertIn("A type_leaf is empty", str(err.exception))

    def test_persona_endslash(self):
        end_slash_path = r"D:\LIDAROS\interfaces\profiles\test\testpersona_persona_type_endslash.json"
        with self.assertRaises(ValueError) as err:
            Persona(end_slash_path)
        msg = str(err.exception)
        self.assertTrue(("end on slash" in msg) or ("A type_leaf is empty" in msg))

    def test_persona_empty(self):
        empty_type_path = r"D:\LIDAROS\interfaces\profiles\test\testpersona_persona_type_empty.json"
        with self.assertRaises(ValueError) as err:
            Persona(empty_type_path)
        self.assertIn("empty", str(err.exception))

    def test_pass(self):
        correct_persona = r"D:\LIDAROS\interfaces\profiles\test\testpersona_persona.json"
        Persona(correct_persona)
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
