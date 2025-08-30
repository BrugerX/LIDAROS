import json
from argparse import ArgumentTypeError
from collections import deque
from enum import Enum
import copy

class Type:


    def __init__(self,type_data):

        """
        :param type_data: Type string or type tree.
        """

        if(isinstance(type_data,list)):
            self._type_tree = type_data
            self._type_str = self._createTypeString()

        elif(isinstance(type_data,str)):
            self._type_str = type_data
            self._type_tree = self._createTypeTree()

        self._validateType()

    def _createTypeTree(self):
        return self.type_str.split("/")

    def _createTypeString(self):
        return "/".join(self._type_tree)

    @property
    def type_str(self):
        return copy.copy(self._type_str)

    @property
    def type_tree(self):
        return copy.copy(self._type_tree)

    def __eq__(self, other):
        flag = self.type_tree == other.type_tree
        return flag

    def _validateType(self):

        if(self.type_tree == []):
            raise ValueError(f"Type tree is empty - {self.type_tree}")

        if(any(type_leaf is "" for type_leaf in self.type_tree)):
            raise ValueError(f"A type_leaf is empty implying a slash without a type name - {self.type_str} \t {self.type_tree}")

        if(self.type_str[-1] == "\\"):
            raise ValueError(f"Types are not allowed to end on slash - {self.type_str}")




class Persona:

    """
    Immutable object - Python implementation of persona (see profiles in docs)
    """

    def __init__(self,persona_path : str):

        if not(persona_path.endswith(".json")):
            raise ArgumentTypeError(f"The persona class can only load JSON files, you tried to load {persona_path}")

        with open(persona_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.descriptor = self.data["descriptor"]
        self.descriptor["type"] = Type(self.descriptor["type"])
        self.capabilities = self.data["capabilities"]
        self.type = self.descriptor["type"]
        self.id = self.descriptor["id"]

        self._validatePersona()

    def getID(self):
        return copy.copy(self.id)

    def getTypeString(self):
        return self.type.type_str

    # Get all the types of this and previous generations
    def getTypeTree(self) -> list:
        return self.type.type_tree

    def _validateDescriptor(self):
        #We don't allow dictionaries in V=
        if False:
            for (key,variable) in self.descriptor:
                if(type(variable) == dict):
                    raise ValueError("Dictionaries are not as a part of a descriptor in the current iteration of LIROS")

    def _validatePersona(self):
        self._validateDescriptor()
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

    """
    Wrapper to use the check directly on component rather than persona level.
    """
    def checkComponent(self,comp):
        pers = comp.getPersona()
        return self. checkPersona(pers)

    def checkPersona(self, pers: Persona):
        """
        :param pers: The persona to be checked according to this criteria.
        :return: True if none of the sub-checks return false.
        This also means, that an empty criteria will always return true.
        """
        crit = self.criteria_dict

        #TODO: Decide if you should add a typo checker

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

    def _iteralize(self,obj):
        if isinstance(obj, (list, tuple,str)):
            return obj
        elif isinstance(obj, (dict)):
            #By using list we match the formal definition
            # + We don't get a runtime error if the underlying dict changes :)
            return list(obj.items())
        elif isinstance(obj,Type):
            return obj.type_tree
        #Primitives
        elif isinstance(obj, (bool, str, int, float)):
            return [obj]
        else:
            raise ValueError(f"Cannot iteralize object {obj} of type {type(obj)}")

    def _containsSublist(a, b):
        n, m = len(a), len(b)
        return n == 0 or any(
            all(b[i + j] == a[j] for j in range(n))
            for i in range(m - n + 1)
        )

    """
    iter(a) is a member of iter(b)^sup
    
    Where sup requires knowledge of the type of x
    """

    def _containsSuper(self, a, b, x):
        if(isinstance(x,(str,Type))):
            if isinstance(a, str) and isinstance(b, str):
                #Substring search is ordered
                return a in b

            n = len(a)
            #We sadly have to do a O(m*n) check
            return n == 0 or any(b[i:i + n] == a for i in range(len(b) - n + 1))
        else:
            return all(val in b for val in a)

    def checkDescriptor(self,desc_criteria,pers:Persona):
        desc_pers = pers.getDescriptor()

        for key_crd,rule in desc_criteria.items():
            # We check if the key exists
            variable_D = desc_pers.get(key_crd,None)

            #There doesn't exist such an item in the persona's descriptor dict
            if(variable_D is None):
                return False

            #parse operator ensures compatibility between using CritOperator class and a string for operators
            operator,variable_crd = self._parseOperator(rule)

            if(operator == CriteriaOperator.IN):
                variable_crd_iter = self._iteralize(variable_crd)
                variable_D_iter = self._iteralize(variable_D)
                if not self._containsSuper(variable_crd_iter, variable_D_iter, variable_D):
                    return False

            elif(operator == CriteriaOperator.EQ):
                if not variable_D == variable_crd:
                    return False

        return True

    """
    
    OUTDATED: USED TO SHOW HOW C00L THE NEW METHOD IS AFTER DOING THE FORMAL DEFINITIONS
    
    def checkDescriptor(self, desc_criteria, pers: Persona):
        desc_persona = pers.getDescriptor()

        for key_crd, rule in desc_criteria.items():
            operator, variable_crd = self._parseOperator(rule)

            #Filter based off of operator type

            #subset check: If not all elements of the crit_value are contained in the persona_value it returns false
            if operator == CriteriaOperator.IN:

                if key_crd != "type":
                    persona_value = desc_persona[key_crd]

                    if not isinstance(variable_crd, (list, tuple, set)):
                        crit_value = [variable_crd]

                    if not all(val in persona_value for val in variable_crd):
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
        
        """

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
