# -*- coding: utf-8 -*-
# Copyright (C) 2006-2012 Søren Roug, European Environment Agency
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Contributor(s):
#
import re

from TurtleArt.util.odf import namespaces

pattern_color = re.compile(r'#[0-9a-fA-F]{6}')
pattern_vector3D = re.compile(
    r'\([ ]*-?([0-9]+(\.[0-9]*)?|\.[0-9]+)([ ]+-?([0-9]+(\.[0-9]*)?|\.[0-9]+)){2}[ ]*\)')


def make_NCName(arg):
    for c in (':', ' '):
        arg = arg.replace(c, "_%x_" % ord(c))
    return arg


def cnv_anyURI(attribute, arg, element):
    return str(arg)


def cnv_boolean(attribute, arg, element):
    """ XML Schema Part 2: Datatypes Second Edition
        An instance of a datatype that is defined as boolean can have the
        following legal literals {true, false, 1, 0}
    """
    if str(arg).lower() in ("0", "false", "no"):
        return "false"
    if str(arg).lower() in ("1", "true", "yes"):
        return "true"
    raise ValueError("'%s' not allowed as Boolean value for %s" % (
        str(arg), attribute))


# Potentially accept color values


def cnv_color(attribute, arg, element):
    """ A RGB color in conformance with §5.9.11 of [XSL], that is a RGB color in notation “#rrggbb”, where
        rr, gg and bb are 8-bit hexadecimal digits.
    """
    return str(arg)


def cnv_configtype(attribute, arg, element):
    if str(arg) not in ("boolean", "short", "int", "long",
                        "double", "string", "datetime", "base64Binary"):
        raise ValueError("'%s' not allowed" % str(arg))
    return str(arg)


def cnv_data_source_has_labels(attribute, arg, element):
    if str(arg) not in ("none", "row", "column", "both"):
        raise ValueError("'%s' not allowed" % str(arg))
    return str(arg)


# Understand different date formats


def cnv_date(attribute, arg, element):
    """ A dateOrDateTime value is either an [xmlschema-2] date value or an [xmlschema-2] dateTime
        value.
    """
    return str(arg)


def cnv_dateTime(attribute, arg, element):
    """ A dateOrDateTime value is either an [xmlschema-2] date value or an [xmlschema-2] dateTime
        value.
    """
    return str(arg)


def cnv_double(attribute, arg, element):
    return str(arg)


def cnv_duration(attribute, arg, element):
    return str(arg)


def cnv_family(attribute, arg, element):
    """ A style family """
    if str(arg) not in (
            "text",
            "paragraph",
            "section",
            "ruby",
            "table",
            "table-column",
            "table-row",
            "table-cell",
            "graphic",
            "presentation",
            "drawing-page",
            "chart"):
        raise ValueError("'%s' not allowed" % str(arg))
    return str(arg)


def __save_prefix(attribute, arg, element):
    prefix = arg.split(':', 1)[0]
    if prefix == arg:
        return str(arg)
    namespace = element.get_knownns(prefix)
    if namespace is None:
        # raise ValueError, "'%s' is an unknown prefix" % str(prefix)
        return str(arg)
    p = element.get_nsprefix(namespace)
    return p


def cnv_formula(attribute, arg, element):
    """ A string containing a formula. Formulas do not have a predefined syntax, but the string should
        begin with a namespace prefix, followed by a “:” (COLON, U+003A) separator, followed by the text
        of the formula. The namespace bound to the prefix determines the syntax and semantics of the
        formula.
    """
    return __save_prefix(attribute, arg, element)


def cnv_ID(attribute, arg, element):
    return str(arg)


def cnv_IDREF(attribute, arg, element):
    return str(arg)


def cnv_integer(attribute, arg, element):
    return str(arg)


def cnv_legend_position(attribute, arg, element):
    if str(arg) not in ("start", "end", "top", "bottom",
                        "top-start", "bottom-start", "top-end", "bottom-end"):
        raise ValueError("'%s' not allowed" % str(arg))
    return str(arg)


pattern_length = re.compile(
    r'-?([0-9]+(\.[0-9]*)?|\.[0-9]+)((cm)|(mm)|(in)|(pt)|(pc)|(px))')


def cnv_length(attribute, arg, element):
    """ A (positive or negative) physical length, consisting of magnitude and unit, in conformance with the
        Units of Measure defined in §5.9.13 of [XSL].
    """
    global pattern_length
    if not pattern_length.match(arg):
        raise ValueError("'%s' is not a valid length" % arg)
    return arg


def cnv_lengthorpercent(attribute, arg, element):
    failed = False
    try:
        return cnv_length(attribute, arg, element)
    except BaseException:
        failed = True
    try:
        return cnv_percent(attribute, arg, element)
    except BaseException:
        failed = True
    if failed:
        raise ValueError("'%s' is not a valid length or percent" % arg)
    return arg


def cnv_metavaluetype(attribute, arg, element):
    if str(arg) not in ("float", "date", "time", "boolean", "string"):
        raise ValueError("'%s' not allowed" % str(arg))
    return str(arg)


def cnv_major_minor(attribute, arg, element):
    if arg not in ('major', 'minor'):
        raise ValueError("'%s' is not either 'minor' or 'major'" % arg)


pattern_namespacedToken = re.compile(r'[0-9a-zA-Z_]+:[0-9a-zA-Z._\-]+')


def cnv_namespacedToken(attribute, arg, element):
    global pattern_namespacedToken

    if not pattern_namespacedToken.match(arg):
        raise ValueError("'%s' is not a valid namespaced token" % arg)
    return __save_prefix(attribute, arg, element)


def cnv_NCName(attribute, arg, element):
    """ NCName is defined in http://www.w3.org/TR/REC-xml-names/#NT-NCName
        Essentially an XML name minus ':'
    """
    if type(arg) in (str,):
        return make_NCName(arg)
    else:
        return arg.getAttrNS(namespaces.STYLENS, 'name')


# This function takes either an instance of a style (preferred)
# or a text string naming the style. If it is a text string, then it must
# already have been converted to an NCName
# The text-string argument is mainly for when we build a structure from XML


def cnv_StyleNameRef(attribute, arg, element):
    try:
        return arg.getAttrNS(namespaces.STYLENS, 'name')
    except BaseException:
        return arg


# This function takes either an instance of a style (preferred)
# or a text string naming the style. If it is a text string, then it must
# already have been converted to an NCName
# The text-string argument is mainly for when we build a structure from XML


def cnv_DrawNameRef(attribute, arg, element):
    try:
        return arg.getAttrNS(namespaces.DRAWNS, 'name')
    except BaseException:
        return arg


# Must accept list of Style objects


def cnv_NCNames(attribute, arg, element):
    return ' '.join(arg)


def cnv_nonNegativeInteger(attribute, arg, element):
    return str(arg)


pattern_percent = re.compile(r'-?([0-9]+(\.[0-9]*)?|\.[0-9]+)%')


def cnv_percent(attribute, arg, element):
    global pattern_percent
    if not pattern_percent.match(arg):
        raise ValueError("'%s' is not a valid length" % arg)
    return arg


# Real one doesn't allow floating point values
pattern_points = re.compile(r'-?[0-9]+,-?[0-9]+([ ]+-?[0-9]+,-?[0-9]+)*')


# pattern_points = re.compile(r'-?[0-9.]+,-?[0-9.]+([ ]+-?[0-9.]+,-?[0-9.]+)*')


def cnv_points(attribute, arg, element):
    global pattern_points
    if type(arg) in (str,):
        if not pattern_points.match(arg):
            raise ValueError(
                "x,y are separated by a comma and the points are separated by white spaces")
        return arg
    else:
        try:
            strarg = ' '.join(["%d,%d" % p for p in arg])
        except BaseException:
            raise ValueError(
                "Points must be string or [(0,0),(1,1)] - not %s" %
                arg)
        return strarg


def cnv_positiveInteger(attribute, arg, element):
    return str(arg)


def cnv_string(attribute, arg, element):
    return str(arg)


def cnv_textnoteclass(attribute, arg, element):
    if str(arg) not in ("footnote", "endnote"):
        raise ValueError("'%s' not allowed" % str(arg))
    return str(arg)


# Understand different time formats


def cnv_time(attribute, arg, element):
    return str(arg)


def cnv_token(attribute, arg, element):
    return str(arg)


pattern_viewbox = re.compile(r'-?[0-9]+([ ]+-?[0-9]+){3}$')


def cnv_viewbox(attribute, arg, element):
    global pattern_viewbox
    if not pattern_viewbox.match(arg):
        raise ValueError(
            "viewBox must be four integers separated by whitespaces")
    return arg


def cnv_xlinkshow(attribute, arg, element):
    if str(arg) not in ("new", "replace", "embed"):
        raise ValueError("'%s' not allowed" % str(arg))
    return str(arg)


attrconverters = {
    ((namespaces.ANIMNS, 'audio-level'), None): cnv_double,
    ((namespaces.ANIMNS, 'color-interpolation'), None): cnv_string,
    ((namespaces.ANIMNS, 'color-interpolation-direction'), None): cnv_string,
    ((namespaces.ANIMNS, 'command'), None): cnv_string,
    ((namespaces.ANIMNS, 'formula'), None): cnv_string,
    ((namespaces.ANIMNS, 'id'), None): cnv_ID,
    ((namespaces.ANIMNS, 'iterate-interval'), None): cnv_duration,
    ((namespaces.ANIMNS, 'iterate-type'), None): cnv_string,
    ((namespaces.ANIMNS, 'name'), None): cnv_string,
    ((namespaces.ANIMNS, 'sub-item'), None): cnv_string,
    ((namespaces.ANIMNS, 'value'), None): cnv_string,
    # ((DBNS,u'type'), None): cnv_namespacedToken,
    ((namespaces.CHARTNS, 'attached-axis'), None): cnv_string,
    ((namespaces.CHARTNS, 'class'), (namespaces.CHARTNS, 'grid')): cnv_major_minor,
    ((namespaces.CHARTNS, 'class'), None): cnv_namespacedToken,
    ((namespaces.CHARTNS, 'column-mapping'), None): cnv_string,
    ((namespaces.CHARTNS, 'connect-bars'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'data-label-number'), None): cnv_string,
    ((namespaces.CHARTNS, 'data-label-symbol'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'data-label-text'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'data-source-has-labels'), None): cnv_data_source_has_labels,
    ((namespaces.CHARTNS, 'deep'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'dimension'), None): cnv_string,
    ((namespaces.CHARTNS, 'display-label'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'error-category'), None): cnv_string,
    ((namespaces.CHARTNS, 'error-lower-indicator'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'error-lower-limit'), None): cnv_string,
    ((namespaces.CHARTNS, 'error-margin'), None): cnv_string,
    ((namespaces.CHARTNS, 'error-percentage'), None): cnv_string,
    ((namespaces.CHARTNS, 'error-upper-indicator'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'error-upper-limit'), None): cnv_string,
    ((namespaces.CHARTNS, 'gap-width'), None): cnv_string,
    ((namespaces.CHARTNS, 'interpolation'), None): cnv_string,
    ((namespaces.CHARTNS, 'interval-major'), None): cnv_string,
    ((namespaces.CHARTNS, 'interval-minor-divisor'), None): cnv_string,
    ((namespaces.CHARTNS, 'japanese-candle-stick'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'label-arrangement'), None): cnv_string,
    ((namespaces.CHARTNS, 'label-cell-address'), None): cnv_string,
    ((namespaces.CHARTNS, 'legend-align'), None): cnv_string,
    ((namespaces.CHARTNS, 'legend-position'), None): cnv_legend_position,
    ((namespaces.CHARTNS, 'lines'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'link-data-style-to-source'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'logarithmic'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'maximum'), None): cnv_string,
    ((namespaces.CHARTNS, 'mean-value'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'minimum'), None): cnv_string,
    ((namespaces.CHARTNS, 'name'), None): cnv_string,
    ((namespaces.CHARTNS, 'origin'), None): cnv_string,
    ((namespaces.CHARTNS, 'overlap'), None): cnv_string,
    ((namespaces.CHARTNS, 'percentage'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'pie-offset'), None): cnv_string,
    ((namespaces.CHARTNS, 'regression-type'), None): cnv_string,
    ((namespaces.CHARTNS, 'repeated'), None): cnv_nonNegativeInteger,
    ((namespaces.CHARTNS, 'row-mapping'), None): cnv_string,
    ((namespaces.CHARTNS, 'scale-text'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'series-source'), None): cnv_string,
    ((namespaces.CHARTNS, 'solid-type'), None): cnv_string,
    ((namespaces.CHARTNS, 'spline-order'), None): cnv_string,
    ((namespaces.CHARTNS, 'spline-resolution'), None): cnv_string,
    ((namespaces.CHARTNS, 'stacked'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'style-name'), None): cnv_StyleNameRef,
    ((namespaces.CHARTNS, 'symbol-height'), None): cnv_string,
    ((namespaces.CHARTNS, 'symbol-name'), None): cnv_string,
    ((namespaces.CHARTNS, 'symbol-type'), None): cnv_string,
    ((namespaces.CHARTNS, 'symbol-width'), None): cnv_string,
    ((namespaces.CHARTNS, 'text-overlap'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'three-dimensional'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'tick-marks-major-inner'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'tick-marks-major-outer'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'tick-marks-minor-inner'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'tick-marks-minor-outer'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'values-cell-range-address'), None): cnv_string,
    ((namespaces.CHARTNS, 'vertical'), None): cnv_boolean,
    ((namespaces.CHARTNS, 'visible'), None): cnv_boolean,
    ((namespaces.CONFIGNS, 'name'), None): cnv_formula,
    ((namespaces.CONFIGNS, 'type'), None): cnv_configtype,
    ((namespaces.DR3DNS, 'ambient-color'), None): cnv_string,
    ((namespaces.DR3DNS, 'back-scale'), None): cnv_string,
    ((namespaces.DR3DNS, 'backface-culling'), None): cnv_string,
    ((namespaces.DR3DNS, 'center'), None): cnv_string,
    ((namespaces.DR3DNS, 'close-back'), None): cnv_boolean,
    ((namespaces.DR3DNS, 'close-front'), None): cnv_boolean,
    ((namespaces.DR3DNS, 'depth'), None): cnv_length,
    ((namespaces.DR3DNS, 'diffuse-color'), None): cnv_string,
    ((namespaces.DR3DNS, 'direction'), None): cnv_string,
    ((namespaces.DR3DNS, 'distance'), None): cnv_length,
    ((namespaces.DR3DNS, 'edge-rounding'), None): cnv_string,
    ((namespaces.DR3DNS, 'edge-rounding-mode'), None): cnv_string,
    ((namespaces.DR3DNS, 'emissive-color'), None): cnv_string,
    ((namespaces.DR3DNS, 'enabled'), None): cnv_boolean,
    ((namespaces.DR3DNS, 'end-angle'), None): cnv_string,
    ((namespaces.DR3DNS, 'focal-length'), None): cnv_length,
    ((namespaces.DR3DNS, 'horizontal-segments'), None): cnv_string,
    ((namespaces.DR3DNS, 'lighting-mode'), None): cnv_boolean,
    ((namespaces.DR3DNS, 'max-edge'), None): cnv_string,
    ((namespaces.DR3DNS, 'min-edge'), None): cnv_string,
    ((namespaces.DR3DNS, 'normals-direction'), None): cnv_string,
    ((namespaces.DR3DNS, 'normals-kind'), None): cnv_string,
    ((namespaces.DR3DNS, 'projection'), None): cnv_string,
    ((namespaces.DR3DNS, 'shade-mode'), None): cnv_string,
    ((namespaces.DR3DNS, 'shadow'), None): cnv_string,
    ((namespaces.DR3DNS, 'shadow-slant'), None): cnv_nonNegativeInteger,
    ((namespaces.DR3DNS, 'shininess'), None): cnv_string,
    ((namespaces.DR3DNS, 'size'), None): cnv_string,
    ((namespaces.DR3DNS, 'specular'), None): cnv_boolean,
    ((namespaces.DR3DNS, 'specular-color'), None): cnv_string,
    ((namespaces.DR3DNS, 'texture-filter'), None): cnv_string,
    ((namespaces.DR3DNS, 'texture-generation-mode-x'), None): cnv_string,
    ((namespaces.DR3DNS, 'texture-generation-mode-y'), None): cnv_string,
    ((namespaces.DR3DNS, 'texture-kind'), None): cnv_string,
    ((namespaces.DR3DNS, 'texture-mode'), None): cnv_string,
    ((namespaces.DR3DNS, 'transform'), None): cnv_string,
    ((namespaces.DR3DNS, 'vertical-segments'), None): cnv_string,
    ((namespaces.DR3DNS, 'vpn'), None): cnv_string,
    ((namespaces.DR3DNS, 'vrp'), None): cnv_string,
    ((namespaces.DR3DNS, 'vup'), None): cnv_string,
    ((namespaces.DRAWNS, 'align'), None): cnv_string,
    ((namespaces.DRAWNS, 'angle'), None): cnv_integer,
    ((namespaces.DRAWNS, 'archive'), None): cnv_string,
    ((namespaces.DRAWNS, 'auto-grow-height'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'auto-grow-width'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'background-size'), None): cnv_string,
    ((namespaces.DRAWNS, 'blue'), None): cnv_string,
    ((namespaces.DRAWNS, 'border'), None): cnv_string,
    ((namespaces.DRAWNS, 'caption-angle'), None): cnv_string,
    ((namespaces.DRAWNS, 'caption-angle-type'), None): cnv_string,
    ((namespaces.DRAWNS, 'caption-escape'), None): cnv_string,
    ((namespaces.DRAWNS, 'caption-escape-direction'), None): cnv_string,
    ((namespaces.DRAWNS, 'caption-fit-line-length'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'caption-gap'), None): cnv_string,
    ((namespaces.DRAWNS, 'caption-line-length'), None): cnv_length,
    ((namespaces.DRAWNS, 'caption-point-x'), None): cnv_string,
    ((namespaces.DRAWNS, 'caption-point-y'), None): cnv_string,
    ((namespaces.DRAWNS, 'caption-id'), None): cnv_IDREF,
    ((namespaces.DRAWNS, 'caption-type'), None): cnv_string,
    ((namespaces.DRAWNS, 'chain-next-name'), None): cnv_string,
    ((namespaces.DRAWNS, 'class-id'), None): cnv_string,
    ((namespaces.DRAWNS, 'class-names'), None): cnv_NCNames,
    ((namespaces.DRAWNS, 'code'), None): cnv_string,
    ((namespaces.DRAWNS, 'color'), None): cnv_string,
    ((namespaces.DRAWNS, 'color-inversion'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'color-mode'), None): cnv_string,
    ((namespaces.DRAWNS, 'concave'), None): cnv_string,
    ((namespaces.DRAWNS, 'concentric-gradient-fill-allowed'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'contrast'), None): cnv_string,
    ((namespaces.DRAWNS, 'control'), None): cnv_IDREF,
    ((namespaces.DRAWNS, 'copy-of'), None): cnv_string,
    ((namespaces.DRAWNS, 'corner-radius'), None): cnv_length,
    ((namespaces.DRAWNS, 'corners'), None): cnv_positiveInteger,
    ((namespaces.DRAWNS, 'cx'), None): cnv_string,
    ((namespaces.DRAWNS, 'cy'), None): cnv_string,
    ((namespaces.DRAWNS, 'data'), None): cnv_string,
    ((namespaces.DRAWNS, 'decimal-places'), None): cnv_string,
    ((namespaces.DRAWNS, 'display'), None): cnv_string,
    ((namespaces.DRAWNS, 'display-name'), None): cnv_string,
    ((namespaces.DRAWNS, 'distance'), None): cnv_lengthorpercent,
    ((namespaces.DRAWNS, 'dots1'), None): cnv_integer,
    ((namespaces.DRAWNS, 'dots1-length'), None): cnv_lengthorpercent,
    ((namespaces.DRAWNS, 'dots2'), None): cnv_integer,
    ((namespaces.DRAWNS, 'dots2-length'), None): cnv_lengthorpercent,
    ((namespaces.DRAWNS, 'end-angle'), None): cnv_double,
    ((namespaces.DRAWNS, 'end'), None): cnv_string,
    ((namespaces.DRAWNS, 'end-color'), None): cnv_string,
    ((namespaces.DRAWNS, 'end-glue-point'), None): cnv_nonNegativeInteger,
    ((namespaces.DRAWNS, 'end-guide'), None): cnv_length,
    ((namespaces.DRAWNS, 'end-intensity'), None): cnv_string,
    ((namespaces.DRAWNS, 'end-line-spacing-horizontal'), None): cnv_string,
    ((namespaces.DRAWNS, 'end-line-spacing-vertical'), None): cnv_string,
    ((namespaces.DRAWNS, 'end-shape'), None): cnv_IDREF,
    ((namespaces.DRAWNS, 'engine'), None): cnv_namespacedToken,
    ((namespaces.DRAWNS, 'enhanced-path'), None): cnv_string,
    ((namespaces.DRAWNS, 'escape-direction'), None): cnv_string,
    ((namespaces.DRAWNS, 'extrusion-allowed'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'extrusion-brightness'), None): cnv_string,
    ((namespaces.DRAWNS, 'extrusion'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'extrusion-color'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'extrusion-depth'), None): cnv_double,
    ((namespaces.DRAWNS, 'extrusion-diffusion'), None): cnv_string,
    ((namespaces.DRAWNS, 'extrusion-first-light-direction'), None): cnv_string,
    ((namespaces.DRAWNS, 'extrusion-first-light-harsh'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'extrusion-first-light-level'), None): cnv_string,
    ((namespaces.DRAWNS, 'extrusion-light-face'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'extrusion-metal'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'extrusion-number-of-line-segments'), None): cnv_integer,
    ((namespaces.DRAWNS, 'extrusion-origin'), None): cnv_double,
    ((namespaces.DRAWNS, 'extrusion-rotation-angle'), None): cnv_double,
    ((namespaces.DRAWNS, 'extrusion-rotation-center'), None): cnv_string,
    ((namespaces.DRAWNS, 'extrusion-second-light-direction'), None): cnv_string,
    ((namespaces.DRAWNS, 'extrusion-second-light-harsh'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'extrusion-second-light-level'), None): cnv_string,
    ((namespaces.DRAWNS, 'extrusion-shininess'), None): cnv_string,
    ((namespaces.DRAWNS, 'extrusion-skew'), None): cnv_double,
    ((namespaces.DRAWNS, 'extrusion-specularity'), None): cnv_string,
    ((namespaces.DRAWNS, 'extrusion-viewpoint'), None): cnv_string,
    ((namespaces.DRAWNS, 'fill'), None): cnv_string,
    ((namespaces.DRAWNS, 'fill-color'), None): cnv_string,
    ((namespaces.DRAWNS, 'fill-gradient-name'), None): cnv_string,
    ((namespaces.DRAWNS, 'fill-hatch-name'), None): cnv_string,
    ((namespaces.DRAWNS, 'fill-hatch-solid'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'fill-image-height'), None): cnv_lengthorpercent,
    ((namespaces.DRAWNS, 'fill-image-name'), None): cnv_DrawNameRef,
    ((namespaces.DRAWNS, 'fill-image-ref-point'), None): cnv_string,
    ((namespaces.DRAWNS, 'fill-image-ref-point-x'), None): cnv_string,
    ((namespaces.DRAWNS, 'fill-image-ref-point-y'), None): cnv_string,
    ((namespaces.DRAWNS, 'fill-image-width'), None): cnv_lengthorpercent,
    ((namespaces.DRAWNS, 'filter-name'), None): cnv_string,
    ((namespaces.DRAWNS, 'fit-to-contour'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'fit-to-size'), None): cnv_string,  # ODF 1.2 says boolean
    ((namespaces.DRAWNS, 'formula'), None): cnv_string,
    ((namespaces.DRAWNS, 'frame-display-border'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'frame-display-scrollbar'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'frame-margin-horizontal'), None): cnv_string,
    ((namespaces.DRAWNS, 'frame-margin-vertical'), None): cnv_string,
    ((namespaces.DRAWNS, 'frame-name'), None): cnv_string,
    ((namespaces.DRAWNS, 'gamma'), None): cnv_string,
    ((namespaces.DRAWNS, 'glue-point-leaving-directions'), None): cnv_string,
    ((namespaces.DRAWNS, 'glue-point-type'), None): cnv_string,
    ((namespaces.DRAWNS, 'glue-points'), None): cnv_string,
    ((namespaces.DRAWNS, 'gradient-step-count'), None): cnv_string,
    ((namespaces.DRAWNS, 'green'), None): cnv_string,
    ((namespaces.DRAWNS, 'guide-distance'), None): cnv_string,
    ((namespaces.DRAWNS, 'guide-overhang'), None): cnv_length,
    ((namespaces.DRAWNS, 'handle-mirror-horizontal'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'handle-mirror-vertical'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'handle-polar'), None): cnv_string,
    ((namespaces.DRAWNS, 'handle-position'), None): cnv_string,
    ((namespaces.DRAWNS, 'handle-radius-range-maximum'), None): cnv_string,
    ((namespaces.DRAWNS, 'handle-radius-range-minimum'), None): cnv_string,
    ((namespaces.DRAWNS, 'handle-range-x-maximum'), None): cnv_string,
    ((namespaces.DRAWNS, 'handle-range-x-minimum'), None): cnv_string,
    ((namespaces.DRAWNS, 'handle-range-y-maximum'), None): cnv_string,
    ((namespaces.DRAWNS, 'handle-range-y-minimum'), None): cnv_string,
    ((namespaces.DRAWNS, 'handle-switched'), None): cnv_boolean,
    # ((DRAWNS,u'id'), None): cnv_ID,
    # ((DRAWNS,u'id'), None): cnv_nonNegativeInteger,   # ?? line 6581 in RNG
    ((namespaces.DRAWNS, 'id'), None): cnv_string,
    ((namespaces.DRAWNS, 'image-opacity'), None): cnv_string,
    ((namespaces.DRAWNS, 'kind'), None): cnv_string,
    ((namespaces.DRAWNS, 'layer'), None): cnv_string,
    ((namespaces.DRAWNS, 'line-distance'), None): cnv_string,
    ((namespaces.DRAWNS, 'line-skew'), None): cnv_string,
    ((namespaces.DRAWNS, 'luminance'), None): cnv_string,
    ((namespaces.DRAWNS, 'marker-end-center'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'marker-end'), None): cnv_string,
    ((namespaces.DRAWNS, 'marker-end-width'), None): cnv_length,
    ((namespaces.DRAWNS, 'marker-start-center'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'marker-start'), None): cnv_string,
    ((namespaces.DRAWNS, 'marker-start-width'), None): cnv_length,
    ((namespaces.DRAWNS, 'master-page-name'), None): cnv_StyleNameRef,
    ((namespaces.DRAWNS, 'may-script'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'measure-align'), None): cnv_string,
    ((namespaces.DRAWNS, 'measure-vertical-align'), None): cnv_string,
    ((namespaces.DRAWNS, 'mime-type'), None): cnv_string,
    ((namespaces.DRAWNS, 'mirror-horizontal'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'mirror-vertical'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'modifiers'), None): cnv_string,
    ((namespaces.DRAWNS, 'name'), None): cnv_NCName,
    # ((DRAWNS,u'name'), None): cnv_string,
    ((namespaces.DRAWNS, 'nav-order'), None): cnv_IDREF,
    ((namespaces.DRAWNS, 'nohref'), None): cnv_string,
    ((namespaces.DRAWNS, 'notify-on-update-of-ranges'), None): cnv_string,
    ((namespaces.DRAWNS, 'object'), None): cnv_string,
    ((namespaces.DRAWNS, 'ole-draw-aspect'), None): cnv_string,
    ((namespaces.DRAWNS, 'opacity'), None): cnv_string,
    ((namespaces.DRAWNS, 'opacity-name'), None): cnv_string,
    ((namespaces.DRAWNS, 'page-number'), None): cnv_positiveInteger,
    ((namespaces.DRAWNS, 'parallel'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'path-stretchpoint-x'), None): cnv_double,
    ((namespaces.DRAWNS, 'path-stretchpoint-y'), None): cnv_double,
    ((namespaces.DRAWNS, 'placing'), None): cnv_string,
    ((namespaces.DRAWNS, 'points'), None): cnv_points,
    ((namespaces.DRAWNS, 'protected'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'recreate-on-edit'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'red'), None): cnv_string,
    ((namespaces.DRAWNS, 'rotation'), None): cnv_integer,
    ((namespaces.DRAWNS, 'secondary-fill-color'), None): cnv_string,
    ((namespaces.DRAWNS, 'shadow'), None): cnv_string,
    ((namespaces.DRAWNS, 'shadow-color'), None): cnv_string,
    ((namespaces.DRAWNS, 'shadow-offset-x'), None): cnv_length,
    ((namespaces.DRAWNS, 'shadow-offset-y'), None): cnv_length,
    ((namespaces.DRAWNS, 'shadow-opacity'), None): cnv_string,
    ((namespaces.DRAWNS, 'shape-id'), None): cnv_IDREF,
    ((namespaces.DRAWNS, 'sharpness'), None): cnv_string,
    ((namespaces.DRAWNS, 'show-unit'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'start-angle'), None): cnv_double,
    ((namespaces.DRAWNS, 'start'), None): cnv_string,
    ((namespaces.DRAWNS, 'start-color'), None): cnv_string,
    ((namespaces.DRAWNS, 'start-glue-point'), None): cnv_nonNegativeInteger,
    ((namespaces.DRAWNS, 'start-guide'), None): cnv_length,
    ((namespaces.DRAWNS, 'start-intensity'), None): cnv_string,
    ((namespaces.DRAWNS, 'start-line-spacing-horizontal'), None): cnv_string,
    ((namespaces.DRAWNS, 'start-line-spacing-vertical'), None): cnv_string,
    ((namespaces.DRAWNS, 'start-shape'), None): cnv_IDREF,
    ((namespaces.DRAWNS, 'stroke'), None): cnv_string,
    ((namespaces.DRAWNS, 'stroke-dash'), None): cnv_string,
    ((namespaces.DRAWNS, 'stroke-dash-names'), None): cnv_string,
    ((namespaces.DRAWNS, 'stroke-linejoin'), None): cnv_string,
    ((namespaces.DRAWNS, 'style'), None): cnv_string,
    ((namespaces.DRAWNS, 'style-name'), None): cnv_StyleNameRef,
    ((namespaces.DRAWNS, 'symbol-color'), None): cnv_string,
    ((namespaces.DRAWNS, 'text-areas'), None): cnv_string,
    ((namespaces.DRAWNS, 'text-path-allowed'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'text-path'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'text-path-mode'), None): cnv_string,
    ((namespaces.DRAWNS, 'text-path-same-letter-heights'), None): cnv_boolean,
    ((namespaces.DRAWNS, 'text-path-scale'), None): cnv_string,
    ((namespaces.DRAWNS, 'text-rotate-angle'), None): cnv_double,
    ((namespaces.DRAWNS, 'text-style-name'), None): cnv_StyleNameRef,
    ((namespaces.DRAWNS, 'textarea-horizontal-align'), None): cnv_string,
    ((namespaces.DRAWNS, 'textarea-vertical-align'), None): cnv_string,
    ((namespaces.DRAWNS, 'tile-repeat-offset'), None): cnv_string,
    ((namespaces.DRAWNS, 'transform'), None): cnv_string,
    ((namespaces.DRAWNS, 'type'), None): cnv_string,
    ((namespaces.DRAWNS, 'unit'), None): cnv_string,
    ((namespaces.DRAWNS, 'value'), None): cnv_string,
    ((namespaces.DRAWNS, 'visible-area-height'), None): cnv_string,
    ((namespaces.DRAWNS, 'visible-area-left'), None): cnv_string,
    ((namespaces.DRAWNS, 'visible-area-top'), None): cnv_string,
    ((namespaces.DRAWNS, 'visible-area-width'), None): cnv_string,
    ((namespaces.DRAWNS, 'wrap-influence-on-position'), None): cnv_string,
    ((namespaces.DRAWNS, 'z-index'), None): cnv_nonNegativeInteger,
    ((namespaces.FONS, 'background-color'), None): cnv_string,
    ((namespaces.FONS, 'border-bottom'), None): cnv_string,
    ((namespaces.FONS, 'border'), None): cnv_string,
    ((namespaces.FONS, 'border-left'), None): cnv_string,
    ((namespaces.FONS, 'border-right'), None): cnv_string,
    ((namespaces.FONS, 'border-top'), None): cnv_string,
    ((namespaces.FONS, 'break-after'), None): cnv_string,
    ((namespaces.FONS, 'break-before'), None): cnv_string,
    ((namespaces.FONS, 'clip'), None): cnv_string,
    ((namespaces.FONS, 'color'), None): cnv_string,
    ((namespaces.FONS, 'column-count'), None): cnv_positiveInteger,
    ((namespaces.FONS, 'column-gap'), None): cnv_length,
    ((namespaces.FONS, 'country'), None): cnv_token,
    ((namespaces.FONS, 'end-indent'), None): cnv_length,
    ((namespaces.FONS, 'font-family'), None): cnv_string,
    ((namespaces.FONS, 'font-size'), None): cnv_string,
    ((namespaces.FONS, 'font-style'), None): cnv_string,
    ((namespaces.FONS, 'font-variant'), None): cnv_string,
    ((namespaces.FONS, 'font-weight'), None): cnv_string,
    ((namespaces.FONS, 'height'), None): cnv_string,
    ((namespaces.FONS, 'hyphenate'), None): cnv_boolean,
    ((namespaces.FONS, 'hyphenation-keep'), None): cnv_string,
    ((namespaces.FONS, 'hyphenation-ladder-count'), None): cnv_string,
    ((namespaces.FONS, 'hyphenation-push-char-count'), None): cnv_string,
    ((namespaces.FONS, 'hyphenation-remain-char-count'), None): cnv_string,
    ((namespaces.FONS, 'keep-together'), None): cnv_string,
    ((namespaces.FONS, 'keep-with-next'), None): cnv_string,
    ((namespaces.FONS, 'language'), None): cnv_token,
    ((namespaces.FONS, 'letter-spacing'), None): cnv_string,
    ((namespaces.FONS, 'line-height'), None): cnv_string,
    ((namespaces.FONS, 'margin-bottom'), None): cnv_string,
    ((namespaces.FONS, 'margin'), None): cnv_string,
    ((namespaces.FONS, 'margin-left'), None): cnv_string,
    ((namespaces.FONS, 'margin-right'), None): cnv_string,
    ((namespaces.FONS, 'margin-top'), None): cnv_string,
    ((namespaces.FONS, 'max-height'), None): cnv_string,
    ((namespaces.FONS, 'max-width'), None): cnv_string,
    ((namespaces.FONS, 'min-height'), None): cnv_length,
    ((namespaces.FONS, 'min-width'), None): cnv_string,
    ((namespaces.FONS, 'orphans'), None): cnv_string,
    ((namespaces.FONS, 'padding-bottom'), None): cnv_string,
    ((namespaces.FONS, 'padding'), None): cnv_string,
    ((namespaces.FONS, 'padding-left'), None): cnv_string,
    ((namespaces.FONS, 'padding-right'), None): cnv_string,
    ((namespaces.FONS, 'padding-top'), None): cnv_string,
    ((namespaces.FONS, 'page-height'), None): cnv_length,
    ((namespaces.FONS, 'page-width'), None): cnv_length,
    ((namespaces.FONS, 'space-after'), None): cnv_length,
    ((namespaces.FONS, 'space-before'), None): cnv_length,
    ((namespaces.FONS, 'start-indent'), None): cnv_length,
    ((namespaces.FONS, 'text-align'), None): cnv_string,
    ((namespaces.FONS, 'text-align-last'), None): cnv_string,
    ((namespaces.FONS, 'text-indent'), None): cnv_string,
    ((namespaces.FONS, 'text-shadow'), None): cnv_string,
    ((namespaces.FONS, 'text-transform'), None): cnv_string,
    ((namespaces.FONS, 'widows'), None): cnv_string,
    ((namespaces.FONS, 'width'), None): cnv_string,
    ((namespaces.FONS, 'wrap-option'), None): cnv_string,
    ((namespaces.FORMNS, 'allow-deletes'), None): cnv_boolean,
    ((namespaces.FORMNS, 'allow-inserts'), None): cnv_boolean,
    ((namespaces.FORMNS, 'allow-updates'), None): cnv_boolean,
    ((namespaces.FORMNS, 'apply-design-mode'), None): cnv_boolean,
    ((namespaces.FORMNS, 'apply-filter'), None): cnv_boolean,
    ((namespaces.FORMNS, 'auto-complete'), None): cnv_boolean,
    ((namespaces.FORMNS, 'automatic-focus'), None): cnv_boolean,
    ((namespaces.FORMNS, 'bound-column'), None): cnv_string,
    ((namespaces.FORMNS, 'button-type'), None): cnv_string,
    ((namespaces.FORMNS, 'command'), None): cnv_string,
    ((namespaces.FORMNS, 'command-type'), None): cnv_string,
    ((namespaces.FORMNS, 'control-implementation'), None): cnv_namespacedToken,
    ((namespaces.FORMNS, 'convert-empty-to-null'), None): cnv_boolean,
    ((namespaces.FORMNS, 'current-selected'), None): cnv_boolean,
    ((namespaces.FORMNS, 'current-state'), None): cnv_string,
    # ((FORMNS,u'current-value'), None): cnv_date,
    # ((FORMNS,u'current-value'), None): cnv_double,
    ((namespaces.FORMNS, 'current-value'), None): cnv_string,
    # ((FORMNS,u'current-value'), None): cnv_time,
    ((namespaces.FORMNS, 'data-field'), None): cnv_string,
    ((namespaces.FORMNS, 'datasource'), None): cnv_string,
    ((namespaces.FORMNS, 'default-button'), None): cnv_boolean,
    ((namespaces.FORMNS, 'delay-for-repeat'), None): cnv_duration,
    ((namespaces.FORMNS, 'detail-fields'), None): cnv_string,
    ((namespaces.FORMNS, 'disabled'), None): cnv_boolean,
    ((namespaces.FORMNS, 'dropdown'), None): cnv_boolean,
    ((namespaces.FORMNS, 'echo-char'), None): cnv_string,
    ((namespaces.FORMNS, 'enctype'), None): cnv_string,
    ((namespaces.FORMNS, 'escape-processing'), None): cnv_boolean,
    ((namespaces.FORMNS, 'filter'), None): cnv_string,
    ((namespaces.FORMNS, 'focus-on-click'), None): cnv_boolean,
    ((namespaces.FORMNS, 'for'), None): cnv_string,
    ((namespaces.FORMNS, 'id'), None): cnv_ID,
    ((namespaces.FORMNS, 'ignore-result'), None): cnv_boolean,
    ((namespaces.FORMNS, 'image-align'), None): cnv_string,
    ((namespaces.FORMNS, 'image-data'), None): cnv_anyURI,
    ((namespaces.FORMNS, 'image-position'), None): cnv_string,
    ((namespaces.FORMNS, 'is-tristate'), None): cnv_boolean,
    ((namespaces.FORMNS, 'label'), None): cnv_string,
    ((namespaces.FORMNS, 'list-source'), None): cnv_string,
    ((namespaces.FORMNS, 'list-source-type'), None): cnv_string,
    ((namespaces.FORMNS, 'master-fields'), None): cnv_string,
    ((namespaces.FORMNS, 'max-length'), None): cnv_nonNegativeInteger,
    # ((FORMNS,u'max-value'), None): cnv_date,
    # ((FORMNS,u'max-value'), None): cnv_double,
    ((namespaces.FORMNS, 'max-value'), None): cnv_string,
    # ((FORMNS,u'max-value'), None): cnv_time,
    ((namespaces.FORMNS, 'method'), None): cnv_string,
    # ((FORMNS,u'min-value'), None): cnv_date,
    # ((FORMNS,u'min-value'), None): cnv_double,
    ((namespaces.FORMNS, 'min-value'), None): cnv_string,
    # ((FORMNS,u'min-value'), None): cnv_time,
    ((namespaces.FORMNS, 'multi-line'), None): cnv_boolean,
    ((namespaces.FORMNS, 'multiple'), None): cnv_boolean,
    ((namespaces.FORMNS, 'name'), None): cnv_string,
    ((namespaces.FORMNS, 'navigation-mode'), None): cnv_string,
    ((namespaces.FORMNS, 'order'), None): cnv_string,
    ((namespaces.FORMNS, 'orientation'), None): cnv_string,
    ((namespaces.FORMNS, 'page-step-size'), None): cnv_positiveInteger,
    ((namespaces.FORMNS, 'printable'), None): cnv_boolean,
    ((namespaces.FORMNS, 'property-name'), None): cnv_string,
    ((namespaces.FORMNS, 'readonly'), None): cnv_boolean,
    ((namespaces.FORMNS, 'selected'), None): cnv_boolean,
    ((namespaces.FORMNS, 'size'), None): cnv_nonNegativeInteger,
    ((namespaces.FORMNS, 'state'), None): cnv_string,
    ((namespaces.FORMNS, 'step-size'), None): cnv_positiveInteger,
    ((namespaces.FORMNS, 'tab-cycle'), None): cnv_string,
    ((namespaces.FORMNS, 'tab-index'), None): cnv_nonNegativeInteger,
    ((namespaces.FORMNS, 'tab-stop'), None): cnv_boolean,
    ((namespaces.FORMNS, 'text-style-name'), None): cnv_StyleNameRef,
    ((namespaces.FORMNS, 'title'), None): cnv_string,
    ((namespaces.FORMNS, 'toggle'), None): cnv_boolean,
    ((namespaces.FORMNS, 'validation'), None): cnv_boolean,
    # ((FORMNS,u'value'), None): cnv_date,
    # ((FORMNS,u'value'), None): cnv_double,
    ((namespaces.FORMNS, 'value'), None): cnv_string,
    # ((FORMNS,u'value'), None): cnv_time,
    ((namespaces.FORMNS, 'visual-effect'), None): cnv_string,
    ((namespaces.FORMNS, 'xforms-list-source'), None): cnv_string,
    ((namespaces.FORMNS, 'xforms-submission'), None): cnv_string,
    ((namespaces.MANIFESTNS, 'algorithm-name'), None): cnv_string,
    ((namespaces.MANIFESTNS, 'checksum'), None): cnv_string,
    ((namespaces.MANIFESTNS, 'checksum-type'), None): cnv_string,
    ((namespaces.MANIFESTNS, 'full-path'), None): cnv_string,
    ((namespaces.MANIFESTNS, 'initialisation-vector'), None): cnv_string,
    ((namespaces.MANIFESTNS, 'iteration-count'), None): cnv_nonNegativeInteger,
    ((namespaces.MANIFESTNS, 'key-derivation-name'), None): cnv_string,
    ((namespaces.MANIFESTNS, 'media-type'), None): cnv_string,
    ((namespaces.MANIFESTNS, 'salt'), None): cnv_string,
    ((namespaces.MANIFESTNS, 'size'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'cell-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'character-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'date'), None): cnv_dateTime,
    ((namespaces.METANS, 'delay'), None): cnv_duration,
    ((namespaces.METANS, 'draw-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'frame-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'image-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'name'), None): cnv_string,
    ((namespaces.METANS, 'non-whitespace-character-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'object-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'ole-object-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'page-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'paragraph-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'row-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'sentence-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'syllable-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'table-count'), None): cnv_nonNegativeInteger,
    ((namespaces.METANS, 'value-type'), None): cnv_metavaluetype,
    ((namespaces.METANS, 'word-count'), None): cnv_nonNegativeInteger,
    ((namespaces.NUMBERNS, 'automatic-order'), None): cnv_boolean,
    ((namespaces.NUMBERNS, 'calendar'), None): cnv_string,
    ((namespaces.NUMBERNS, 'country'), None): cnv_token,
    ((namespaces.NUMBERNS, 'decimal-places'), None): cnv_integer,
    ((namespaces.NUMBERNS, 'decimal-replacement'), None): cnv_string,
    ((namespaces.NUMBERNS, 'denominator-value'), None): cnv_integer,
    ((namespaces.NUMBERNS, 'display-factor'), None): cnv_double,
    ((namespaces.NUMBERNS, 'format-source'), None): cnv_string,
    ((namespaces.NUMBERNS, 'grouping'), None): cnv_boolean,
    ((namespaces.NUMBERNS, 'language'), None): cnv_token,
    ((namespaces.NUMBERNS, 'min-denominator-digits'), None): cnv_integer,
    ((namespaces.NUMBERNS, 'min-exponent-digits'), None): cnv_integer,
    ((namespaces.NUMBERNS, 'min-integer-digits'), None): cnv_integer,
    ((namespaces.NUMBERNS, 'min-numerator-digits'), None): cnv_integer,
    ((namespaces.NUMBERNS, 'position'), None): cnv_integer,
    ((namespaces.NUMBERNS, 'possessive-form'), None): cnv_boolean,
    ((namespaces.NUMBERNS, 'style'), None): cnv_string,
    ((namespaces.NUMBERNS, 'textual'), None): cnv_boolean,
    ((namespaces.NUMBERNS, 'title'), None): cnv_string,
    ((namespaces.NUMBERNS, 'transliteration-country'), None): cnv_token,
    ((namespaces.NUMBERNS, 'transliteration-format'), None): cnv_string,
    ((namespaces.NUMBERNS, 'transliteration-language'), None): cnv_token,
    ((namespaces.NUMBERNS, 'transliteration-style'), None): cnv_string,
    ((namespaces.NUMBERNS, 'truncate-on-overflow'), None): cnv_boolean,
    ((namespaces.OFFICENS, 'automatic-update'), None): cnv_boolean,
    ((namespaces.OFFICENS, 'boolean-value'), None): cnv_boolean,
    ((namespaces.OFFICENS, 'conversion-mode'), None): cnv_string,
    ((namespaces.OFFICENS, 'currency'), None): cnv_string,
    ((namespaces.OFFICENS, 'date-value'), None): cnv_dateTime,
    ((namespaces.OFFICENS, 'dde-application'), None): cnv_string,
    ((namespaces.OFFICENS, 'dde-item'), None): cnv_string,
    ((namespaces.OFFICENS, 'dde-topic'), None): cnv_string,
    ((namespaces.OFFICENS, 'display'), None): cnv_boolean,
    ((namespaces.OFFICENS, 'mimetype'), None): cnv_string,
    ((namespaces.OFFICENS, 'name'), None): cnv_string,
    ((namespaces.OFFICENS, 'process-content'), None): cnv_boolean,
    ((namespaces.OFFICENS, 'server-map'), None): cnv_boolean,
    ((namespaces.OFFICENS, 'string-value'), None): cnv_string,
    ((namespaces.OFFICENS, 'target-frame'), None): cnv_string,
    ((namespaces.OFFICENS, 'target-frame-name'), None): cnv_string,
    ((namespaces.OFFICENS, 'time-value'), None): cnv_duration,
    ((namespaces.OFFICENS, 'title'), None): cnv_string,
    ((namespaces.OFFICENS, 'value'), None): cnv_double,
    ((namespaces.OFFICENS, 'value-type'), None): cnv_string,
    ((namespaces.OFFICENS, 'version'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'action'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'animations'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'background-objects-visible'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'background-visible'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'class'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'class-names'), None): cnv_NCNames,
    ((namespaces.PRESENTATIONNS, 'delay'), None): cnv_duration,
    ((namespaces.PRESENTATIONNS, 'direction'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'display-date-time'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'display-footer'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'display-header'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'display-page-number'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'duration'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'effect'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'endless'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'force-manual'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'full-screen'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'group-id'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'master-element'), None): cnv_IDREF,
    ((namespaces.PRESENTATIONNS, 'mouse-as-pen'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'mouse-visible'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'name'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'node-type'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'object'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'pages'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'path-id'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'pause'), None): cnv_duration,
    ((namespaces.PRESENTATIONNS, 'placeholder'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'play-full'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'presentation-page-layout-name'), None): cnv_StyleNameRef,
    ((namespaces.PRESENTATIONNS, 'preset-class'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'preset-id'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'preset-sub-type'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'show'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'show-end-of-presentation-slide'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'show-logo'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'source'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'speed'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'start-page'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'start-scale'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'start-with-navigator'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'stay-on-top'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'style-name'), None): cnv_StyleNameRef,
    ((namespaces.PRESENTATIONNS, 'transition-on-click'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'transition-speed'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'transition-style'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'transition-type'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'use-date-time-name'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'use-footer-name'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'use-header-name'), None): cnv_string,
    ((namespaces.PRESENTATIONNS, 'user-transformed'), None): cnv_boolean,
    ((namespaces.PRESENTATIONNS, 'verb'), None): cnv_nonNegativeInteger,
    ((namespaces.PRESENTATIONNS, 'visibility'), None): cnv_string,
    ((namespaces.SCRIPTNS, 'event-name'), None): cnv_formula,
    ((namespaces.SCRIPTNS, 'language'), None): cnv_formula,
    ((namespaces.SCRIPTNS, 'macro-name'), None): cnv_string,
    ((namespaces.SMILNS, 'accelerate'), None): cnv_double,
    ((namespaces.SMILNS, 'accumulate'), None): cnv_string,
    ((namespaces.SMILNS, 'additive'), None): cnv_string,
    ((namespaces.SMILNS, 'attributeName'), None): cnv_string,
    ((namespaces.SMILNS, 'autoReverse'), None): cnv_boolean,
    ((namespaces.SMILNS, 'begin'), None): cnv_string,
    ((namespaces.SMILNS, 'by'), None): cnv_string,
    ((namespaces.SMILNS, 'calcMode'), None): cnv_string,
    ((namespaces.SMILNS, 'decelerate'), None): cnv_double,
    ((namespaces.SMILNS, 'direction'), None): cnv_string,
    ((namespaces.SMILNS, 'dur'), None): cnv_string,
    ((namespaces.SMILNS, 'end'), None): cnv_string,
    ((namespaces.SMILNS, 'endsync'), None): cnv_string,
    ((namespaces.SMILNS, 'fadeColor'), None): cnv_string,
    ((namespaces.SMILNS, 'fill'), None): cnv_string,
    ((namespaces.SMILNS, 'fillDefault'), None): cnv_string,
    ((namespaces.SMILNS, 'from'), None): cnv_string,
    ((namespaces.SMILNS, 'keySplines'), None): cnv_string,
    ((namespaces.SMILNS, 'keyTimes'), None): cnv_string,
    ((namespaces.SMILNS, 'mode'), None): cnv_string,
    ((namespaces.SMILNS, 'repeatCount'), None): cnv_nonNegativeInteger,
    ((namespaces.SMILNS, 'repeatDur'), None): cnv_string,
    ((namespaces.SMILNS, 'restart'), None): cnv_string,
    ((namespaces.SMILNS, 'restartDefault'), None): cnv_string,
    ((namespaces.SMILNS, 'subtype'), None): cnv_string,
    ((namespaces.SMILNS, 'targetElement'), None): cnv_IDREF,
    ((namespaces.SMILNS, 'to'), None): cnv_string,
    ((namespaces.SMILNS, 'type'), None): cnv_string,
    ((namespaces.SMILNS, 'values'), None): cnv_string,
    ((namespaces.STYLENS, 'adjustment'), None): cnv_string,
    ((namespaces.STYLENS, 'apply-style-name'), None): cnv_StyleNameRef,
    ((namespaces.STYLENS, 'auto-text-indent'), None): cnv_boolean,
    ((namespaces.STYLENS, 'auto-update'), None): cnv_boolean,
    ((namespaces.STYLENS, 'background-transparency'), None): cnv_string,
    ((namespaces.STYLENS, 'base-cell-address'), None): cnv_string,
    ((namespaces.STYLENS, 'border-line-width-bottom'), None): cnv_string,
    ((namespaces.STYLENS, 'border-line-width'), None): cnv_string,
    ((namespaces.STYLENS, 'border-line-width-left'), None): cnv_string,
    ((namespaces.STYLENS, 'border-line-width-right'), None): cnv_string,
    ((namespaces.STYLENS, 'border-line-width-top'), None): cnv_string,
    ((namespaces.STYLENS, 'cell-protect'), None): cnv_string,
    ((namespaces.STYLENS, 'char'), None): cnv_string,
    ((namespaces.STYLENS, 'class'), None): cnv_string,
    ((namespaces.STYLENS, 'color'), None): cnv_string,
    ((namespaces.STYLENS, 'column-width'), None): cnv_string,
    ((namespaces.STYLENS, 'condition'), None): cnv_string,
    ((namespaces.STYLENS, 'country-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'country-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'data-style-name'), None): cnv_StyleNameRef,
    ((namespaces.STYLENS, 'decimal-places'), None): cnv_string,
    ((namespaces.STYLENS, 'default-outline-level'), None): cnv_positiveInteger,
    ((namespaces.STYLENS, 'diagonal-bl-tr'), None): cnv_string,
    ((namespaces.STYLENS, 'diagonal-bl-tr-widths'), None): cnv_string,
    ((namespaces.STYLENS, 'diagonal-tl-br'), None): cnv_string,
    ((namespaces.STYLENS, 'diagonal-tl-br-widths'), None): cnv_string,
    ((namespaces.STYLENS, 'direction'), None): cnv_string,
    ((namespaces.STYLENS, 'display'), None): cnv_boolean,
    ((namespaces.STYLENS, 'display-name'), None): cnv_string,
    ((namespaces.STYLENS, 'distance-after-sep'), None): cnv_length,
    ((namespaces.STYLENS, 'distance-before-sep'), None): cnv_length,
    ((namespaces.STYLENS, 'distance'), None): cnv_length,
    ((namespaces.STYLENS, 'dynamic-spacing'), None): cnv_boolean,
    ((namespaces.STYLENS, 'editable'), None): cnv_boolean,
    ((namespaces.STYLENS, 'family'), None): cnv_family,
    ((namespaces.STYLENS, 'filter-name'), None): cnv_string,
    ((namespaces.STYLENS, 'first-page-number'), None): cnv_string,
    ((namespaces.STYLENS, 'flow-with-text'), None): cnv_boolean,
    ((namespaces.STYLENS, 'font-adornments'), None): cnv_string,
    ((namespaces.STYLENS, 'font-charset'), None): cnv_string,
    ((namespaces.STYLENS, 'font-charset-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'font-charset-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'font-family-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'font-family-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'font-family-generic-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'font-family-generic'), None): cnv_string,
    ((namespaces.STYLENS, 'font-family-generic-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'font-independent-line-spacing'), None): cnv_boolean,
    ((namespaces.STYLENS, 'font-name-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'font-name'), None): cnv_string,
    ((namespaces.STYLENS, 'font-name-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'font-pitch-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'font-pitch'), None): cnv_string,
    ((namespaces.STYLENS, 'font-pitch-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'font-relief'), None): cnv_string,
    ((namespaces.STYLENS, 'font-size-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'font-size-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'font-size-rel-asian'), None): cnv_length,
    ((namespaces.STYLENS, 'font-size-rel'), None): cnv_length,
    ((namespaces.STYLENS, 'font-size-rel-complex'), None): cnv_length,
    ((namespaces.STYLENS, 'font-style-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'font-style-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'font-style-name-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'font-style-name'), None): cnv_string,
    ((namespaces.STYLENS, 'font-style-name-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'font-weight-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'font-weight-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'footnote-max-height'), None): cnv_length,
    ((namespaces.STYLENS, 'glyph-orientation-vertical'), None): cnv_string,
    ((namespaces.STYLENS, 'height'), None): cnv_string,
    ((namespaces.STYLENS, 'horizontal-pos'), None): cnv_string,
    ((namespaces.STYLENS, 'horizontal-rel'), None): cnv_string,
    ((namespaces.STYLENS, 'justify-single-word'), None): cnv_boolean,
    ((namespaces.STYLENS, 'language-asian'), None): cnv_string,
    ((namespaces.STYLENS, 'language-complex'), None): cnv_string,
    ((namespaces.STYLENS, 'layout-grid-base-height'), None): cnv_length,
    ((namespaces.STYLENS, 'layout-grid-color'), None): cnv_string,
    ((namespaces.STYLENS, 'layout-grid-display'), None): cnv_boolean,
    ((namespaces.STYLENS, 'layout-grid-lines'), None): cnv_string,
    ((namespaces.STYLENS, 'layout-grid-mode'), None): cnv_string,
    ((namespaces.STYLENS, 'layout-grid-print'), None): cnv_boolean,
    ((namespaces.STYLENS, 'layout-grid-ruby-below'), None): cnv_boolean,
    ((namespaces.STYLENS, 'layout-grid-ruby-height'), None): cnv_length,
    ((namespaces.STYLENS, 'leader-char'), None): cnv_string,
    ((namespaces.STYLENS, 'leader-color'), None): cnv_string,
    ((namespaces.STYLENS, 'leader-style'), None): cnv_string,
    ((namespaces.STYLENS, 'leader-text'), None): cnv_string,
    ((namespaces.STYLENS, 'leader-text-style'), None): cnv_StyleNameRef,
    ((namespaces.STYLENS, 'leader-type'), None): cnv_string,
    ((namespaces.STYLENS, 'leader-width'), None): cnv_string,
    ((namespaces.STYLENS, 'legend-expansion-aspect-ratio'), None): cnv_double,
    ((namespaces.STYLENS, 'legend-expansion'), None): cnv_string,
    ((namespaces.STYLENS, 'length'), None): cnv_positiveInteger,
    ((namespaces.STYLENS, 'letter-kerning'), None): cnv_boolean,
    ((namespaces.STYLENS, 'line-break'), None): cnv_string,
    ((namespaces.STYLENS, 'line-height-at-least'), None): cnv_string,
    ((namespaces.STYLENS, 'line-spacing'), None): cnv_length,
    ((namespaces.STYLENS, 'line-style'), None): cnv_string,
    ((namespaces.STYLENS, 'lines'), None): cnv_positiveInteger,
    ((namespaces.STYLENS, 'list-style-name'), None): cnv_StyleNameRef,
    ((namespaces.STYLENS, 'master-page-name'), None): cnv_StyleNameRef,
    ((namespaces.STYLENS, 'may-break-between-rows'), None): cnv_boolean,
    ((namespaces.STYLENS, 'min-row-height'), None): cnv_string,
    ((namespaces.STYLENS, 'mirror'), None): cnv_string,
    ((namespaces.STYLENS, 'name'), None): cnv_NCName,
    ((namespaces.STYLENS, 'name'), (namespaces.STYLENS, 'font-face')): cnv_string,
    ((namespaces.STYLENS, 'next-style-name'), None): cnv_StyleNameRef,
    ((namespaces.STYLENS, 'num-format'), None): cnv_string,
    ((namespaces.STYLENS, 'num-letter-sync'), None): cnv_boolean,
    ((namespaces.STYLENS, 'num-prefix'), None): cnv_string,
    ((namespaces.STYLENS, 'num-suffix'), None): cnv_string,
    ((namespaces.STYLENS, 'number-wrapped-paragraphs'), None): cnv_string,
    ((namespaces.STYLENS, 'overflow-behavior'), None): cnv_string,
    ((namespaces.STYLENS, 'page-layout-name'), None): cnv_StyleNameRef,
    ((namespaces.STYLENS, 'page-number'), None): cnv_string,
    ((namespaces.STYLENS, 'page-usage'), None): cnv_string,
    ((namespaces.STYLENS, 'paper-tray-name'), None): cnv_string,
    ((namespaces.STYLENS, 'parent-style-name'), None): cnv_StyleNameRef,
    ((namespaces.STYLENS, 'position'), (namespaces.STYLENS, 'tab-stop')): cnv_length,
    ((namespaces.STYLENS, 'position'), None): cnv_string,
    ((namespaces.STYLENS, 'print'), None): cnv_string,
    ((namespaces.STYLENS, 'print-content'), None): cnv_boolean,
    ((namespaces.STYLENS, 'print-orientation'), None): cnv_string,
    ((namespaces.STYLENS, 'print-page-order'), None): cnv_string,
    ((namespaces.STYLENS, 'protect'), (namespaces.STYLENS, 'section-properties')): cnv_boolean,
    ((namespaces.STYLENS, 'protect'), (namespaces.STYLENS, 'graphic-properties')): cnv_string,
    # ((STYLENS,u'protect'), None): cnv_boolean,
    ((namespaces.STYLENS, 'punctuation-wrap'), None): cnv_string,
    ((namespaces.STYLENS, 'register-true'), None): cnv_boolean,
    ((namespaces.STYLENS, 'register-truth-ref-style-name'), None): cnv_string,
    ((namespaces.STYLENS, 'rel-column-width'), None): cnv_string,
    ((namespaces.STYLENS, 'rel-height'), None): cnv_string,
    ((namespaces.STYLENS, 'rel-width'), None): cnv_string,
    ((namespaces.STYLENS, 'repeat'), None): cnv_string,
    ((namespaces.STYLENS, 'repeat-content'), None): cnv_boolean,
    ((namespaces.STYLENS, 'rotation-align'), None): cnv_string,
    ((namespaces.STYLENS, 'rotation-angle'), None): cnv_string,
    ((namespaces.STYLENS, 'row-height'), None): cnv_string,
    ((namespaces.STYLENS, 'ruby-align'), None): cnv_string,
    ((namespaces.STYLENS, 'ruby-position'), None): cnv_string,
    ((namespaces.STYLENS, 'run-through'), None): cnv_string,
    ((namespaces.STYLENS, 'scale-to'), None): cnv_string,
    ((namespaces.STYLENS, 'scale-to-pages'), None): cnv_string,
    ((namespaces.STYLENS, 'script-type'), None): cnv_string,
    ((namespaces.STYLENS, 'shadow'), None): cnv_string,
    ((namespaces.STYLENS, 'shrink-to-fit'), None): cnv_boolean,
    ((namespaces.STYLENS, 'snap-to-layout-grid'), None): cnv_boolean,
    ((namespaces.STYLENS, 'style'), None): cnv_string,
    ((namespaces.STYLENS, 'style-name'), None): cnv_StyleNameRef,
    ((namespaces.STYLENS, 'tab-stop-distance'), None): cnv_string,
    ((namespaces.STYLENS, 'table-centering'), None): cnv_string,
    ((namespaces.STYLENS, 'text-align-source'), None): cnv_string,
    ((namespaces.STYLENS, 'text-autospace'), None): cnv_string,
    ((namespaces.STYLENS, 'text-blinking'), None): cnv_boolean,
    ((namespaces.STYLENS, 'text-combine'), None): cnv_string,
    ((namespaces.STYLENS, 'text-combine-end-char'), None): cnv_string,
    ((namespaces.STYLENS, 'text-combine-start-char'), None): cnv_string,
    ((namespaces.STYLENS, 'text-emphasize'), None): cnv_string,
    ((namespaces.STYLENS, 'text-line-through-color'), None): cnv_string,
    ((namespaces.STYLENS, 'text-line-through-mode'), None): cnv_string,
    ((namespaces.STYLENS, 'text-line-through-style'), None): cnv_string,
    ((namespaces.STYLENS, 'text-line-through-text'), None): cnv_string,
    ((namespaces.STYLENS, 'text-line-through-text-style'), None): cnv_string,
    ((namespaces.STYLENS, 'text-line-through-type'), None): cnv_string,
    ((namespaces.STYLENS, 'text-line-through-width'), None): cnv_string,
    ((namespaces.STYLENS, 'text-outline'), None): cnv_boolean,
    ((namespaces.STYLENS, 'text-position'), None): cnv_string,
    ((namespaces.STYLENS, 'text-rotation-angle'), None): cnv_string,
    ((namespaces.STYLENS, 'text-rotation-scale'), None): cnv_string,
    ((namespaces.STYLENS, 'text-scale'), None): cnv_string,
    ((namespaces.STYLENS, 'text-underline-color'), None): cnv_string,
    ((namespaces.STYLENS, 'text-underline-mode'), None): cnv_string,
    ((namespaces.STYLENS, 'text-underline-style'), None): cnv_string,
    ((namespaces.STYLENS, 'text-underline-type'), None): cnv_string,
    ((namespaces.STYLENS, 'text-underline-width'), None): cnv_string,
    ((namespaces.STYLENS, 'type'), None): cnv_string,
    ((namespaces.STYLENS, 'use-optimal-column-width'), None): cnv_boolean,
    ((namespaces.STYLENS, 'use-optimal-row-height'), None): cnv_boolean,
    ((namespaces.STYLENS, 'use-window-font-color'), None): cnv_boolean,
    ((namespaces.STYLENS, 'vertical-align'), None): cnv_string,
    ((namespaces.STYLENS, 'vertical-pos'), None): cnv_string,
    ((namespaces.STYLENS, 'vertical-rel'), None): cnv_string,
    ((namespaces.STYLENS, 'volatile'), None): cnv_boolean,
    ((namespaces.STYLENS, 'width'), None): cnv_string,
    ((namespaces.STYLENS, 'wrap'), None): cnv_string,
    ((namespaces.STYLENS, 'wrap-contour'), None): cnv_boolean,
    ((namespaces.STYLENS, 'wrap-contour-mode'), None): cnv_string,
    ((namespaces.STYLENS, 'wrap-dynamic-threshold'), None): cnv_length,
    ((namespaces.STYLENS, 'writing-mode-automatic'), None): cnv_boolean,
    ((namespaces.STYLENS, 'writing-mode'), None): cnv_string,
    ((namespaces.SVGNS, 'accent-height'), None): cnv_integer,
    ((namespaces.SVGNS, 'alphabetic'), None): cnv_integer,
    ((namespaces.SVGNS, 'ascent'), None): cnv_integer,
    ((namespaces.SVGNS, 'bbox'), None): cnv_string,
    ((namespaces.SVGNS, 'cap-height'), None): cnv_integer,
    ((namespaces.SVGNS, 'cx'), None): cnv_string,
    ((namespaces.SVGNS, 'cy'), None): cnv_string,
    ((namespaces.SVGNS, 'd'), None): cnv_string,
    ((namespaces.SVGNS, 'descent'), None): cnv_integer,
    ((namespaces.SVGNS, 'fill-rule'), None): cnv_string,
    ((namespaces.SVGNS, 'font-family'), None): cnv_string,
    ((namespaces.SVGNS, 'font-size'), None): cnv_string,
    ((namespaces.SVGNS, 'font-stretch'), None): cnv_string,
    ((namespaces.SVGNS, 'font-style'), None): cnv_string,
    ((namespaces.SVGNS, 'font-variant'), None): cnv_string,
    ((namespaces.SVGNS, 'font-weight'), None): cnv_string,
    ((namespaces.SVGNS, 'fx'), None): cnv_string,
    ((namespaces.SVGNS, 'fy'), None): cnv_string,
    ((namespaces.SVGNS, 'gradientTransform'), None): cnv_string,
    ((namespaces.SVGNS, 'gradientUnits'), None): cnv_string,
    ((namespaces.SVGNS, 'hanging'), None): cnv_integer,
    ((namespaces.SVGNS, 'height'), None): cnv_length,
    ((namespaces.SVGNS, 'ideographic'), None): cnv_integer,
    ((namespaces.SVGNS, 'mathematical'), None): cnv_integer,
    ((namespaces.SVGNS, 'name'), None): cnv_string,
    ((namespaces.SVGNS, 'offset'), None): cnv_string,
    ((namespaces.SVGNS, 'origin'), None): cnv_string,
    ((namespaces.SVGNS, 'overline-position'), None): cnv_integer,
    ((namespaces.SVGNS, 'overline-thickness'), None): cnv_integer,
    ((namespaces.SVGNS, 'panose-1'), None): cnv_string,
    ((namespaces.SVGNS, 'path'), None): cnv_string,
    ((namespaces.SVGNS, 'r'), None): cnv_length,
    ((namespaces.SVGNS, 'rx'), None): cnv_length,
    ((namespaces.SVGNS, 'ry'), None): cnv_length,
    ((namespaces.SVGNS, 'slope'), None): cnv_integer,
    ((namespaces.SVGNS, 'spreadMethod'), None): cnv_string,
    ((namespaces.SVGNS, 'stemh'), None): cnv_integer,
    ((namespaces.SVGNS, 'stemv'), None): cnv_integer,
    ((namespaces.SVGNS, 'stop-color'), None): cnv_string,
    ((namespaces.SVGNS, 'stop-opacity'), None): cnv_double,
    ((namespaces.SVGNS, 'strikethrough-position'), None): cnv_integer,
    ((namespaces.SVGNS, 'strikethrough-thickness'), None): cnv_integer,
    ((namespaces.SVGNS, 'string'), None): cnv_string,
    ((namespaces.SVGNS, 'stroke-color'), None): cnv_string,
    ((namespaces.SVGNS, 'stroke-opacity'), None): cnv_string,
    ((namespaces.SVGNS, 'stroke-width'), None): cnv_length,
    ((namespaces.SVGNS, 'type'), None): cnv_string,
    ((namespaces.SVGNS, 'underline-position'), None): cnv_integer,
    ((namespaces.SVGNS, 'underline-thickness'), None): cnv_integer,
    ((namespaces.SVGNS, 'unicode-range'), None): cnv_string,
    ((namespaces.SVGNS, 'units-per-em'), None): cnv_integer,
    ((namespaces.SVGNS, 'v-alphabetic'), None): cnv_integer,
    ((namespaces.SVGNS, 'v-hanging'), None): cnv_integer,
    ((namespaces.SVGNS, 'v-ideographic'), None): cnv_integer,
    ((namespaces.SVGNS, 'v-mathematical'), None): cnv_integer,
    ((namespaces.SVGNS, 'viewBox'), None): cnv_viewbox,
    ((namespaces.SVGNS, 'width'), None): cnv_length,
    ((namespaces.SVGNS, 'widths'), None): cnv_string,
    ((namespaces.SVGNS, 'x'), None): cnv_length,
    ((namespaces.SVGNS, 'x-height'), None): cnv_integer,
    ((namespaces.SVGNS, 'x1'), None): cnv_lengthorpercent,
    ((namespaces.SVGNS, 'x2'), None): cnv_lengthorpercent,
    ((namespaces.SVGNS, 'y'), None): cnv_length,
    ((namespaces.SVGNS, 'y1'), None): cnv_lengthorpercent,
    ((namespaces.SVGNS, 'y2'), None): cnv_lengthorpercent,
    ((namespaces.TABLENS, 'acceptance-state'), None): cnv_string,
    ((namespaces.TABLENS, 'add-empty-lines'), None): cnv_boolean,
    ((namespaces.TABLENS, 'algorithm'), None): cnv_formula,
    ((namespaces.TABLENS, 'align'), None): cnv_string,
    ((namespaces.TABLENS, 'allow-empty-cell'), None): cnv_boolean,
    ((namespaces.TABLENS, 'application-data'), None): cnv_string,
    ((namespaces.TABLENS, 'automatic-find-labels'), None): cnv_boolean,
    ((namespaces.TABLENS, 'base-cell-address'), None): cnv_string,
    ((namespaces.TABLENS, 'bind-styles-to-content'), None): cnv_boolean,
    ((namespaces.TABLENS, 'border-color'), None): cnv_string,
    ((namespaces.TABLENS, 'border-model'), None): cnv_string,
    ((namespaces.TABLENS, 'buttons'), None): cnv_string,
    ((namespaces.TABLENS, 'buttons'), None): cnv_string,
    ((namespaces.TABLENS, 'case-sensitive'), None): cnv_boolean,
    ((namespaces.TABLENS, 'case-sensitive'), None): cnv_string,
    ((namespaces.TABLENS, 'cell-address'), None): cnv_string,
    ((namespaces.TABLENS, 'cell-range-address'), None): cnv_string,
    ((namespaces.TABLENS, 'cell-range-address'), None): cnv_string,
    ((namespaces.TABLENS, 'cell-range'), None): cnv_string,
    ((namespaces.TABLENS, 'column'), None): cnv_integer,
    ((namespaces.TABLENS, 'comment'), None): cnv_string,
    ((namespaces.TABLENS, 'condition'), None): cnv_formula,
    ((namespaces.TABLENS, 'condition-source'), None): cnv_string,
    ((namespaces.TABLENS, 'condition-source-range-address'), None): cnv_string,
    ((namespaces.TABLENS, 'contains-error'), None): cnv_boolean,
    ((namespaces.TABLENS, 'contains-header'), None): cnv_boolean,
    ((namespaces.TABLENS, 'content-validation-name'), None): cnv_string,
    ((namespaces.TABLENS, 'copy-back'), None): cnv_boolean,
    ((namespaces.TABLENS, 'copy-formulas'), None): cnv_boolean,
    ((namespaces.TABLENS, 'copy-styles'), None): cnv_boolean,
    ((namespaces.TABLENS, 'count'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'country'), None): cnv_token,
    ((namespaces.TABLENS, 'data-cell-range-address'), None): cnv_string,
    ((namespaces.TABLENS, 'data-field'), None): cnv_string,
    ((namespaces.TABLENS, 'data-type'), None): cnv_string,
    ((namespaces.TABLENS, 'database-name'), None): cnv_string,
    ((namespaces.TABLENS, 'database-table-name'), None): cnv_string,
    ((namespaces.TABLENS, 'date-end'), None): cnv_string,
    ((namespaces.TABLENS, 'date-start'), None): cnv_string,
    ((namespaces.TABLENS, 'date-value'), None): cnv_date,
    ((namespaces.TABLENS, 'default-cell-style-name'), None): cnv_StyleNameRef,
    ((namespaces.TABLENS, 'direction'), None): cnv_string,
    ((namespaces.TABLENS, 'display-border'), None): cnv_boolean,
    ((namespaces.TABLENS, 'display'), None): cnv_boolean,
    ((namespaces.TABLENS, 'display-duplicates'), None): cnv_boolean,
    ((namespaces.TABLENS, 'display-filter-buttons'), None): cnv_boolean,
    ((namespaces.TABLENS, 'display-list'), None): cnv_string,
    ((namespaces.TABLENS, 'display-member-mode'), None): cnv_string,
    ((namespaces.TABLENS, 'drill-down-on-double-click'), None): cnv_boolean,
    ((namespaces.TABLENS, 'enabled'), None): cnv_boolean,
    ((namespaces.TABLENS, 'end-cell-address'), None): cnv_string,
    ((namespaces.TABLENS, 'end'), None): cnv_string,
    ((namespaces.TABLENS, 'end-column'), None): cnv_integer,
    ((namespaces.TABLENS, 'end-position'), None): cnv_integer,
    ((namespaces.TABLENS, 'end-row'), None): cnv_integer,
    ((namespaces.TABLENS, 'end-table'), None): cnv_integer,
    ((namespaces.TABLENS, 'end-x'), None): cnv_length,
    ((namespaces.TABLENS, 'end-y'), None): cnv_length,
    ((namespaces.TABLENS, 'execute'), None): cnv_boolean,
    ((namespaces.TABLENS, 'expression'), None): cnv_formula,
    ((namespaces.TABLENS, 'field-name'), None): cnv_string,
    ((namespaces.TABLENS, 'field-number'), None): cnv_nonNegativeInteger,
    ((namespaces.TABLENS, 'field-number'), None): cnv_string,
    ((namespaces.TABLENS, 'filter-name'), None): cnv_string,
    ((namespaces.TABLENS, 'filter-options'), None): cnv_string,
    ((namespaces.TABLENS, 'formula'), None): cnv_formula,
    ((namespaces.TABLENS, 'function'), None): cnv_string,
    ((namespaces.TABLENS, 'function'), None): cnv_string,
    ((namespaces.TABLENS, 'grand-total'), None): cnv_string,
    ((namespaces.TABLENS, 'group-by-field-number'), None): cnv_nonNegativeInteger,
    ((namespaces.TABLENS, 'grouped-by'), None): cnv_string,
    ((namespaces.TABLENS, 'has-persistent-data'), None): cnv_boolean,
    ((namespaces.TABLENS, 'id'), None): cnv_string,
    ((namespaces.TABLENS, 'identify-categories'), None): cnv_boolean,
    ((namespaces.TABLENS, 'ignore-empty-rows'), None): cnv_boolean,
    ((namespaces.TABLENS, 'index'), None): cnv_nonNegativeInteger,
    ((namespaces.TABLENS, 'is-active'), None): cnv_boolean,
    ((namespaces.TABLENS, 'is-data-layout-field'), None): cnv_string,
    ((namespaces.TABLENS, 'is-selection'), None): cnv_boolean,
    ((namespaces.TABLENS, 'is-sub-table'), None): cnv_boolean,
    ((namespaces.TABLENS, 'label-cell-range-address'), None): cnv_string,
    ((namespaces.TABLENS, 'language'), None): cnv_token,
    ((namespaces.TABLENS, 'language'), None): cnv_token,
    ((namespaces.TABLENS, 'last-column-spanned'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'last-row-spanned'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'layout-mode'), None): cnv_string,
    ((namespaces.TABLENS, 'link-to-source-data'), None): cnv_boolean,
    ((namespaces.TABLENS, 'marked-invalid'), None): cnv_boolean,
    ((namespaces.TABLENS, 'matrix-covered'), None): cnv_boolean,
    ((namespaces.TABLENS, 'maximum-difference'), None): cnv_double,
    ((namespaces.TABLENS, 'member-count'), None): cnv_nonNegativeInteger,
    ((namespaces.TABLENS, 'member-name'), None): cnv_string,
    ((namespaces.TABLENS, 'member-type'), None): cnv_string,
    ((namespaces.TABLENS, 'message-type'), None): cnv_string,
    ((namespaces.TABLENS, 'mode'), None): cnv_string,
    ((namespaces.TABLENS, 'multi-deletion-spanned'), None): cnv_integer,
    ((namespaces.TABLENS, 'name'), None): cnv_string,
    ((namespaces.TABLENS, 'name'), None): cnv_string,
    ((namespaces.TABLENS, 'null-year'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'number-columns-repeated'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'number-columns-spanned'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'number-matrix-columns-spanned'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'number-matrix-rows-spanned'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'number-rows-repeated'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'number-rows-spanned'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'object-name'), None): cnv_string,
    ((namespaces.TABLENS, 'on-update-keep-size'), None): cnv_boolean,
    ((namespaces.TABLENS, 'on-update-keep-styles'), None): cnv_boolean,
    ((namespaces.TABLENS, 'operator'), None): cnv_string,
    ((namespaces.TABLENS, 'operator'), None): cnv_string,
    ((namespaces.TABLENS, 'order'), None): cnv_string,
    ((namespaces.TABLENS, 'orientation'), None): cnv_string,
    ((namespaces.TABLENS, 'orientation'), None): cnv_string,
    ((namespaces.TABLENS, 'page-breaks-on-group-change'), None): cnv_boolean,
    ((namespaces.TABLENS, 'parse-sql-statement'), None): cnv_boolean,
    ((namespaces.TABLENS, 'password'), None): cnv_string,
    ((namespaces.TABLENS, 'position'), None): cnv_integer,
    ((namespaces.TABLENS, 'precision-as-shown'), None): cnv_boolean,
    ((namespaces.TABLENS, 'print'), None): cnv_boolean,
    ((namespaces.TABLENS, 'print-ranges'), None): cnv_string,
    ((namespaces.TABLENS, 'protect'), None): cnv_boolean,
    ((namespaces.TABLENS, 'protected'), None): cnv_boolean,
    ((namespaces.TABLENS, 'protection-key'), None): cnv_string,
    ((namespaces.TABLENS, 'query-name'), None): cnv_string,
    ((namespaces.TABLENS, 'range-usable-as'), None): cnv_string,
    ((namespaces.TABLENS, 'refresh-delay'), None): cnv_boolean,
    ((namespaces.TABLENS, 'refresh-delay'), None): cnv_duration,
    ((namespaces.TABLENS, 'rejecting-change-id'), None): cnv_string,
    ((namespaces.TABLENS, 'row'), None): cnv_integer,
    ((namespaces.TABLENS, 'scenario-ranges'), None): cnv_string,
    ((namespaces.TABLENS, 'search-criteria-must-apply-to-whole-cell'), None): cnv_boolean,
    ((namespaces.TABLENS, 'selected-page'), None): cnv_string,
    ((namespaces.TABLENS, 'show-details'), None): cnv_boolean,
    ((namespaces.TABLENS, 'show-empty'), None): cnv_boolean,
    ((namespaces.TABLENS, 'show-empty'), None): cnv_string,
    ((namespaces.TABLENS, 'show-filter-button'), None): cnv_boolean,
    ((namespaces.TABLENS, 'sort-mode'), None): cnv_string,
    ((namespaces.TABLENS, 'source-cell-range-addresses'), None): cnv_string,
    ((namespaces.TABLENS, 'source-cell-range-addresses'), None): cnv_string,
    ((namespaces.TABLENS, 'source-field-name'), None): cnv_string,
    ((namespaces.TABLENS, 'source-field-name'), None): cnv_string,
    ((namespaces.TABLENS, 'source-name'), None): cnv_string,
    ((namespaces.TABLENS, 'sql-statement'), None): cnv_string,
    ((namespaces.TABLENS, 'start'), None): cnv_string,
    ((namespaces.TABLENS, 'start-column'), None): cnv_integer,
    ((namespaces.TABLENS, 'start-position'), None): cnv_integer,
    ((namespaces.TABLENS, 'start-row'), None): cnv_integer,
    ((namespaces.TABLENS, 'start-table'), None): cnv_integer,
    ((namespaces.TABLENS, 'status'), None): cnv_string,
    ((namespaces.TABLENS, 'step'), None): cnv_double,
    ((namespaces.TABLENS, 'steps'), None): cnv_positiveInteger,
    ((namespaces.TABLENS, 'structure-protected'), None): cnv_boolean,
    ((namespaces.TABLENS, 'style-name'), None): cnv_StyleNameRef,
    ((namespaces.TABLENS, 'table-background'), None): cnv_boolean,
    ((namespaces.TABLENS, 'table'), None): cnv_integer,
    ((namespaces.TABLENS, 'table-name'), None): cnv_string,
    ((namespaces.TABLENS, 'target-cell-address'), None): cnv_string,
    ((namespaces.TABLENS, 'target-cell-address'), None): cnv_string,
    ((namespaces.TABLENS, 'target-range-address'), None): cnv_string,
    ((namespaces.TABLENS, 'target-range-address'), None): cnv_string,
    ((namespaces.TABLENS, 'title'), None): cnv_string,
    ((namespaces.TABLENS, 'track-changes'), None): cnv_boolean,
    ((namespaces.TABLENS, 'type'), None): cnv_string,
    ((namespaces.TABLENS, 'use-labels'), None): cnv_string,
    ((namespaces.TABLENS, 'use-regular-expressions'), None): cnv_boolean,
    ((namespaces.TABLENS, 'used-hierarchy'), None): cnv_integer,
    ((namespaces.TABLENS, 'user-name'), None): cnv_string,
    ((namespaces.TABLENS, 'value'), None): cnv_string,
    ((namespaces.TABLENS, 'value'), None): cnv_string,
    ((namespaces.TABLENS, 'value-type'), None): cnv_string,
    ((namespaces.TABLENS, 'visibility'), None): cnv_string,
    ((namespaces.TEXTNS, 'active'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'address'), None): cnv_string,
    ((namespaces.TEXTNS, 'alphabetical-separators'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'anchor-page-number'), None): cnv_positiveInteger,
    ((namespaces.TEXTNS, 'anchor-type'), None): cnv_string,
    ((namespaces.TEXTNS, 'animation'), None): cnv_string,
    ((namespaces.TEXTNS, 'animation-delay'), None): cnv_string,
    ((namespaces.TEXTNS, 'animation-direction'), None): cnv_string,
    ((namespaces.TEXTNS, 'animation-repeat'), None): cnv_string,
    ((namespaces.TEXTNS, 'animation-start-inside'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'animation-steps'), None): cnv_length,
    ((namespaces.TEXTNS, 'animation-stop-inside'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'annote'), None): cnv_string,
    ((namespaces.TEXTNS, 'author'), None): cnv_string,
    ((namespaces.TEXTNS, 'bibliography-data-field'), None): cnv_string,
    ((namespaces.TEXTNS, 'bibliography-type'), None): cnv_string,
    ((namespaces.TEXTNS, 'booktitle'), None): cnv_string,
    ((namespaces.TEXTNS, 'bullet-char'), None): cnv_string,
    ((namespaces.TEXTNS, 'bullet-relative-size'), None): cnv_string,
    ((namespaces.TEXTNS, 'c'), None): cnv_nonNegativeInteger,
    ((namespaces.TEXTNS, 'capitalize-entries'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'caption-sequence-format'), None): cnv_string,
    ((namespaces.TEXTNS, 'caption-sequence-name'), None): cnv_string,
    ((namespaces.TEXTNS, 'change-id'), None): cnv_IDREF,
    ((namespaces.TEXTNS, 'chapter'), None): cnv_string,
    ((namespaces.TEXTNS, 'citation-body-style-name'), None): cnv_StyleNameRef,
    ((namespaces.TEXTNS, 'citation-style-name'), None): cnv_StyleNameRef,
    ((namespaces.TEXTNS, 'class-names'), None): cnv_NCNames,
    ((namespaces.TEXTNS, 'column-name'), None): cnv_string,
    ((namespaces.TEXTNS, 'combine-entries'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'combine-entries-with-dash'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'combine-entries-with-pp'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'comma-separated'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'cond-style-name'), None): cnv_StyleNameRef,
    ((namespaces.TEXTNS, 'condition'), None): cnv_formula,
    ((namespaces.TEXTNS, 'connection-name'), None): cnv_string,
    ((namespaces.TEXTNS, 'consecutive-numbering'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'continue-numbering'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'copy-outline-levels'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'count-empty-lines'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'count-in-text-boxes'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'current-value'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'custom1'), None): cnv_string,
    ((namespaces.TEXTNS, 'custom2'), None): cnv_string,
    ((namespaces.TEXTNS, 'custom3'), None): cnv_string,
    ((namespaces.TEXTNS, 'custom4'), None): cnv_string,
    ((namespaces.TEXTNS, 'custom5'), None): cnv_string,
    ((namespaces.TEXTNS, 'database-name'), None): cnv_string,
    ((namespaces.TEXTNS, 'date-adjust'), None): cnv_duration,
    ((namespaces.TEXTNS, 'date-value'), None): cnv_date,
    # ((TEXTNS,u'date-value'), None): cnv_dateTime,
    ((namespaces.TEXTNS, 'default-style-name'), None): cnv_StyleNameRef,
    ((namespaces.TEXTNS, 'description'), None): cnv_string,
    ((namespaces.TEXTNS, 'display'), None): cnv_string,
    ((namespaces.TEXTNS, 'display-levels'), None): cnv_positiveInteger,
    ((namespaces.TEXTNS, 'display-outline-level'), None): cnv_nonNegativeInteger,
    ((namespaces.TEXTNS, 'dont-balance-text-columns'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'duration'), None): cnv_duration,
    ((namespaces.TEXTNS, 'edition'), None): cnv_string,
    ((namespaces.TEXTNS, 'editor'), None): cnv_string,
    ((namespaces.TEXTNS, 'filter-name'), None): cnv_string,
    ((namespaces.TEXTNS, 'first-row-end-column'), None): cnv_string,
    ((namespaces.TEXTNS, 'first-row-start-column'), None): cnv_string,
    ((namespaces.TEXTNS, 'fixed'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'footnotes-position'), None): cnv_string,
    ((namespaces.TEXTNS, 'formula'), None): cnv_formula,
    ((namespaces.TEXTNS, 'global'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'howpublished'), None): cnv_string,
    ((namespaces.TEXTNS, 'id'), None): cnv_ID,
    # ((TEXTNS,u'id'), None): cnv_string,
    ((namespaces.TEXTNS, 'identifier'), None): cnv_string,
    ((namespaces.TEXTNS, 'ignore-case'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'increment'), None): cnv_nonNegativeInteger,
    ((namespaces.TEXTNS, 'index-name'), None): cnv_string,
    ((namespaces.TEXTNS, 'index-scope'), None): cnv_string,
    ((namespaces.TEXTNS, 'institution'), None): cnv_string,
    ((namespaces.TEXTNS, 'is-hidden'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'is-list-header'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'isbn'), None): cnv_string,
    ((namespaces.TEXTNS, 'issn'), None): cnv_string,
    ((namespaces.TEXTNS, 'issn'), None): cnv_string,
    ((namespaces.TEXTNS, 'journal'), None): cnv_string,
    ((namespaces.TEXTNS, 'key'), None): cnv_string,
    ((namespaces.TEXTNS, 'key1'), None): cnv_string,
    ((namespaces.TEXTNS, 'key1-phonetic'), None): cnv_string,
    ((namespaces.TEXTNS, 'key2'), None): cnv_string,
    ((namespaces.TEXTNS, 'key2-phonetic'), None): cnv_string,
    ((namespaces.TEXTNS, 'kind'), None): cnv_string,
    ((namespaces.TEXTNS, 'label'), None): cnv_string,
    ((namespaces.TEXTNS, 'last-row-end-column'), None): cnv_string,
    ((namespaces.TEXTNS, 'last-row-start-column'), None): cnv_string,
    ((namespaces.TEXTNS, 'level'), None): cnv_positiveInteger,
    ((namespaces.TEXTNS, 'line-break'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'line-number'), None): cnv_string,
    ((namespaces.TEXTNS, 'main-entry'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'main-entry-style-name'), None): cnv_StyleNameRef,
    ((namespaces.TEXTNS, 'master-page-name'), None): cnv_StyleNameRef,
    ((namespaces.TEXTNS, 'min-label-distance'), None): cnv_string,
    ((namespaces.TEXTNS, 'min-label-width'), None): cnv_string,
    ((namespaces.TEXTNS, 'month'), None): cnv_string,
    ((namespaces.TEXTNS, 'name'), None): cnv_string,
    ((namespaces.TEXTNS, 'note-class'), None): cnv_textnoteclass,
    ((namespaces.TEXTNS, 'note'), None): cnv_string,
    ((namespaces.TEXTNS, 'number'), None): cnv_string,
    ((namespaces.TEXTNS, 'number-lines'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'number-position'), None): cnv_string,
    ((namespaces.TEXTNS, 'numbered-entries'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'offset'), None): cnv_string,
    ((namespaces.TEXTNS, 'organizations'), None): cnv_string,
    ((namespaces.TEXTNS, 'outline-level'), None): cnv_string,
    ((namespaces.TEXTNS, 'page-adjust'), None): cnv_integer,
    ((namespaces.TEXTNS, 'pages'), None): cnv_string,
    ((namespaces.TEXTNS, 'paragraph-style-name'), None): cnv_StyleNameRef,
    ((namespaces.TEXTNS, 'placeholder-type'), None): cnv_string,
    ((namespaces.TEXTNS, 'prefix'), None): cnv_string,
    ((namespaces.TEXTNS, 'protected'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'protection-key'), None): cnv_string,
    ((namespaces.TEXTNS, 'publisher'), None): cnv_string,
    ((namespaces.TEXTNS, 'ref-name'), None): cnv_string,
    ((namespaces.TEXTNS, 'reference-format'), None): cnv_string,
    ((namespaces.TEXTNS, 'relative-tab-stop-position'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'report-type'), None): cnv_string,
    ((namespaces.TEXTNS, 'restart-numbering'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'restart-on-page'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'row-number'), None): cnv_nonNegativeInteger,
    ((namespaces.TEXTNS, 'school'), None): cnv_string,
    ((namespaces.TEXTNS, 'section-name'), None): cnv_string,
    ((namespaces.TEXTNS, 'select-page'), None): cnv_string,
    ((namespaces.TEXTNS, 'separation-character'), None): cnv_string,
    ((namespaces.TEXTNS, 'series'), None): cnv_string,
    ((namespaces.TEXTNS, 'sort-algorithm'), None): cnv_string,
    ((namespaces.TEXTNS, 'sort-ascending'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'sort-by-position'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'space-before'), None): cnv_string,
    ((namespaces.TEXTNS, 'start-numbering-at'), None): cnv_string,
    ((namespaces.TEXTNS, 'start-value'), None): cnv_nonNegativeInteger,
    ((namespaces.TEXTNS, 'start-value'), None): cnv_positiveInteger,
    ((namespaces.TEXTNS, 'string-value'), None): cnv_string,
    ((namespaces.TEXTNS, 'string-value-if-false'), None): cnv_string,
    ((namespaces.TEXTNS, 'string-value-if-true'), None): cnv_string,
    ((namespaces.TEXTNS, 'string-value-phonetic'), None): cnv_string,
    ((namespaces.TEXTNS, 'style-name'), None): cnv_StyleNameRef,
    ((namespaces.TEXTNS, 'suffix'), None): cnv_string,
    ((namespaces.TEXTNS, 'tab-ref'), None): cnv_nonNegativeInteger,
    ((namespaces.TEXTNS, 'table-name'), None): cnv_string,
    ((namespaces.TEXTNS, 'table-type'), None): cnv_string,
    ((namespaces.TEXTNS, 'time-adjust'), None): cnv_duration,
    ((namespaces.TEXTNS, 'time-value'), None): cnv_dateTime,
    ((namespaces.TEXTNS, 'time-value'), None): cnv_time,
    ((namespaces.TEXTNS, 'title'), None): cnv_string,
    ((namespaces.TEXTNS, 'track-changes'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'url'), None): cnv_string,
    ((namespaces.TEXTNS, 'use-caption'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-chart-objects'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-draw-objects'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-floating-frames'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-graphics'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-index-marks'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-index-source-styles'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-keys-as-entries'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-math-objects'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-objects'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-other-objects'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-outline-level'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-soft-page-breaks'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-spreadsheet-objects'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'use-tables'), None): cnv_boolean,
    ((namespaces.TEXTNS, 'value'), None): cnv_nonNegativeInteger,
    ((namespaces.TEXTNS, 'visited-style-name'), None): cnv_StyleNameRef,
    ((namespaces.TEXTNS, 'volume'), None): cnv_string,
    ((namespaces.TEXTNS, 'year'), None): cnv_string,
    ((namespaces.XFORMSNS, 'bind'), None): cnv_string,
    ((namespaces.XLINKNS, 'actuate'), None): cnv_string,
    ((namespaces.XLINKNS, 'href'), None): cnv_anyURI,
    ((namespaces.XLINKNS, 'show'), None): cnv_xlinkshow,
    ((namespaces.XLINKNS, 'title'), None): cnv_string,
    ((namespaces.XLINKNS, 'type'), None): cnv_string,
}


class AttrConverters:
    def convert(self, attribute, value, element):
        """ Based on the element, figures out how to check/convert the attribute value
            All values are converted to string
        """
        conversion = attrconverters.get((attribute, element.qname), None)
        if conversion is not None:
            return conversion(attribute, value, element)
        else:
            conversion = attrconverters.get((attribute, None), None)
            if conversion is not None:
                return conversion(attribute, value, element)
        return str(value)
