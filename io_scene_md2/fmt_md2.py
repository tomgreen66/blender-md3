from math import pi, sin, cos, atan2, acos

from .utils import AnyStruct


def string_from_bytes(b):
    return b.rstrip(b'\0').decode('utf-8', errors='ignore')


def string_to_bytes(s):
    return s.encode('utf-8')


def decode_normal(b):
    lat = b[0] / 255.0 * 2 * pi
    lon = b[1] / 255.0 * 2 * pi
    x = cos(lat) * sin(lon)
    y = sin(lat) * sin(lon)
    z = cos(lon)
    return (x, y, z)


def encode_normal(n):
    x, y, z = n
    if x == 0 and y == 0:
        return bytes((0, 0)) if z > 0 else bytes((128, 0))
    lon = int(atan2(y, x) * 255 / (2 * pi)) & 255
    lat = int(acos(z) * 255 / (2 * pi)) & 255
    return bytes((lat, lon))


VERTEX_SCALE = 64.0


def decode_vertex(v):
    return v / VERTEX_SCALE


def encode_vertex(v):
    return int(v * VERTEX_SCALE)


def texcoord_inverted(v):
    return 1.0 - v


Header = AnyStruct('Header', (
    ('magic', '4s'),
    ('version', 'i'),
    ('skinwidth', 'i'),
    ('skinheight', 'i'),
    ('framesize', 'i'),
    ('nSkins', 'i'),
    ('nVerts', 'i'),
    ('nTexCoords', 'i'),
    ('nTris', 'i'),
    ('nGlCmds', 'i'),
    ('nFrames', 'i'),
    ('offSkins', 'i'),
    ('offTexCoords', 'i'),
    ('offTris', 'i'),
    ('offFrames', 'i'),
    ('offGlCmds', 'i'),
    ('offEnd', 'i'),
))

Skin = AnyStruct('Skin', (
    ('name', '64s', 1, string_from_bytes, string_to_bytes),
))

TexCoord = AnyStruct('TexCoord', (
    ('s', 'h'),
    ('t', 'h')
))

Tri = AnyStruct('Tri', (
    ('vertex', '3H', 3),
    ('st', '3H', 3)
))

Vert = AnyStruct('Vert', (
    ('v', '3B', 3),
    ('normalIndex', 'B')
))

Frame = AnyStruct('Frame', (
    ('scale', '3f', 3),
    ('translate', '3f', 3),
    ('name', '16s', 1, string_from_bytes, string_to_bytes)
# Should be list of vertices here using nVerts
))

GlCmd = AnyStruct('GlCmd', (
    ('s', 'f'),
    ('t', 'f'),
    ('index', 'i')
))

MAGIC = b'IDP2'
VERSION = 8
