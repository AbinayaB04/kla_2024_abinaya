import json
#loading the json file in variable input_data
with open("Milestone1.json", 'r') as json_File:
    input_data= json.load(json_File)
#print(input_data)
steps=input_data["steps"]
machine=input_data["machines"]
wafer=input_data["wafers"]
#print(steps[0])
#print(steps[0]["id"])
#output 
schedule = []
#initialising the current time of the machine and the machines initial time 
current_time = {}
current=0
machine_sets= {machine['machine_id']: {'time': 0, 'parameters': machine['initial_parameters']} for machine in input_data['machines']}
current_time= {machine['machine_id']: 0 for machine in input_data['machines']}
#procedure to build the schedule
#traversing the thw wafers
for wafer in input_data['wafers']:
    #traversing the particular wafer type quantity(range)
    for z in range(wafer['quantity']):
        wafer_id = f"{wafer['type']}-{z+1}"
        #traversing through the steps
        for step in input_data['steps']:
            step_id = step['id']
            #setting up the machines list asthe steps maches the machine
            machine_list= [m for m in input_data['machines'] if m['step_id']==step_id]
            #traversing the machine list for paticular step id
            print(machine_list)
            print("--------")
            for machine in machine_list:
                machine_id=machine['machine_id']
                #from the list of machines select the machine with less time
                if machine_sets[machine_id]['time']<=current:
                    #print(current_time)
                    processing_time=wafer['processing_times'][step_id]
                    #print(wafer['processing_times'][step_id])
                    start_time=current
                    end_time=start_time +processing_time
                    #append in the schedule list as dictionary
                    schedule.append({
                            "wafer_id":wafer_id,
                            "step":step_id,
                            "machine":machine_id,
                            "start_time":start_time,
                            "end_time":end_time
                        })
                    
                        #once we update the schedule change the machine time
                    machine_sets[machine_id]['time']= end_time
                    current=end_time

                    #if length of the equal to n value make cooldown and initialize
                    if (len(schedule) ==machine['n']):
                        cooldown_time =machine['cooldown_time']
                        current=end_time +cooldown_time
                        machine_sets[machine_id]['parameters']=machine['initial_parameters']
                    break
output_schedule={"schedule":schedule}
op_file=json.dumps(output_schedule, indent=4)
with open("mile1.json", "w") as outfile:
    outfile.write(op_file)
print(op_file)

