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
if DE_GAMMA_FROM_LINEAR:
    # もしガンマ補正が世の中に存在しなかったら、バー全体に表現の幅があります
    U = 1.00
    L = 0.95  # 少し控えめ
    M = (U+L)/2
    WHITE = filtering((M, M, M))
else:
    # 世の中にはガンマ補正が存在するから、バーの上の方に表現の幅が偏ります
    M = 0.95  # 少し控えめ
    WHITE = filtering((M, M, M))


# Pale
if DE_GAMMA_FROM_LINEAR:
    U = 1.00
    L = 0.75
    M = (U+L)/2
    PALE_GRAY = filtering((M, M, M))
    PALE_RED = filtering((U, L, L))
    PALE_GREEN = filtering((L, U, L))
    PALE_BLUE = filtering((L, L, U))
else:
    U = 1.00
    L = 0.70
    M = (U+L)/2
    PALE_GRAY = filtering((M, M, M))
    PALE_RED = filtering((U, L, L))
    PALE_GREEN = filtering((L, U, L))
    PALE_BLUE = filtering((L, L, U))

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
if DE_GAMMA_FROM_LINEAR:
    U = 1.00
    L = 0.50
    M = (U+L)/2
    LIGHT_GRAY = filtering((M, M, M))
    LIGHT_RED = filtering((U, L, L))
    LIGHT_GREEN = filtering((L, U, L))
    LIGHT_BLUE = filtering((L, L, U))
else:
    U = 1.00
    L = 0.60
    M = (U+L)/2
    LIGHT_GRAY = filtering((M, M, M))
    LIGHT_RED = filtering((U, L, L))
    LIGHT_GREEN = filtering((L, U, L))
    LIGHT_BLUE = filtering((L, L, U))

# Soft
if DE_GAMMA_FROM_LINEAR:
    U = 0.872
    L = 0.372
    M = (U+L)/2
    SOFT_GRAY = filtering((M, M, M))
    SOFT_RED = filtering((U, L, L))
    SOFT_GREEN = filtering((L, U, L))
    SOFT_BLUE = filtering((L, L, U))
else:
    U = 0.90
    L = 0.50
    M = (U+L)/2
    SOFT_GRAY = filtering((M, M, M))
    SOFT_RED = filtering((U, L, L))
    SOFT_GREEN = filtering((L, U, L))
    SOFT_BLUE = filtering((L, L, U))

# Vivid
if DE_GAMMA_FROM_LINEAR:
    U = 1.000
    L = 0.000
    M = (U+L)/2
    VIVID_RED = filtering((U, L, L))
    VIVID_GREEN = filtering((L, U, L))
    VIVID_BLUE = filtering((L, L, U))
else:
    U = 1.000
    L = 0.000
    M = (U+L)/2
    VIVID_RED = filtering((U, L, L))
    VIVID_GREEN = filtering((L, U, L))
    VIVID_BLUE = filtering((L, L, U))

# Strong
if DE_GAMMA_FROM_LINEAR:
    U = 0.875
    L = 0.125
    M = (U+L)/2
    GRAY = filtering((M, M, M))
    RED = filtering((U, L, L))
    YELLOW = filtering((U, U, L))
    GREEN = filtering((L, U, L))
    CYAN = filtering((L, U, U))
    BLUE = filtering((L, L, U))
    MAGENTA = filtering((U, L, U))
else:
    U = 0.8
    L = 0.1
    M = (U+L)/2
    GRAY = filtering((M, M, M))
    RED = filtering((U, L, L))
    YELLOW = filtering((U, U, L))
    GREEN = filtering((L, U, L))
    CYAN = filtering((L, U, U))
    BLUE = filtering((L, L, U))
    MAGENTA = filtering((U, L, U))

# Dark
if DE_GAMMA_FROM_LINEAR:
    U = 0.500
    L = 0.000
    M = (U+L)/2
    DARK_GRAY = filtering((M, M, M))
    DARK_RED = filtering((U, L, L))
    DARK_GREEN = filtering((L, U, L))
    DARK_BLUE = filtering((L, L, U))
else:
    U = 0.600
    L = 0.200
    M = (U+L)/2
    DARK_GRAY = filtering((M, M, M))
    DARK_RED = filtering((U, L, L))
    DARK_GREEN = filtering((L, U, L))
    DARK_BLUE = filtering((L, L, U))

# Dark grayish
if DE_GAMMA_FROM_LINEAR:
    U = 0.250
    L = 0.000
    M = (U+L)/2
    DARK_GRAYISH_GRAY = filtering((M, M, M))
    DARK_GRAYISH_RED = filtering((U, L, L))
    DARK_GRAYISH_GREEN = filtering((L, U, L))
    DARK_GRAYISH_BLUE = filtering((L, L, U))
else:
    U = 0.400
    L = 0.100
    M = (U+L)/2
    DARK_GRAYISH_GRAY = filtering((M, M, M))
    DARK_GRAYISH_RED = filtering((U, L, L))
    DARK_GRAYISH_GREEN = filtering((L, U, L))
    DARK_GRAYISH_BLUE = filtering((L, L, U))

# BLACK
if DE_GAMMA_FROM_LINEAR:
    U = 0.050
    L = 0.000
    M = (U+L)/2
    BLACK = filtering((M, M, M))
else:
    M = 0.05  # 少し控えめ
    BLACK = filtering((M, M, M))
