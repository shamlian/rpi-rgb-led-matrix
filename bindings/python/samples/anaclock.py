#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import math


class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        #canvas = self.matrix
        canvas = self.matrix.CreateFrameCanvas()
        w = canvas.width
        h = canvas.height
        r = w / 2 - 1

        cx = w/2
        cy = h/2

        #font = graphics.Font()
        #font.LoadFont("../../../fonts/7x13.bdf")

        c_border = graphics.Color(255, 255, 255)
        c_tick = graphics.Color(64, 32, 64)
        c_sec = graphics.Color(255, 0, 0)
        c_min = graphics.Color(0, 255, 0)
        c_hour = graphics.Color(0, 0, 255)

        ticklen = 0.8
        minlen = 0.9
        hourlen = 0.6

        sweep = True

        while True:
            now = time.localtime()

            canvas.Clear()

            for step in range(12):
                t = step / 12.0 * 2.0 * math.pi
                c = math.cos(t)
                s = math.sin(t)
                graphics.DrawLine(canvas, cx+c*r*ticklen+0.5, cy-s*r*ticklen+0.5, 
                                  cx+c*r+0.5, cy-s*r+0.5, c_tick)

            #clock border
            #graphics.DrawCircle(canvas, cx, cy, r, c_border)

            sec = now.tm_sec
            if sec > 59:
                sec = 59
            c = math.cos(sec / 60.0 * -2.0 * math.pi + math.pi / 2)
            s = math.sin(sec / 60.0 * -2.0 * math.pi + math.pi / 2)
            graphics.DrawLine(canvas, cx, cy, 
                              cx+c*r+0.5, cy-s*r+0.5, c_sec)

            min = now.tm_min
            if sweep:
                min += sec / 60.0
            c = math.cos(min / 60.0 * -2.0 * math.pi + math.pi / 2)
            s = math.sin(min / 60.0 * -2.0 * math.pi + math.pi / 2)
            graphics.DrawLine(canvas, cx, cy, 
                              cx+c*r*minlen+0.5, cy-s*r*minlen+0.5, c_min)

            hour = now.tm_hour if now.tm_hour < 12 else now.tm_hour - 12
            if sweep:
                hour += min / 60.0
            c = math.cos(hour / 12.0 * -2.0 * math.pi + math.pi / 2)
            s = math.sin(hour / 12.0 * -2.0 * math.pi + math.pi / 2)
            graphics.DrawLine(canvas, cx, cy, 
                              cx+c*r*hourlen+0.5, cy-s*r*hourlen+0.5, c_hour)

            canvas = self.matrix.SwapOnVSync(canvas)

            while (not sweep) and time.localtime() == now:
                time.sleep(1.0/30)

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
