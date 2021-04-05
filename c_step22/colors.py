"""色(RGB)
"""

from conf import BAR_TICKS

# White
WHITE = (0.95*BAR_TICKS, 0.95*BAR_TICKS, 0.95*BAR_TICKS)  # 少し控えめ

# Pale
PALE_GRAY = (0.85*BAR_TICKS, 0.85*BAR_TICKS, 0.85*BAR_TICKS)
PALE_RED = (BAR_TICKS-1, 0.7*BAR_TICKS, 0.7*BAR_TICKS)
PALE_GREEN = (0.7*BAR_TICKS, BAR_TICKS-1, 0.7*BAR_TICKS)
PALE_BLUE = (0.7*BAR_TICKS, 0.7*BAR_TICKS, BAR_TICKS-1)

# Bright
BRIGHT_GRAY = (0.55*BAR_TICKS, 0.55*BAR_TICKS, 0.55*BAR_TICKS)
BRIGHT_RED = (0.9*BAR_TICKS, 0.2*BAR_TICKS, 0.2*BAR_TICKS)
BRIGHT_GREEN = (0.2*BAR_TICKS, 0.9*BAR_TICKS, 0.2*BAR_TICKS)
BRIGHT_BLUE = (0.2*BAR_TICKS, 0.2*BAR_TICKS, 0.9*BAR_TICKS)

# Light
LIGHT_GRAY = (0.8*BAR_TICKS, 0.8*BAR_TICKS, 0.8*BAR_TICKS)
LIGHT_RED = (BAR_TICKS-1, 0.6*BAR_TICKS, 0.6*BAR_TICKS)
LIGHT_GREEN = (0.6*BAR_TICKS, BAR_TICKS-1, 0.6*BAR_TICKS)
LIGHT_BLUE = (0.6*BAR_TICKS, 0.6*BAR_TICKS, BAR_TICKS-1)

# Soft
SOFT_GRAY = (0.7*BAR_TICKS, 0.7*BAR_TICKS, 0.7*BAR_TICKS)
SOFT_RED = (int(0.9*BAR_TICKS), int(0.5*BAR_TICKS), int(0.5*BAR_TICKS))
SOFT_GREEN = (int(0.5*BAR_TICKS), int(0.9*BAR_TICKS), int(0.5*BAR_TICKS))
SOFT_BLUE = (int(0.5*BAR_TICKS), int(0.5*BAR_TICKS), int(0.9*BAR_TICKS))

# Vivid
VIVID_RED = ((BAR_TICKS-1), 0, 0)
VIVID_GREEN = (0, (BAR_TICKS-1), 0)
VIVID_BLUE = (0, 0, (BAR_TICKS-1))

# Strong
RED = (int(0.8*BAR_TICKS), int(0.1*BAR_TICKS), int(0.1*BAR_TICKS))
GREEN = (int(0.1*BAR_TICKS), int(0.8*BAR_TICKS), int(0.1*BAR_TICKS))
BLUE = (int(0.1*BAR_TICKS), int(0.1*BAR_TICKS), int(0.8*BAR_TICKS))

# Dark
DARK_GRAY = (int(0.4*BAR_TICKS), int(0.4*BAR_TICKS), int(0.4*BAR_TICKS))
DARK_RED = (int(0.6*BAR_TICKS), int(0.2*BAR_TICKS), int(0.2*BAR_TICKS))
DARK_GREEN = (int(0.2*BAR_TICKS), int(0.6*BAR_TICKS), int(0.2*BAR_TICKS))
DARK_BLUE = (int(0.2*BAR_TICKS), int(0.2*BAR_TICKS), int(0.6*BAR_TICKS))

# Dark grayish
DARK_GRAYISH_GRAY = (int(0.25*BAR_TICKS),
                     int(0.25*BAR_TICKS), int(0.25*BAR_TICKS))
DARK_GRAYISH_RED = (int(0.4*BAR_TICKS), int(0.1*BAR_TICKS), int(0.1*BAR_TICKS))
DARK_GRAYISH_GREEN = (int(0.1*BAR_TICKS),
                      int(0.4*BAR_TICKS), int(0.1*BAR_TICKS))
DARK_GRAYISH_BLUE = (int(0.1*BAR_TICKS),
                     int(0.1*BAR_TICKS), int(0.4*BAR_TICKS))

# BLACK
BLACK = (int(0.05*BAR_TICKS), int(0.05*BAR_TICKS),
         int(0.05*BAR_TICKS))  # 少し控えめ
