# -*- coding: utf-8 -*-
from django import template


def validate_template_tag_params(bits, arguments_count, keyword_positions):
    '''
        Raises exception if passed params (`bits`) do not match signature.
        Signature is defined by `bits_len` (acceptible number of params) and
        keyword_positions (dictionary with positions in keys and keywords in values,
        for ex. {2:'by', 4:'of', 5:'type', 7:'as'}).
    '''

    if len(bits) != arguments_count+1:
        raise template.TemplateSyntaxError("'%s' tag takes %d arguments" % (bits[0], arguments_count,))

    for pos in keyword_positions:
        value = keyword_positions[pos]
        if bits[pos] != value:
            raise template.TemplateSyntaxError("argument #%d to '%s' tag must be '%s'" % (pos, bits[0], value))
