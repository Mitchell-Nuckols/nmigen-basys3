from nmigen import *
from nmigen.build import Platform
from basys3 import Basys3Platform

class BlinkyWithDomain(Elaboratable):

    def __init__(self, width):
        self.width = width

    def elaborate(self, platform):
        clk = platform.request("CLK100")
        timer  = Signal(self.width)

        seg = platform.request("7SEG")

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk.i)
        m.d.sync += timer.eq(timer + 1)

        m.d.comb += seg.CA.o.eq(1)
        m.d.comb += seg.AN0.o.eq(1)

        for i in range(0,16):
            sw = platform.request("SW", i)
            with m.If(~sw.i):
                m.d.comb += platform.request("LD", i).o.eq(timer[(self.width-1) - i])

        return m

if __name__ == "__main__":
    platform = Basys3Platform()
    platform.build(BlinkyWithDomain(38), do_program=True)

