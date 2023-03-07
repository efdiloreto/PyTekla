import inspect

import pytest
from Tekla.Structures import TeklaStructuresSettings
from Tekla.Structures.Analysis import AnalysisBeamEnd
from Tekla.Structures.Drawing import Arc, DrawingHandler, GADrawing
from Tekla.Structures.Geometry3d import Point
from Tekla.Structures.Model import Assembly, Beam, BoltArray, Model

from pytekla import (
    BaseWrapper,
    DrawingDbObjectWrapper,
    DrawingHandlerWrapper,
    ModelObjectWrapper,
    ModelWrapper,
    wrap,
)


@pytest.mark.parametrize(
    "tekla_object, wrapper_type, tekla_type, detect_type",
    [
        (Point(), BaseWrapper, Point, True),
        ("Geometry3d.Point", BaseWrapper, Point, True),
        (Model(), ModelWrapper, Model, True),
        ("Model.Model", ModelWrapper, Model, True),
        (Beam(), ModelObjectWrapper, Beam, True),
        ("Model.Beam", ModelObjectWrapper, Beam, True),
        (BoltArray(), ModelObjectWrapper, BoltArray, True),
        ("Model.BoltArray", ModelObjectWrapper, BoltArray, True),
        (Assembly(), ModelObjectWrapper, Assembly, True),
        ("Model.Assembly", ModelObjectWrapper, Assembly, True),
        (TeklaStructuresSettings(), BaseWrapper, TeklaStructuresSettings, True),
        ("TeklaStructuresSettings", BaseWrapper, TeklaStructuresSettings, True),
        (AnalysisBeamEnd(), BaseWrapper, AnalysisBeamEnd, True),
        ("Analysis.AnalysisBeamEnd", BaseWrapper, AnalysisBeamEnd, True),
        (GADrawing(), DrawingDbObjectWrapper, GADrawing, True),
        ("Drawing.GADrawing", DrawingDbObjectWrapper, GADrawing, True),
        (DrawingHandler(), DrawingHandlerWrapper, DrawingHandler, True),
        ("Drawing.DrawingHandler", DrawingHandlerWrapper, DrawingHandler, True),
        (Arc(), DrawingDbObjectWrapper, Arc, True),
        ("Drawing.Arc", DrawingDbObjectWrapper, Arc, True),
        (Beam.BeamTypeEnum, Beam.BeamTypeEnum, Beam.BeamTypeEnum, True),
        ("random string", str, str, False),
        (4, int, int, False),
        ({"key1": 34, "key2": 56}, dict, dict, False),
        ([1, 2, 3, 4], list, list, False),
    ],
)
def test_wrapper_objects_creation(tekla_object, wrapper_type, tekla_type, detect_type):
    wrapped_object = wrap(tekla_object, detect_type)
    if inspect.isclass(tekla_object):
        assert str(tekla_object) == str(wrapper_type)
    else:
        assert isinstance(wrapped_object, wrapper_type)
        if detect_type:
            assert isinstance(wrapped_object.unwrap(), tekla_type)
