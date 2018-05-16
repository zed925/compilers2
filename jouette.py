
var_x = """MEM
=+
==TEMP
===FP
==CONST
===VARIABLE"""

var_x2 = """MEM
=+
==CONST
===VARIABLE
==TEMP
===FP"""

var_xe = """MOVE
=VARIABLE
=EXPRESSION"""

input_tile = """CALL
=NAME
==EXPRESSION"""

func_tile = """CALL
=NAME
==function
=PARAM"""

add_tile_1 ="""OP
=VARIABLE
=CONST
==N"""

add_tile_2 ="""OP
=CONST
==N
=VARIABLE
"""

add_tile_3 ="""OP
=VARIABLE
=VARIABLE
"""

const = """CONST
=N"""
tiles = {"var_x": [var_x, var_x2],
         "var_xe" : var_xe,
         'input': input_tile,
         'func':func_tile,
         'ops': {add_tile_1, add_tile_2, add_tile_3},
         'const': const}


