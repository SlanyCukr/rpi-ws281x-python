import time
from rpi_ws281x import *


def get_strip() -> Adafruit_NeoPixel:
    """
    Gets LED strip.
    """
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    return strip

# LED strip configuration:
LED_COUNT      = 180      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
strip = get_strip()


def led_turn_off(wait_ms=50):
    """
    Turn off the LED strip.
    """
    black = Color(0, 0, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, black)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def led_gradually_turn_on(wait_ms=50):
    """
    Gradually increase brightness.
    """
    color_red = 255
    color_green = 255
    color_blue = 255
    for i in range(255):
        for j in range(strip.numPixels()):
            color = Color(max(0, color_red + i + 1), max(0, color_green + i + 1), max(0, color_blue + i + 1))
            strip.setPixelColor(j, color)
            #strip.show()
        strip.show()
        time.sleep(wait_ms / 1000.0)
