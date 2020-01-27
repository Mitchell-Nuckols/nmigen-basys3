from nmigen import *
from nmigen.build import Platform
from basys3 import Basys3Platform

class BlinkyWithDomain(Elaboratable):
    def elaborate(self, platform):
        clk = platform.request("CLK100")
        led    = platform.request("LD", 0)
        timer  = Signal(24)

        led1 = platform.request("LD", 1)
        sw1 = platform.request("SW", 1)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk.i)
        m.d.sync += timer.eq(timer + 1)
        m.d.comb += led.o.eq(timer[-1])

        m.d.comb += led1.o.eq(sw1.i)

        return m

if __name__ == "__main__":
    platform = Basys3Platform()
    platform.build(BlinkyWithDomain(), do_program=True)

