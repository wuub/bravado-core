# -*- coding: utf-8 -*-
import copy
import pytest

from bravado_core.exception import SwaggerMappingError
from bravado_core.spec import Spec
from bravado_core.unmarshal import unmarshal_schema_object


def test_use_models_true(petstore_dict):
    petstore_spec = Spec.from_dict(petstore_dict, config={'use_models': True})
    Category = petstore_spec.definitions['Category']
    category_spec = petstore_spec.spec_dict['definitions']['Category']

    result = unmarshal_schema_object(
        petstore_spec,
        category_spec,
        {'id': 200, 'name': 'short-hair'})

    assert isinstance(result, Category)


def test_use_models_false(petstore_dict):
    petstore_spec = Spec.from_dict(petstore_dict, config={'use_models': False})
    category_spec = petstore_spec.spec_dict['definitions']['Category']

    result = unmarshal_schema_object(
        petstore_spec,
        category_spec,
        {'id': 200, 'name': 'short-hair'})

    assert isinstance(result, dict)


def test_bad_object_spec(petstore_dict):
    petstore_spec = Spec.from_dict(petstore_dict, config={'use_models': False})
    category_spec = copy.deepcopy(
        petstore_spec.spec_dict['definitions']['Category']
    )
    # Type is a required field for objects.
    category_spec['properties']['id'].pop('type')

    with pytest.raises(SwaggerMappingError):
        unmarshal_schema_object(
            petstore_spec,
            category_spec,
            {'id': 200, 'name': 'short-hair'})
