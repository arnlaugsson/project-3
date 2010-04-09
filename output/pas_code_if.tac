               VAR                                            i
               VAR                                            j
              GOTO                                      example
example:    ASSIGN              1                             i
               VAR                                           t1
            UMINUS              1                            t1
            ASSIGN             t1                             j
               VAR                                           t2
                GT              i              0           lab3
            ASSIGN              0                            t2
              GOTO                                         lab4
   lab3:    ASSIGN              1                            t2
   lab4:        EQ             t2              0           lab2
               VAR                                           t3
              MULT              j              3             t3
               VAR                                           t4
               SUB              1             t3             t4
            ASSIGN             t4                             i
              GOTO                                         lab1
   lab2:       VAR                                           t5
               ADD              i              1             t5
            ASSIGN             t5                             i
   lab1:    APARAM                                            i
              CALL        writeln                              
            RETURN                                             
               VAR                                            i
               VAR                                            j
              GOTO                                      example
example:    ASSIGN              1                             i
               VAR                                           t1
            UMINUS              1                            t1
            ASSIGN             t1                             j
               VAR                                           t2
                GT              i              0           lab3
            ASSIGN              0                            t2
              GOTO                                         lab4
   lab3:    ASSIGN              1                            t2
   lab4:        EQ             t2              0           lab2
               VAR                                           t3
              MULT              j              3             t3
               VAR                                           t4
               SUB              1             t3             t4
            ASSIGN             t4                             i
              GOTO                                         lab1
   lab2:       VAR                                           t5
               ADD              i              1             t5
            ASSIGN             t5                             i
   lab1:    APARAM                                            i
              CALL        writeln                              
            RETURN                                             
