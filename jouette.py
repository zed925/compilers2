
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
==name
=PARAM"""


tiles = {"var_x": [var_x, var_x2], "var_xe" : var_xe, 'input': input_tile}


