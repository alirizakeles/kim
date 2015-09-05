# kim/pipelines/nested.py
# Copyright (C) 2014-2015 the Kim authors and contributors
# <see AUTHORS file>
#
# This module is part of Kim and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from .base import (Input, Output, marshal_input_pipe, marshal_output_pipe,
                   serialize_input_pipe, serialize_output_pipe)


def marshal_nested(field, data):
    """Marshal data using the nested mapper defined on this field.
    """

    nested_mapper = field.get_mapper(data=data)
    return nested_mapper.marshal(role=field.opts.role)


def serialize_nested(field, data):
    """Serialize data using the nested mapper defined on this field.
    """

    nested_mapper = field.get_mapper(obj=data)
    return nested_mapper.serialize(role=field.opts.role)


def call_getter(field, data):
    """
    TODO add docstring
    """
    if field.opts.getter:
        result = field.opts.getter(field, data)
        if result is None:
            raise field.invalid(error_type='not_found')
        else:
            return result
    else:
        return data


class NestedInput(Input):

    input_pipes = marshal_input_pipe + [
        call_getter
    ]
    process_pipes = [
        marshal_nested
    ]
    output_pipes = marshal_output_pipe


class NestedOutput(Output):

    input_pipes = serialize_input_pipe
    process_pipes = [
        serialize_nested
    ]
    output_pipes = serialize_output_pipe