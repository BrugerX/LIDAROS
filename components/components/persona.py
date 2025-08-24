import json
from argparse import ArgumentTypeError
from collections import deque
from enum import Enum


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

        if(type_tree is []):
            raise ValueError(f"Type tree is empty - {self.type}")

        if(any(type_leaf is "" for type_leaf in type_tree)):
            raise ValueError(f"A type_leaf is empty implying a \\ without a type name - {self.type}")

        if(self.type[-1] == "\\"):
            raise ValueError(f"Types are not allowed to end on \\ - {self.type}")

    def validatePersona(self):
        self._validateType()


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
            if not self._check_descriptor(crit["descriptor"], pers):
                return False

        if "capabilities" in crit:
            if not self._check_capabilities(crit["capabilities"], pers):
                return False

        return True

    def _parse_op(self, rule):
        #Gets the operator from a criteria rule
        operator, crit_value = next(iter(rule.items()))
        if isinstance(operator, CriteriaOperator):
            operator = operator.value
        return operator, crit_value

    def _check_descriptor(self, desc_criteria, pers: Persona):
        desc_persona = pers.descriptor
        for field_name, rule in desc_criteria.items():
            operator, crit_value = self._parse_op(rule)

            #Filter based off of operator type

            #subset check: If not all elements of the crit_value are contained in the persona_value it returns false
            if operator == "in":

                if field_name != "type":
                    persona_value = desc_persona[field_name]

                    if not isinstance(crit_value, (list, tuple, set)):
                        crit_value = [crit_value]

                    if not all(val in persona_value for val in crit_value):
                        return False

                else:
                    type_tree = pers.getTypeTree()
                    crit_iter = crit_value if isinstance(crit_value, (list, tuple, set)) else [crit_value]
                    if not all(val in type_tree for val in crit_iter):
                        return False


            elif operator == "eq":
                persona_value = desc_persona[field_name]
                if crit_value != persona_value:
                    return False
            else:
                raise ValueError(f"Unsupported operator for critical match: {operator}")

        return True

    def _check_capabilities(self, cap_criteria, pers: Persona):
        cap_names = set(pers.capabilities.keys())

        # Accept shorthand like {"in": "setPower"} or {"in": ["setPower","turnOn"]}
        # and also enum keys CriteriaOperator.IN / EQ
        def is_op_dict(d):
            return isinstance(d, dict) and any(
                k in d for k in ("in", "eq", CriteriaOperator.IN, CriteriaOperator.EQ)
            )

        if is_op_dict(cap_criteria):
            operator, crit_value = self._parse_op(cap_criteria)
            # normalize to a set of required names
            if isinstance(crit_value, (list, tuple, set)):
                required = set(crit_value)
            else:
                required = {crit_value}

            if operator == "in":
                # require all listed capability names to exist
                return required.issubset(cap_names)

            elif operator == "eq":
                # eq with one value => that capability must exist
                # eq with multiple values => EXACT match to that set
                return (required <= cap_names) if len(required) == 1 else (required == cap_names)

            else:
                raise ValueError(f"Unsupported operator: {operator}")

        # Fallback: legacy per-capability shape (kept minimal, still name-only)
        # e.g. {"check": {"in": ["setPower","turnOn"]}}
        for _, rule in cap_criteria.items():
            operator, crit_value = self._parse_op(rule)
            values = {crit_value} if not isinstance(crit_value, (list, tuple, set)) else set(crit_value)

            if operator == "in":
                if not values.issubset(cap_names):
                    return False
            elif operator == "eq":
                if len(values) == 1:
                    if not values.issubset(cap_names):
                        return False
                else:
                    if values != cap_names:
                        return False
            else:
                raise ValueError(f"Unsupported operator: {operator}")

        return True
