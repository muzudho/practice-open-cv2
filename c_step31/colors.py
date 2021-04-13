"""色(RGB)
"""

from conf import DE_GAMMA_FROM_LINEAR
#from gamma_correction import de_gamma_from_linear


def filtering(color):
    """色にフィルターを掛けやすいようにラッピングしておいてください"""

    # if DE_GAMMA_FROM_LINEAR:
    #    color = de_gamma_from_linear(color)

    # ここではフィルターを掛けずに、cv2 に色を渡すときに掛けた方がいい？
    return color


# White
WHITE = filtering((0.95, 0.95, 0.95))  # 少し控えめ

# Pale
PALE_GRAY = filtering((0.85, 0.85, 0.85))
PALE_RED = filtering((1.0, 0.7, 0.7))
PALE_GREEN = filtering((0.7, 1.0, 0.7))
PALE_BLUE = filtering((0.7, 0.7, 1.0))

# Bright
if DE_GAMMA_FROM_LINEAR:
    # ガンマ補正を解除する前提なら、上の方を使える
    U = 1.4
    L = 0.3
    M = (U+L)/2
    BRIGHT_GRAY = filtering((M, M, M))
    BRIGHT_RED = filtering((U, L, L))
    BRIGHT_GREEN = filtering((L, U, L))
    BRIGHT_BLUE = filtering((L, L, U))
else:
    BRIGHT_GRAY = filtering((0.55, 0.55, 0.55))
    BRIGHT_RED = filtering((0.9, 0.2, 0.2))
    BRIGHT_GREEN = filtering((0.2, 0.9, 0.2))
    BRIGHT_BLUE = filtering((0.2, 0.2, 0.9))

# Light
LIGHT_GRAY = filtering((0.8, 0.8, 0.8))
LIGHT_RED = filtering((1.0, 0.6, 0.6))
LIGHT_GREEN = filtering((0.6, 1.0, 0.6))
LIGHT_BLUE = filtering((0.6, 0.6, 1.0))

# Soft
SOFT_GRAY = filtering((0.7, 0.7, 0.7))
SOFT_RED = filtering((0.9, 0.5, 0.5))
SOFT_GREEN = filtering((0.5, 0.9, 0.5))
SOFT_BLUE = filtering((0.5, 0.5, 0.9))

# Vivid
VIVID_RED = filtering((1.0, 0, 0))
VIVID_GREEN = filtering((0, 1.0, 0))
VIVID_BLUE = filtering((0, 0, 1.0))

# Strong
if DE_GAMMA_FROM_LINEAR:
    # ガンマ補正を解除する前提なら、上の方と下の方の全部を使える
    U = 0.85
    L = 0.15
    M = (U+L)/2
    GRAY = filtering((M, M, M))
    RED = filtering((U, L, L))
    YELLOW = filtering((U, U, L))
    GREEN = filtering((L, U, L))
    CYAN = filtering((L, U, U))
    BLUE = filtering((L, L, U))
    MAGENTA = filtering((U, L, U))
else:
    GRAY = filtering((0.45, 0.45, 0.45))
    RED = filtering((0.8, 0.1, 0.1))
    YELLOW = filtering((0.8, 0.8, 0.1))
    GREEN = filtering((0.1, 0.8, 0.1))
    CYAN = filtering((0.1, 0.8, 0.8))
    BLUE = filtering((0.1, 0.1, 0.8))
    MAGENTA = filtering((0.8, 0.1, 0.8))

# Dark
if DE_GAMMA_FROM_LINEAR:
    # ガンマ補正を解除する前提なら、下の方を使える
    U = 0.4
    L = 0.0
    M = (U+L)/2
    DARK_GRAY = filtering((M, M, M))
    DARK_RED = filtering((U, L, L))
    DARK_GREEN = filtering((L, U, L))
    DARK_BLUE = filtering((L, L, U))
else:
    DARK_GRAY = filtering((0.4, 0.4, 0.4))
    DARK_RED = filtering((0.6, 0.2, 0.2))
    DARK_GREEN = filtering((0.2, 0.6, 0.2))
    DARK_BLUE = filtering((0.2, 0.2, 0.6))

# Dark grayish
DARK_GRAYISH_GRAY = filtering((0.25, 0.25, 0.25))
DARK_GRAYISH_RED = filtering((0.4, 0.1, 0.1))
DARK_GRAYISH_GREEN = filtering((0.1, 0.4, 0.1))
DARK_GRAYISH_BLUE = filtering((0.1, 0.1, 0.4))

# BLACK
BLACK = filtering((0.05, 0.05, 0.05))  # 少し控えめ
