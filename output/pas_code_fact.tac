               VAR                                            j
               VAR                                            n
              GOTO                                      example
   fact:    FPARAM                                            n
               VAR                                            k
               VAR                                           t1
                LT              n              1           lab3
            ASSIGN              0                            t1
              GOTO                                         lab4
   lab3:    ASSIGN              1                            t1
   lab4:        EQ             t1              0           lab2
            ASSIGN              1                          fact
              GOTO                                         lab1
   lab2:       VAR                                           t2
               SUB              n              1             t2
            APARAM                                           t2
              CALL           fact                              
            ASSIGN           fact                             k
               VAR                                           t3
              MULT              n              k             t3
            ASSIGN             t3                          fact
   lab1:    RETURN                                             
example:    ASSIGN              5                             j
   lab5:        GT              j              0           lab7
              GOTO                                         lab6
   lab7:    APARAM                                            j
              CALL           fact                              
            ASSIGN           fact                             n
            APARAM                                            n
              CALL        writeln                              
               VAR                                           t4
               SUB              j              1             t4
            ASSIGN             t4                             j
              GOTO                                         lab5
   lab6:    RETURN                                             
