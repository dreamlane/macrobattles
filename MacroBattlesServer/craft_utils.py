## craft_utils.py
import logging
import operator
import string

def getAttributeValue(resource_templates, formula):
  """
    @param resources A dictionary with each of the required resource templates,
                     where the key is the resource type key, and the value is
                     the template.
    @param formula An AttributeFormula with the properties and formula string.
                   see constants_equipment.py for details.
    @returns A floating point attribute value.
  """
  # Replace all of the placeholders in the formula.
  formula_string = formula.formula
  for placeholder, resource_property in formula.properties.iteritems():
    type_key, property_key = resource_property
    resource_template = resource_templates[type_key]
    # Python's getattr lets us get the property of a class by string.
    # This is equivalent to doing something like resource_template.hardness if
    # the property_key is 'hardness'
    property_value = operator.attrgetter(property_key)(resource_template)
    formula_string = string.replace(formula_string, placeholder, str(property_value))

  # Now that we've replaced all of the placeholders with property values, we can
  # evaluate the formula to get the attribute value.
  return eval(formula_string)
