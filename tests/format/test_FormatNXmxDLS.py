from __future__ import annotations

import os

import pytest

from dxtbx.format.FormatNXmxDLS import FormatNXmxDLS
from dxtbx.model.experiment_list import ExperimentListFactory
from dxtbx.model.goniometer import Goniometer

pytestmark = pytest.mark.skipif(
    not os.access("/dls/mx/data/mx21314/mx21314-27/VMXi-AB0816/well_7/images", os.R_OK),
    reason="Test images not available",
)

pytest.importorskip("h5py")


def test_VMXi_rotation_scan():
    master_h5 = "/dls/mx/data/nt24686/nt24686-96/VMXi-AB5623/well_47/images/image_54771_master.h5"
    assert FormatNXmxDLS.understand(master_h5)

    expts = ExperimentListFactory.from_filenames([master_h5])
    imageset = expts[0].imageset
    assert imageset.get_format_class() == FormatNXmxDLS

    detector = imageset.get_detector()
    gonio = imageset.get_goniometer()
    scan = imageset.get_scan()
    beam = imageset.get_beam()

    panel = detector[0]
    assert panel.get_pixel_size() == (0.075, 0.075)
    assert (
        tuple(reversed(panel.get_image_size())) == imageset[0][0].all() == (2162, 2068)
    )
    assert panel.get_trusted_range() == (0, 23315)
    assert panel.get_fast_axis() == (1, 0, 0)
    assert panel.get_slow_axis() == (0, -1, 0)
    assert panel.get_origin() == pytest.approx((-79.155, 87.4875, -183.1849844439))
    assert panel.get_distance() == pytest.approx(183.1849844439)

    assert isinstance(gonio, Goniometer)
    assert gonio.get_rotation_axis() == (0, 1, 0)
    assert gonio.get_fixed_rotation() == (1, 0, 0, 0, 1, 0, 0, 0, 1)
    assert gonio.get_setting_rotation() == (1, 0, 0, 0, 1, 0, 0, 0, 1)

    assert scan.get_oscillation() == pytest.approx((-30, 0.1))
    assert scan.get_image_range() == (1, 600)

    assert beam.get_wavelength() == pytest.approx(0.7749042569928773)
    assert beam.get_s0() == pytest.approx((0, 0, -1 / beam.get_wavelength()))
