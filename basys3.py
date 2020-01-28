import os
import subprocess

from nmigen.build import Platform, Resource, Pins, PinsN, Clock, Attrs, Connector, Subsignal
from nmigen.build.run import LocalBuildProducts
from nmigen.cli import main_parser, main_runner
from nmigen.vendor.xilinx_7series import Xilinx7SeriesPlatform
from nmigen_boards.resources import SPIFlashResources

__all__ = ["Basys3Platform"]

class Basys3Platform(Xilinx7SeriesPlatform):
    device = "xc7a35t"
    package = "cpg236"

    speed = "1"

    default_clk = "CLK100"

    # J connectors are layed out looking at the connector head-on [6-1],[12-7]
    # J[A(0), B(1), C(2), XADC(3)]
    connectors = [

        # JA
        Connector(
            "J",
            0,
            " - - G2 J2 L2 J1 "
            " - - G3 H2 K2 H1 "
        ),

        # JB
        Connector(
            "J",
            1,
            " - - B16 B15 A16 A14 "
            " - - C16 C15 A17 A15 "
        ),

        # JC
        Connector(
            "J",
            2,
            " - - P18 N17 M18 K17 "
            " - - R18 P17 M19 L17 "
        ),

        # JXADC
        Connector(
            "J",
            3,
            " - - N2 M2 L3 J3 "
            " - - N1 M1 M3 K3 "
        ),

    ]

    resources = [

        # Integrated 100MHz clock
        Resource("CLK100", 0, Pins("W5", dir="i"), Clock(100e6), Attrs(IOSTANDARD="LVCMOS33")),

        # Onboard LEDs: LD[0-15]
        Resource("LD", 0, Pins("U16", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 1, Pins("E19", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 2, Pins("U19", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 3, Pins("V19", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 4, Pins("W18", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 5, Pins("U15", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 6, Pins("U14", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 7, Pins("V14", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 8, Pins("V13", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 9, Pins("V3", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 10, Pins("W3", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 11, Pins("U3", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 12, Pins("P3", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 13, Pins("N3", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 14, Pins("P1", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("LD", 15, Pins("L1", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),

        # Onboard switches: SW[0-15]
        Resource("SW", 0, Pins("V17", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 1, Pins("V16", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 2, Pins("W16", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 3, Pins("W17", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 4, Pins("W15", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 5, Pins("V15", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 6, Pins("W14", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 7, Pins("W13", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 8, Pins("V2", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 9, Pins("T3", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 10, Pins("T2", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 11, Pins("R3", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 12, Pins("W2", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 13, Pins("U1", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 14, Pins("T1", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("SW", 15, Pins("R2", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        # Onboard buttons: BTN[L(0),R(1),U(2),D(3),C(4)]
        Resource("BTN", 0, Pins("W19", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("BTN", 1, Pins("T17", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("BTN", 2, Pins("T18", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("BTN", 3, Pins("U17", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("BTN", 4, Pins("U18", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        # 7seg anode/cathodes: AN[0-3] C[A(0),B(1),C(2),D(3),E(4),F(5),G(6),P(7)]
        Resource("7SEG", 0,
            Subsignal("AN0", Pins("U2", dir="o")),
            Subsignal("AN1", Pins("U4", dir="o")),
            Subsignal("AN2", Pins("V4", dir="o")),
            Subsignal("AN3", Pins("W4", dir="o")),
            Subsignal("CA", PinsN("W7", dir="o")),
            Subsignal("CB", PinsN("W6", dir="o")),
            Subsignal("CC", PinsN("U8", dir="o")),
            Subsignal("CD", PinsN("V8", dir="o")),
            Subsignal("CE", PinsN("U5", dir="o")),
            Subsignal("CF", PinsN("V5", dir="o")),
            Subsignal("CG", PinsN("U7", dir="o")),
            Subsignal("CP", PinsN("V7", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # VGA port
        Resource("VGA", 0,
            Subsignal("RED0", Pins("G19", dir="o")),
            Subsignal("RED1", Pins("H19", dir="o")),
            Subsignal("RED2", Pins("J19", dir="o")),
            Subsignal("RED3", Pins("N19", dir="o")),
            Subsignal("GRN0", Pins("J17", dir="o")),
            Subsignal("GRN1", Pins("H17", dir="o")),
            Subsignal("GRN2", Pins("G17", dir="o")),
            Subsignal("GRN3", Pins("D17", dir="o")),
            Subsignal("BLU0", Pins("N18", dir="o")),
            Subsignal("BLU1", Pins("L18", dir="o")),
            Subsignal("BLU2", Pins("K18", dir="o")),
            Subsignal("BLU3", Pins("J18", dir="o")),
            Subsignal("HSYNC", Pins("P19", dir="o")),
            Subsignal("VSYNC", Pins("R19", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # JA GPIO
        Resource("JA", 0,
            Subsignal("P1", Pins("J1")),
            Subsignal("P2", Pins("L2")),
            Subsignal("P3", Pins("J2")),
            Subsignal("P4", Pins("G2")),
            Subsignal("P7", Pins("H1")),
            Subsignal("P8", Pins("K2")),
            Subsignal("P9", Pins("H2")),
            Subsignal("P10", Pins("G3")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # JB GPIO
        Resource("JB", 0,
            Subsignal("P1", Pins("A14")),
            Subsignal("P2", Pins("A16")),
            Subsignal("P3", Pins("B15")),
            Subsignal("P4", Pins("B16")),
            Subsignal("P7", Pins("A15")),
            Subsignal("P8", Pins("A17")),
            Subsignal("P9", Pins("C15")),
            Subsignal("P10", Pins("C16")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # JC GPIO
        Resource("JC", 0,
            Subsignal("P1", Pins("K17")),
            Subsignal("P2", Pins("M18")),
            Subsignal("P3", Pins("N17")),
            Subsignal("P4", Pins("P18")),
            Subsignal("P7", Pins("L17")),
            Subsignal("P8", Pins("M19")),
            Subsignal("P9", Pins("P17")),
            Subsignal("P10", Pins("R18")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # JXADC GPIO
        Resource("JXADC", 0,
            Subsignal("P1", Pins("J3")),
            Subsignal("P2", Pins("L3")),
            Subsignal("P3", Pins("M2")),
            Subsignal("P4", Pins("N2")),
            Subsignal("P7", Pins("K3")),
            Subsignal("P8", Pins("M3")),
            Subsignal("P9", Pins("M1")),
            Subsignal("P10", Pins("N1")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # Onboard SPI flash
        *SPIFlashResources(0,
            cs="K19",
            clk="C11",
            mosi="D18",
            miso="D19",
            wp="G18",
            hold="F18",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
    ]

    def toolchain_program(self, products, name):
        djtgcfg = os.environ.get("DJTGCFG", "djtgcfg")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.run([djtgcfg, "prog", "-d", "Basys3", "-i", "0", "-f", bitstream_filename], check=True)
