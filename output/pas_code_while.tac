               VAR                                            i
               VAR                                            j
              GOTO                                      example
example:    ASSIGN              0                             i
            ASSIGN              1                             j
   lab1:        LT              i             10           lab3
              GOTO                                         lab2
   lab3:       VAR                                           t1
               ADD              i              j             t1
            ASSIGN             t1                             j
               VAR                                           t2
               ADD              i              1             t2
            ASSIGN             t2                             i
              GOTO                                         lab1
   lab2:    APARAM                                            i
              CALL        writeln                              
            APARAM                                            j
              CALL        writeln                              
            RETURN                                             
