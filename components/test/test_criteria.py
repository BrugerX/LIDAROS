import copy
import unittest
from components.components.persona import Persona, Criteria, CriteriaOperator,Type

class MyTestCase_Operators(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_pers = Persona(r"D:\LIDAROS\interfaces\profiles\test\testpersona_persona.json")

    """
    We show that "eq" operator only works if the value for the criterion is equal to the persona's
    """
    def test_eq_type_works(self):
        #The criteria is a subset of the persona
        criteria_subset = {"descriptor": {"type": {"eq":Type("base/device")}}}
        self.assertFalse(Criteria(criteria_subset).checkPersona(self.test_pers))

        #The criteria is equivalent to the persona
        criteria_equiv = {"descriptor": {"type": {"eq": Type('base/device/test')}}}
        self.assertTrue(Criteria(criteria_equiv).checkPersona(self.test_pers),f"{self.test_pers.getTypeTree()}")

        #The criteria is different from the persona
        criteria_wrong = {"descriptor":{"type":{"eq":Type("base/laser")}}}
        self.assertFalse(Criteria(criteria_wrong).checkPersona(self.test_pers))

    """
    We show that the order of sub-types matters for eq
    """
    def test_eq_order_sensisitive(self):
        #The criteria is equivalent to the persona
        criteria_equiv = {"descriptor":
                              {"type": {"eq": Type('base/device/test')},"dummy2_list":{"in":[]}}}
        self.assertTrue(Criteria(criteria_equiv).checkPersona(self.test_pers),f"{self.test_pers.getTypeTree()}")

        #Wrong order
        criteria_arrangement = {"descriptor": {"type": {"eq": Type('device/test/base')}}}

        self.assertEqual(set(criteria_equiv["descriptor"]["type"]["eq"].type_tree),set(criteria_arrangement["descriptor"]["type"]["eq"].type_tree))
        #But the ordering is wrong for criteria_arrangement
        self.assertFalse(Criteria(criteria_arrangement).checkPersona(self.test_pers),f"{self.test_pers.getTypeTree()}")

    """
    We show that "in" works if the value for criterion is a subset of the persona's
    """
    def test_in_type_works(self):
        #The criteria is a subset of the persona's
        criteria_subset = {"descriptor": {"type": {"in": Type("base")}}}
        self.assertTrue(Criteria(criteria_subset).checkPersona(self.test_pers))


        #The criteria is equivalent to the persona's
        criteria_equiv = {"descriptor": {"type": {"in": Type("base/device/test")}}}
        self.assertTrue(Criteria(criteria_equiv).checkPersona(self.test_pers))

        #Should return wrong
        criteria_wrong = {"descriptor":{"type":{"in":Type("base/laser")}}}
        self.assertFalse(Criteria(criteria_wrong).checkPersona(self.test_pers))

    """
    We show that the "in" operator is insensitive with regards to the value of the criterion if it has the right type
    That is to say "in" is a set operator for list,value and dict.
    """
    def test_in_order_insensitive(self):
        desc = self.__class__.test_pers.getDescriptor()
        subset = desc["dummy2_list"][:3]
        criteria_a = {"descriptor": {"dummy2_list": {"in": subset}}}
        criteria_b = {"descriptor": {"dummy2_list": {"in": list(reversed(subset))}}}
        self.assertTrue(Criteria(criteria_a).checkPersona(self.__class__.test_pers))
        self.assertTrue(Criteria(criteria_b).checkPersona(self.__class__.test_pers))

    """
    We show that "in" is order sensitive for strings as well as types.
    """
    def test_in_order_sensitive(self):
        #First we do it for type
        type_tree_pers = self.__class__.test_pers.getTypeTree()
        sub_tree = type_tree_pers[:2]
        sub_tree_shuffled = list(reversed(sub_tree))
        type_shuffled = Type(sub_tree_shuffled)
        type_sub =  Type(sub_tree)

        crit_shuffled = Criteria({"descriptor": {"type": {"in": type_shuffled}}})
        crit_true = Criteria({"descriptor": {"type": {"in": type_sub}}})
        print(type_shuffled)

        self.assertFalse(crit_shuffled.checkPersona(self.__class__.test_pers))
        self.assertTrue(crit_true.checkPersona(self.__class__.test_pers))

    """
    We show that the "eq" operator differentiates between different datatypes
    """
    def test_eq_cares_about_datatype(self):
        desc = self.__class__.test_pers.getDescriptor()
        wrong_type = [str(x) for x in desc["dummy2_list"]]
        criteria = {"descriptor": {"dummy2_list": {"eq": wrong_type}}}
        self.assertFalse(Criteria(criteria).checkPersona(self.__class__.test_pers))


    """
    We show that multiple "in" operators can be put together in the same criteria
    """
    def test_multiple_in_operators(self):
        desc = self.__class__.test_pers.getDescriptor()
        subset = desc["dummy2_list"][:2]
        criteria = {
            "descriptor": {
                "dummy2_list": {"in": subset},
                #And that in can be used with substrings
                "dummy3": {"in": ["CAE", "AR"]}
            }
        }
        self.assertTrue(Criteria(criteria).checkPersona(self.__class__.test_pers))


    """
    We show that type criteria with "in" operators can be strung together independently.
    """
    def test_multiple_in_operators_with_type(self):
        desc = self.__class__.test_pers.getDescriptor()
        subset = desc["dummy2_list"][:2]
        crit_type = Type("base/device/test")
        criteria = {
            "descriptor": {
                "dummy2_list": {"in": subset},
                "type": {"in": crit_type},
            }
        }

        print(crit_type.type_tree)

        print(self.__class__.test_pers.getTypeTree())

        self.assertTrue(Criteria(criteria).checkPersona(self.__class__.test_pers))


    """
    We test that our criteria is agnostic towards whether we use the enum class or its value.
    """
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
