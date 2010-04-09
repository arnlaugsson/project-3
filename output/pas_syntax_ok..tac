               VAR                                            x
               VAR                                            y
              GOTO                                         test
   test:    FPARAM                                            x
               VAR                                            t
               VAR                                            i
            ASSIGN              0                             i
               VAR                                           t1
              MULT             10              5             t1
               VAR                                           t2
            UMINUS             t1                            t2
   lab1:        LT              i              4           lab3
              GOTO                                         lab2
   lab3:       VAR                                           t3
               ADD              i              1             t3
            ASSIGN             t3                             i
              GOTO                                         lab1
   lab2:    ASSIGN              t                          test
            RETURN                                             
   test:       VAR                                           t4
              MULT             10             15             t4
            ASSIGN             t4                             y
               VAR                                           t5
                GT              x              2           lab6
            ASSIGN              0                            t5
              GOTO                                         lab7
   lab6:    ASSIGN              1                            t5
   lab7:        EQ             17              0           lab5
            ASSIGN      123.45e-3                             y
              GOTO                                         lab4
   lab5:    APARAM                                          3.3
              CALL           test                              
            ASSIGN           test                             y
               VAR                                           t6
               ADD              x              2             t6
            ASSIGN             t6                             x
   lab4:    RETURN                                             
