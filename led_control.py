import time
import random

from rpi_ws281x import *


def get_strip() -> Adafruit_NeoPixel:
    """
    Gets LED strip.
    """
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    return strip


def generate_pretty_color():
    colors = [random.randint(128, 255), random.randint(0,50), random.randint(0, 25)]

    red_index = random.randint(0, 2)
    color_red = colors[red_index]
    del colors[red_index]

    green_index = random.randint(0, 1)
    color_green = colors[green_index]

    color_blue = colors[green_index - 1]
    return color_red, color_green, color_blue


# LED strip configuration:
LED_COUNT = 178      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 64     # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
RANDOM_COLOR_TTL = 100

strip = get_strip()
random_color_timer = 0

random_color_red, random_color_green, random_color_blue = generate_pretty_color()

random_dest_color_red, random_dest_color_green, random_dest_color_blue = generate_pretty_color()

def led_set_brightness(brightness: int):
    """
    Sets brightness for the strip.
    """
    global LED_BRIGHTNESS, strip
    LED_BRIGHTNESS = brightness
    strip = get_strip()


def wheel(pos):
    """
    Generate rainbow colors across 0-255 positions.
    """
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def led_rainbow(wait_ms=20):
    """
    Draw rainbow that uniformly distributes itself across all pixels.
    """
    while True:
        for j in range(256):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(wait_ms/1000.0)


def led_turn_off():
    """
    Turn off the LED strip.
    """
    black = Color(0, 0, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, black)
        strip.show()


def led_gradually_turn_on(timespan_sec1=300, timespan_sec2=300):
    """
    Gradually increase brightness.
    """
    wait_ms1 = ((timespan_sec1 / 255.0) / strip.numPixels())
    wait_ms2 = (timespan_sec2 / 255.0)

    color_red = 0
    color_green = 0
    color_blue = 0
    for i in range(255):
        for j in range(strip.numPixels()):
            color = Color(max(0, color_red + i + 1), max(0, color_green + i + 1), max(0, color_blue + i + 1))
            strip.setPixelColor(j, color)
            if wait_ms1 != 0:
                time.sleep(wait_ms1)
                strip.show()
        if wait_ms2 != 0:
            time.sleep(wait_ms2)
        strip.show()


def get_random_color(sudden_change: bool):
    global random_dest_color_red, random_dest_color_green, random_dest_color_blue, random_color_timer, random_color_red, random_color_green, random_color_blue

    if sudden_change:
        random_color_red, random_color_green, random_color_blue = generate_pretty_color()

    # slowly progress to destination color
    if random_color_timer < RANDOM_COLOR_TTL:
        random_color_red += (random_dest_color_red - random_color_red) / RANDOM_COLOR_TTL
        random_color_green += (random_dest_color_green - random_color_green) / RANDOM_COLOR_TTL
        random_color_blue += (random_dest_color_blue - random_color_blue) / RANDOM_COLOR_TTL
        random_color_timer += 1
    # or create new one
    else:
        random_dest_color_red, random_dest_color_green, random_dest_color_blue = generate_pretty_color()
        random_color_timer = 0
    # return current color
    return Color(int(random_color_red), int(random_color_green), int(random_color_blue))


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def led_real_time(num, values: [], sudden_change: bool):
    """
    Show colors in real time. (from client application)
    """
    color = get_random_color(sudden_change)

    for i in range(LED_COUNT):
        if i > num:
            strip.setPixelColor(i, Color(0, 0, 0))
            continue

        strip.setPixelColor(i, color)
    strip.show()
