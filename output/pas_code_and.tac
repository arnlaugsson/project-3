               VAR                                            i
               VAR                                            j
              GOTO                                      example
example:    ASSIGN              0                             i
            ASSIGN              6                             j
               VAR                                           t1
                LT              i              1           lab3
                GT              j              5           lab4
               VAR                                           t2
               AND           lab3           lab4             t2
            ASSIGN              0                            t1
              GOTO                                         lab5
     10:    ASSIGN              1                            t1
   lab5:        EQ              8              0           lab2
               VAR                                           t3
               ADD              j              1             t3
            ASSIGN             t3                             j
              GOTO                                         lab1
   lab2:       VAR                                           t4
               SUB              i              1             t4
            ASSIGN             t4                             i
   lab1:    APARAM                                            i
              CALL        writeln                              
            APARAM                                            j
              CALL        writeln                              
            RETURN                                             
