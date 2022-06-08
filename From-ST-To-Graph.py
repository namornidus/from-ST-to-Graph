################################################################################
#                                                                              #
#    Author: Roman Sudin                                                       #
#    Collaborator : Andrea Gemmani (Gimmmy)                                    #
#    E-mail : roman.sudin@studio.unibo.it                                      #
#    Version : 0.0.1                                                           #
#    Date : 08/06/2022                                                         #
#    Licence : MIT                                                             #
#                                                                              #
################################################################################

# Python program for finite state machine visualization with graphs

"""https://graphviz.org/Gallery/directed/fsm.html"""

try:
    import graphviz
    import re
except:
    print("\nYou dont have the needed libraries\n")
    
TextToConvert = """CASE Pallet_Handler_State OF
		Lifting:
			pallet_lift_target_position := 0; (*lifted position*)
			SystemClock := TRUE;
			IF (pallet_fork_enabled = FALSE) THEN;
				Pallet_Handler_State := Pallet_move_1;
			END_IF		
		Pallet_move_1:
			IF SystemTimer >= MaxCycles_Lifting THEN; // timer check routine
				SystemClock := FALSE;
				Pallet_Handler_State := Expired_request_error;
			END_IF
			
			IF (pallet_lifter_position = 0) THEN;
				SystemClock := FALSE;
				pallet_conv1_enable := TRUE;
				pallet_conv2_target_velocity := 0.5;
				SystemClock := TRUE;
				Pallet_Handler_State := Pallet_move_2;
			END_IF
		Pallet_move_2:
			IF SystemTimer >= MaxCycles_Moving THEN; // timer check routine
				SystemClock := 0;
				Pallet_Handler_State := Expired_request_error;
			END_IF
			
			IF (pallet_light_barrier_1 = TRUE AND pallet_light_barrier_2 = FALSE) THEN;
				SystemClock := FALSE;
				pallet_conv1_enable := FALSE;
				pallet_conv2_target_velocity := 0.1;
			END_IF
			IF (pallet_light_barrier_1 = TRUE AND pallet_light_barrier_2 = TRUE) THEN;
				pallet_conv2_target_velocity := 0;
				ReadyToCharge := TRUE;
				Pallet_Handler_State := Charging_phase;
				pallet_lift_target_position := -0.258; //release position
				SystemClock := TRUE;
			END_IF		
		Charging_phase:
			IF SystemTimer >= MaxCycles_Forking THEN; // timer check routine
				SystemClock := 0;
				Pallet_Handler_State := Expired_request_error;
			END_IF
			
			// wait for pallet lifter to be in position to unengage the fork
			IF (pallet_lifter_position = -0.258 AND pallet_fork_enabled = FALSE) THEN;
				pallet_fork_enable := TRUE; // unengage the fork
			END_IF
			// wait for fork to be unengaged
			IF (pallet_lifter_position = -0.258 AND pallet_fork_enabled = TRUE) THEN;
				pallet_lift_target_position := -0.12; // lift to position to reengage second pallet	
			END_IF
			// wait for right position to fork second pallet		
			IF (pallet_lifter_position = -0.12 AND pallet_fork_enabled = TRUE) THEN;
				pallet_fork_enable := FALSE; // fork second pallet
			END_IF
			// wait for fork engaged
			IF (pallet_lifter_position = -0.12 AND pallet_fork_enabled = FALSE) THEN;
				SystemClock := FALSE;
				pallet_lift_target_position := 0; (*lifted position*)
			    Pallet_Handler_State := Pallet_expulsion;
			END_IF
		Pallet_expulsion:
			// timer check routine
			IF SystemTimer >= MaxCycles_PalletCharging THEN;
				SystemClock := 0;
				Pallet_Handler_State := Expired_request_error;
			END_IF
			
			// wait for the pallet to be charged to move it away
			IF (PalletCharged = TRUE) THEN;
				ReadyToCharge := FALSE;
				pallet_conv2_target_velocity := 0.5;
				Pallet_Handler_State:=Lifting;
			END_IF
		Expired_request_error: 
			(* State is sent to this error whenever the rensponse of the machine took much longer than
			predicted time, in this case the whole machine needs to stop and an operator have to check 
			what went wrong in order to avoid damages *)
			ReadyToCharge := FALSE;
			pallet_conv1_enable := FALSE;
			pallet_conv2_target_velocity := 0;
			IF ResetReq THEN;
				SystemClock := TRUE;
				Pallet_Handler_State:=Reset;
			END_IF
		Reset:
			IF SystemClock >= MaxCycles_Reset THEN;
				Pallet_Handler_State    :=     Expired_request_error;
			END_IF
		END_CASE"""

Stringa = TextToConvert

# ATTENZIONE ALLA FORMATTAZIONE DEL CASE
risultati = re.findall(r'\n[ \t]*(.*):\n', Stringa)#.group(1)
print("risultati={}".format(risultati))

posizioni = []# lista che conterra le posizioni degli stati all'interno della Stringa
for ii in range(len(risultati)):
    #posizioni.append(re.findall(r'{0}:\n'.format(risultati[ii]), Stringa))
    posizioni.append(Stringa.find('{0}:\n'.format(risultati[ii])))

print("Posizioni = {0}".format(posizioni))
print(Stringa[posizioni[1]:posizioni[1]+1])

print(type(posizioni))
posizioni.append(0)
print(posizioni)
#print(dir(posizioni))
posizioni.sort()
print(posizioni)
print("Lenths of the whole code = {0}".format(len(Stringa)))
posizioni.append(len(Stringa))
print(posizioni)

AdjointMatrix=[]
for ii in range(len(risultati)+1):
    #print("ii = {0}".format(ii))
    a = posizioni[ii]
    b = posizioni[ii+1]
    #print("a = {0}".format(a))
    #print("b = {0}".format(b))
    #print(type(b))
    SSSstringaAAA = TextToConvert[a: b]
    #print("\n{0}\n".format(SSSstringaAAA))
    
    RisultatiLocali = re.findall(r'\n[ \t]*Pallet_Handler_State\s*:=\s*(.*)\s*;\n', SSSstringaAAA)
    AdjointMatrix.append(RisultatiLocali)
    
#AdjointMatrix.remove([])
    #for jj in range(len(risultati)):
    #    if risultati[ii] in SSSstringaAAA:
    #        #AdjointMatrix[ii].append(risultati[ii])
    #        pass

# visualization part of the code
f = graphviz.Digraph('finite_state_machine', filename='fsm.gv')
f.attr(rankdir='TD', size='8,5')# where 'LR' -> graph from left to right, 'RL' -> graph from right to left, 'TD' -> graph from top to down

f.attr('node', shape='box', splines="line", K="0.99")
for ii in range(len(risultati)):
    f.node(risultati[ii])

for ii in range(len(AdjointMatrix)):
    #print(len(AdjointMatrix[ii]))
    for jj in range(len(AdjointMatrix[ii])):
        #print("ii = {0}, jj = {1}".format(ii, jj))
        #print("risultati[{0}] = {1}".format(ii, risultati[ii]))
        
        f.edge(risultati[ii], AdjointMatrix[ii][jj], label='')
        
f.view()













