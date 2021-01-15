def procedure(state_matrix,period):
    
    global vcc_one_high 
    global vcc_one_low 
    global vcc_two_high 
    global vcc_two_low   
    global phase_one
    global phase_two
    global position

    states = state_matrix
    while True:
        for state in states:
            motor_update(state)
            
            
            print('{} {} {} {} {} {}'.format(vcc_one_high.value,
                                      vcc_one_low.value,
                                       vcc_two_high.value,
                                       vcc_two_low.value,
                                       direction,
                                       position
                                        ))
            time.sleep(period)
            print('----')

