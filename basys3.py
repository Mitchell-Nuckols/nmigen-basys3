import os
import subprocess

from nmigen.build import Platform, Resource, Pins, Clock, Attrs, Connector
from nmigen.build.run import LocalBuildProducts
from nmigen.cli import main_parser, main_runner
from nmigen.vendor.xilinx_7series import Xilinx7SeriesPlatform

__all__ = ["Basys3Platform"]

class Basys3Platform(Xilinx7SeriesPlatform):
    device = "xc7a35t"
    package = "cpg236"

    speed="1"

    default_clk = "CLK100"

    connectors=[]

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



    ]

    def toolchain_program(self, products, name):
        djtgcfg = os.environ.get("DJTGCFG", "djtgcfg")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.run([djtgcfg, "prog", "-d", "Basys3", "-i", "0", "-f", bitstream_filename], check=True)
