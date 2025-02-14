from __future__ import annotations

import sys

from dxtbx.format.FormatSMVADSC import FormatSMVADSC


class FormatSMVADSCmlfsom(FormatSMVADSC):
    """A class for reading SMV::ADSC-format images generated by MLFSOM
    simulation."""

    @staticmethod
    def understand(image_file):

        size, header = FormatSMVADSC.get_smv_header(image_file)

        unwanted_header_items = ["TIME", "DATE"]

        for header_item in unwanted_header_items:
            if header_item in header:
                return False

        return True

    def _scan(self):
        """Return the scan information for this image."""

        exposure_time = 1.0  # dummy argument; ought to be explicitly output by MLFSOM!
        epoch = None

        # assert(epoch)
        osc_start = float(self._header_dictionary["OSC_START"])
        osc_range = float(self._header_dictionary["OSC_RANGE"])

        return self._scan_factory.single_file(
            self._image_file, exposure_time, osc_start, osc_range, epoch
        )


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(FormatSMVADSCmlfsom.understand(arg))
