# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Spr(KaitaiStruct):
    """Quake's sprite format. Also supports QTest, Quake 2, Darkplaces and
    Half-Life sprites.
    
    Origin of this file: https://github.com/erysdren/Formats
    """

    class SprMagics(Enum):
        ids2 = 844317769
        idsp = 1347634249

    class SprTypes(Enum):
        parallel_upright = 0
        facing_upright = 1
        parallel = 2
        oriented = 3
        parallel_oriented = 4

    class SprRenderTypes(Enum):
        normal = 0
        additive = 1
        index_alpha = 2
        alphatest = 3

    class SprFrameType(Enum):
        single = 0
        group = 1
        angled = 2

    class SprSyncType(Enum):
        sync = 0
        rand = 1

    class SprVersions(Enum):
        spr = 1
        sp2 = 2
        spr32 = 32
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = KaitaiStream.resolve_enum(Spr.SprMagics, self._io.read_u4le())
        self.version = KaitaiStream.resolve_enum(Spr.SprVersions, self._io.read_u4le())
        if  ((self.magic == Spr.SprMagics.idsp) and (self.version == Spr.SprVersions.spr)) :
            self.data_spr = Spr.SprData(self._io, self, self._root)

        if  ((self.magic == Spr.SprMagics.ids2) and (self.version == Spr.SprVersions.sp2)) :
            self.data_sp2 = Spr.Sp2Data(self._io, self, self._root)

        if  ((self.magic == Spr.SprMagics.idsp) and (self.version == Spr.SprVersions.spr32)) :
            self.data_spr32 = Spr.Spr32Data(self._io, self, self._root)

        if  ((self.magic == Spr.SprMagics.idsp) and (self.version == Spr.SprVersions.sp2)) :
            self.data_hlspr = Spr.HlsprData(self._io, self, self._root)


    class Rgb(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.r = self._io.read_u1()
            self.g = self._io.read_u1()
            self.b = self._io.read_u1()


    class HlsprData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = KaitaiStream.resolve_enum(Spr.SprTypes, self._io.read_u4le())
            self.render_type = KaitaiStream.resolve_enum(Spr.SprRenderTypes, self._io.read_u4le())
            self.bounding_radius = self._io.read_f4le()
            self.size = Spr.Vec2i(self._io, self, self._root)
            self.num_frames = self._io.read_u4le()
            self.beam_length = self._io.read_f4le()
            self.sync_type = KaitaiStream.resolve_enum(Spr.SprSyncType, self._io.read_u4le())
            self.len_palette = self._io.read_u2le()
            self.palette = []
            for i in range(self.len_palette):
                self.palette.append(Spr.Rgb(self._io, self, self._root))

            self.frames = []
            for i in range(self.num_frames):
                self.frames.append(Spr.SprFrame(self._io, self, self._root))



    class Spr32Subframe(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.origin = Spr.Vec2i(self._io, self, self._root)
            self.size = Spr.Vec2i(self._io, self, self._root)
            self.pixels = self._io.read_bytes(((self.size.x * self.size.y) * 4))


    class Rgba(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.r = self._io.read_u1()
            self.g = self._io.read_u1()
            self.b = self._io.read_u1()
            self.a = self._io.read_u1()


    class Vec2i(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_s4le()
            self.y = self._io.read_s4le()


    class Spr32Data(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = KaitaiStream.resolve_enum(Spr.SprTypes, self._io.read_u4le())
            self.bounding_radius = self._io.read_f4le()
            self.size = Spr.Vec2i(self._io, self, self._root)
            self.num_frames = self._io.read_u4le()
            self.beam_length = self._io.read_f4le()
            self.sync_type = KaitaiStream.resolve_enum(Spr.SprSyncType, self._io.read_u4le())
            self.frames = []
            for i in range(self.num_frames):
                self.frames.append(Spr.SprFrame(self._io, self, self._root))



    class SprSubframe(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.origin = Spr.Vec2i(self._io, self, self._root)
            self.size = Spr.Vec2i(self._io, self, self._root)
            self.pixels = self._io.read_bytes((self.size.x * self.size.y))


    class SprFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = KaitaiStream.resolve_enum(Spr.SprFrameType, self._io.read_u4le())
            if self.is_grouped_frame:
                self.num_subframes = self._io.read_u4le()

            if self.is_grouped_frame:
                self.intervals = []
                for i in range(self.num_subframes):
                    self.intervals.append(self._io.read_f4le())


            self.subframes = []
            for i in range((self.num_subframes if self.is_grouped_frame else 1)):
                _on = self._root.version
                if _on == Spr.SprVersions.spr32:
                    self.subframes.append(Spr.Spr32Subframe(self._io, self, self._root))
                else:
                    self.subframes.append(Spr.SprSubframe(self._io, self, self._root))


        @property
        def is_grouped_frame(self):
            if hasattr(self, '_m_is_grouped_frame'):
                return self._m_is_grouped_frame

            self._m_is_grouped_frame =  ((self.type == Spr.SprFrameType.group) or (self.type == Spr.SprFrameType.angled)) 
            return getattr(self, '_m_is_grouped_frame', None)


    class SprData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = KaitaiStream.resolve_enum(Spr.SprTypes, self._io.read_u4le())
            self.bounding_radius = self._io.read_f4le()
            self.size = Spr.Vec2i(self._io, self, self._root)
            self.num_frames = self._io.read_u4le()
            self.beam_length = self._io.read_f4le()
            self.sync_type = KaitaiStream.resolve_enum(Spr.SprSyncType, self._io.read_u4le())
            self.frames = []
            for i in range(self.num_frames):
                self.frames.append(Spr.SprFrame(self._io, self, self._root))



    class Sp2Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = Spr.Vec2i(self._io, self, self._root)
            self.origin = Spr.Vec2i(self._io, self, self._root)
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(64), 0, False)).decode(u"ascii")


    class Sp2Data(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_frames = self._io.read_u4le()
            self.frames = []
            for i in range(self.num_frames):
                self.frames.append(Spr.Sp2Frame(self._io, self, self._root))




