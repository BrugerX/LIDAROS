import json
from argparse import ArgumentTypeError
from collections import deque
from enum import Enum
import copy


class Persona:

    def __init__(self,persona_path : str):

        if not(persona_path.endswith(".json")):
            raise ArgumentTypeError(f"The persona class can only load JSON files, you tried to load {persona_path}")

        with open(persona_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.descriptor = self.data["descriptor"]
        self.capabilities = self.data["capabilities"]
        self.type = self.descriptor["type"]
        self.id = self.descriptor["id"]

        self.validatePersona()

    def getID(self):
        return self.id

    #Get all the types of this and previous generations
    def getTypeTree(self) -> list:
        return self.type.split("/")

    def _validateType(self):
        type_tree = self.getTypeTree()

        if(type_tree == []):
            raise ValueError(f"Type tree is empty - {self.type}")

        if(any(type_leaf is "" for type_leaf in type_tree)):
            raise ValueError(f"A type_leaf is empty implying a slash without a type name - {self.type}")

        if(self.type[-1] == "\\"):
            raise ValueError(f"Types are not allowed to end on slash - {self.type}")

    def validatePersona(self):
        self._validateType()
        #TODO: Add tests for the capabilities

    def getDescriptor(self):
        """
        :return: Copy of descriptor
        """
        return copy.copy(self.descriptor)

    def getCapabilities(self):
        """
        :return: Copy of capabilities
        """
        return copy.copy(self.capabilities)


    #CHATGPT Generated Code - Works as expected!
    def __repr__(self):
        # Extract descriptor info
        desc = self.data.get("descriptor", {})
        capabilities = self.data.get("capabilities", {})

        # Table header
        lines = []
        lines.append(f"Persona for: {self.id}")
        lines.append("=" * 60)

        # Descriptor section
        lines.append("Descriptor:")
        for key, value in desc.items():
            lines.append(f"  {key:15} : {value}")

        # Capabilities section
        lines.append("\nCapabilities:")
        for name, details in capabilities.items():
            # If capability is a dict, flatten it nicely
            if isinstance(details, dict):
                lines.append(f"  {name:15} :")
                for k, v in details.items():
                    lines.append(f"    {k:13} -> {v}")
            else:
                lines.append(f"  {name:15} : {details}")

        return "\n".join(lines)

class CriteriaOperator(Enum):
    EQ = "eq"
    IN = "in"

class Criteria:

    def __init__(self, criteria_dict):
        self.criteria_dict = criteria_dict

    def checkPersona(self, pers: Persona):
        crit = self.criteria_dict


        #Both checks return a truth value - if either of them are false, the total check fails
        if "descriptor" in crit:
            if not self.checkDescriptor(crit["descriptor"], pers):
                return False

        if "capabilities" in crit:
            if not self.checkCapabilities(crit["capabilities"], pers):
                return False

        return True

    def _parseOperator(self, rule):
        #Ensures that it doesn't matter whether we use string or Enum
        operator, crit_value = next(iter(rule.items()))
        if isinstance(operator, str):
            operator = CriteriaOperator(operator)
        return operator, crit_value

    def checkDescriptor(self, desc_criteria, pers: Persona):
        desc_persona = pers.getDescriptor()

        for field_name, rule in desc_criteria.items():
            operator, crit_value = self._parseOperator(rule)

            #Filter based off of operator type

            #subset check: If not all elements of the crit_value are contained in the persona_value it returns false
            if operator == CriteriaOperator.IN:

                if field_name != "type":
                    persona_value = desc_persona[field_name]

                    if not isinstance(crit_value, (list, tuple, set)):
                        crit_value = [crit_value]

                    if not all(val in persona_value for val in crit_value):
                        return False

                else:
                    type_tree = pers.getTypeTree()
                    #Turn it into a singleton
                    crit_iter = crit_value if isinstance(crit_value, (list, tuple, set)) else [crit_value]
                    if not all(val in type_tree for val in crit_iter):
                        return False


            elif operator == CriteriaOperator.EQ:
                persona_value = pers.getTypeTree()

                if crit_value != persona_value:
                    return False
            else:
                raise ValueError(f"Unsupported operator for critical match: {operator}")

        return True

    def checkCapabilities(self,cap_criteria, pers: Persona):
        """
        :param cap_criteria: The criteria by which we should filter - in v0 we only allow for filtering based off of the names of the criteria.
        :return:
        """
        cap_pers = pers.getCapabilities()
        cap_names = list(cap_pers)

        for op_key,crit_cap_names in cap_criteria.items():
            operator, _ = self._parseOperator({op_key: crit_cap_names})

            if operator == CriteriaOperator.IN:

                if not all(name in cap_names for name in crit_cap_names):
                    return False

            elif operator == CriteriaOperator.EQ:

                if not crit_cap_names == cap_names:
                    return False

            else:

                raise ValueError(f"Unsupported operator for criterion match: {operator}")

        return True
