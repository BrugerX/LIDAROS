import copy
import unittest
from components.components.persona import Persona, Criteria, CriteriaOperator

class MyTestCase_Operators(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_pers = Persona(r"D:\LIDAROS\interfaces\profiles\test\testpersona_persona.json")

    def test_in_order_insensitive(self):
        desc = self.__class__.test_pers.getDescriptor()
        subset = desc["dummy2_list"][:3]
        criteria_a = {"descriptor": {"dummy2_list": {"in": subset}}}
        criteria_b = {"descriptor": {"dummy2_list": {"in": list(reversed(subset))}}}
        self.assertTrue(Criteria(criteria_a).checkPersona(self.__class__.test_pers))
        self.assertTrue(Criteria(criteria_b).checkPersona(self.__class__.test_pers))

    def test_eq_cares_about_datatype(self):
        desc = self.__class__.test_pers.getDescriptor()
        wrong_type = [str(x) for x in desc["dummy2_list"]]
        criteria = {"descriptor": {"dummy2_list": {"eq": wrong_type}}}
        self.assertFalse(Criteria(criteria).checkPersona(self.__class__.test_pers))

    def test_in_type_works(self):
        criteria = {"descriptor": {"type": {"in": ["base", "device"]}}}
        self.assertTrue(Criteria(criteria).checkPersona(self.__class__.test_pers))

    def test_multiple_in_operators(self):
        desc = self.__class__.test_pers.getDescriptor()
        subset = desc["dummy2_list"][:2]
        criteria = {
            "descriptor": {
                "dummy2_list": {"in": subset},
                "dummy3": {"in": ["CAE", "AR"]}
            }
        }
        self.assertTrue(Criteria(criteria).checkPersona(self.__class__.test_pers))

    def test_multiple_in_operators_with_type(self):
        desc = self.__class__.test_pers.getDescriptor()
        subset = desc["dummy2_list"][:2]
        criteria = {
            "descriptor": {
                "dummy2_list": {"in": subset},
                "type": {"in": ["base", "test"]}
            }
        }
        self.assertTrue(Criteria(criteria).checkPersona(self.__class__.test_pers))


    def test_string_vs_enum_operators(self):
        desc = self.__class__.test_pers.getDescriptor()
        subset = desc["dummy2_list"][:3]

        crit_str_non_type = {"descriptor": {"dummy2_list": {"in": subset}, "dummy3": {"eq": desc["dummy3"]}}}
        crit_enum_non_type = {"descriptor": {"dummy2_list": {CriteriaOperator.IN: subset}, "dummy3": {CriteriaOperator.EQ: desc["dummy3"]}}}

        crit_str_type_in = {"descriptor": {"type": {"in": ["base"]}}}
        crit_enum_type_in = {"descriptor": {"type": {CriteriaOperator.IN: ["base"]}}}

        crit_str_type_eq = {"descriptor": {"type": {"eq": desc["type"]}}}
        crit_enum_type_eq = {"descriptor": {"type": {CriteriaOperator.EQ: desc["type"]}}}

        self.assertTrue(Criteria(crit_str_non_type).checkPersona(self.__class__.test_pers))
        self.assertTrue(Criteria(crit_enum_non_type).checkPersona(self.__class__.test_pers))
        self.assertTrue(Criteria(crit_str_type_in).checkPersona(self.__class__.test_pers))
        self.assertTrue(Criteria(crit_enum_type_in).checkPersona(self.__class__.test_pers))
        self.assertTrue(Criteria(crit_str_type_eq).checkPersona(self.__class__.test_pers))
        self.assertTrue(Criteria(crit_enum_type_eq).checkPersona(self.__class__.test_pers))


if __name__ == '__main__':
    unittest.main()
