if_else="""SEQ
=SEQ
==SEQ
===SEQ
====SEQ
=====SEQ
======CJUMP
=======EXPRESSION
=======LT
=======CONST
========VAR
=======NAME
========TRUE
=======NAME
========FALSE
=====TRUE_EXPRESSION
====JUMP
=====done
===LABEL
====FALSE
==FALSE_EXPRESSION
=LABEL
==done"""

while_loop="""SEQ
=SEQ
==SEQ
===SEQ
====SEQ
=====LABEL
======TEST
=====CJUMP
======VAR
======LT
======CONST
=======VAR
======NAME
=======DONE
======NAME
=======BODY
====LABEL
=====BODY
===STUFF
==JUMP
===TEST
=LABEL
==DONE"""

var_x = """MEM
=+
==TEMP
===FP
==CONST
===VAR"""

var_x2 = """MEM
=+
==CONST
===VAR
==TEMP
===FP"""

var_xe = """MOVE
=VAR
=EXPRESSION"""

input_tile = """CALL
=NAME
==EXPRESSION"""

func_tile = """CALL
=NAME
==function
=PARAM"""

add_tile_1 ="""OP
=VAR
=CONST
==N"""

add_tile_2 ="""OP
=CONST
==N
=VAR
"""

add_tile_3 ="""OP
=VAR
=VAR
"""

const = """CONST
=N"""
tiles = {"var_x"   : [var_x, var_x2],
         "var_xe"  : var_xe,
         'input'   : input_tile,
         'func'    : func_tile,
         'ops'     : {add_tile_1, add_tile_2, add_tile_3},
         'const'   : const,
         'ifelse'  : if_else,
         'while'   : while_loop}


