import residential_controller
import copy
import pytest
from unittest import mock

Column = residential_controller.Column
Elevator = residential_controller.Elevator
CallButton = residential_controller.CallButton
FloorRequestButton = residential_controller.FloorRequestButton
Door = residential_controller.Door

def scenario(column,requestedFloor, direction, destination):
    tempColumn = copy.deepcopy(column)
    selectedElevator = tempColumn.requestElevator(requestedFloor, direction)
    pickedUpUser = False
    if selectedElevator.currentFloor == requestedFloor:
        pickedUpUser = True 
    
    selectedElevator.requestFloor(destination)
    moveAllElevators(tempColumn)

    for i in range(len(tempColumn.elevatorList)):
        if tempColumn.elevatorList[i].ID == selectedElevator.ID:
            tempColumn.elevatorList[i].currentFloor = selectedElevator.currentFloor
        i+=1

    results = {
        "tempColumn": tempColumn,
        "selectedElevator": selectedElevator,
        "pickedUpUser": pickedUpUser
    }
    return results

column1 = Column(1, 10, 2)

#Makes the elevators who already have requests move before continuing with the scenario
def moveAllElevators(column):
    for elevator in column.elevatorList:
        while len(elevator.floorRequestList) != 0:
            elevator.move()

def test_Instantiates_a_Column_with_valid_attributes():
    
    assert type(column1) is Column
    assert column1.ID == 1
    assert column1.status is not None
    assert len(column1.elevatorList) is 2
    assert type(column1.elevatorList[0]) is Elevator
    assert len(column1.callButtonList ) is 18
    assert type(column1.callButtonList [0]) is CallButton

def test_Has_a_requestElevator_method():
    assert column1.requestElevator(1, "up") != None

def test_Can_find_and_return_an_elevator():
    elevator = column1.requestElevator(1, "up")
    assert type(elevator) is Elevator

elevator = Elevator(1, 10)
def test_Instantiates_a_Elevator_with_valid_attributes():
    
    assert type(elevator) is Elevator
    assert elevator.ID == 1
    assert elevator.status is not None
    assert elevator.currentFloor is not None
    assert type(elevator.door) is Door
    assert len(elevator.floorRequestButtonList) is 10

def test_Has_a_requestFloor_method():
    assert elevator.requestFloor(1) is not AttributeError

def test_Instantiates_a_CallButton_with_valid_attributes():
    callbutton = CallButton(1, 1,'up')
    assert type(callbutton) is CallButton
    assert callbutton.ID == 1
    assert callbutton.status is not None
    assert callbutton.floor is 1
    assert callbutton.direction is 'up'

def test_Instantiates_a_FloorRequestButton_with_valid_attributes():
    floorRequestButton = FloorRequestButton(1, 1)
    assert type(floorRequestButton) is FloorRequestButton
    assert floorRequestButton.ID == 1
    assert floorRequestButton.status is not None
    assert floorRequestButton.floor is 1

def test_Instantiates_a_Door_with_valid_attributes():
    door = Door(1)
    assert type(door) is Door
    assert door.ID == 1
    assert door.status is not None

#------------------------------------Scenario 1--------------------------------------------------------
column1.elevatorList[0].currentFloor = 2
column1.elevatorList[0].status = 'idle'
column1.elevatorList[1].currentFloor = 6
column1.elevatorList[1].status = 'idle'

results = scenario(column1, 3, 'up', 7)

def test_Part_1_of_scenario_1_chooses_the_best_elevator():
    assert results["selectedElevator"].ID is 1

def test_Part_1_of_scenario_1_picks_up_the_user():
    assert results["pickedUpUser"] is True

def test_Part_1_of_scenario_1_brings_the_user_to_destination():
    assert results["selectedElevator"].currentFloor is 7

def test_Part_1_of_scenario_1_ends_with_all_the_elevators_at_the_right_position():
    assert results["tempColumn"].elevatorList[0].currentFloor is 7
    assert results["tempColumn"].elevatorList[1].currentFloor is 6

#------------------------------------Scenario 2--------------------------------------------------------
column1.elevatorList[0].currentFloor = 10
column1.elevatorList[0].status = 'idle'
column1.elevatorList[1].currentFloor = 3
column1.elevatorList[1].status = 'idle'

results1 = scenario(column1, 1, 'up', 6)
        
column1 = copy.deepcopy(results1["tempColumn"]) # Update the column state with last scenario's result

results2 = scenario(column1, 3, 'up', 5)
column1 = copy.deepcopy(results2["tempColumn"]) # Update the column state with last scenario's result

results3 = scenario(column1, 9, 'down', 2)
column1 = copy.deepcopy(results3["tempColumn"]) # Update the column state with last scenario's result

def test_Part_1_of_scenario_2_chooses_the_best_elevator():
    assert results1["selectedElevator"].ID is 2

def test_Part_1_of_scenario_2_picks_up_the_user():
    assert results1["pickedUpUser"] is True

def test_Part_1_of_scenario_2_brings_the_user_to_destination():
    assert results1["selectedElevator"].currentFloor is 6

def test_Part_1_of_scenario_2_ends_with_all_the_elevators_at_the_right_position():
    assert results1["tempColumn"].elevatorList[0].currentFloor is 10
    assert results1["tempColumn"].elevatorList[1].currentFloor is 6

def test_Part_2_of_scenario_2_chooses_the_best_elevator():
    assert results2["selectedElevator"].ID is 2

def test_Part_2_of_scenario_2_picks_up_the_user():
    assert results2["pickedUpUser"] is True

def test_Part_2_of_scenario_2_brings_the_user_to_destination():
    assert results2["selectedElevator"].currentFloor is 5

def test_Part_2_of_scenario_2_ends_with_all_the_elevators_at_the_right_position():
    assert results2["tempColumn"].elevatorList[0].currentFloor is 10
    assert results2["tempColumn"].elevatorList[1].currentFloor is 5

def test_Part_3_of_scenario_2_chooses_the_best_elevator():
    assert results3["selectedElevator"].ID is 1

def test_Part_3_of_scenario_2_picks_up_the_user():
    assert results3["pickedUpUser"] is True

def test_Part_3_of_scenario_2_brings_the_user_to_destination():
    assert results3["selectedElevator"].currentFloor is 2

def test_Part_3_of_scenario_2_ends_with_all_the_elevators_at_the_right_position():
    assert results3["tempColumn"].elevatorList[0].currentFloor is 2
    assert results3["tempColumn"].elevatorList[1].currentFloor is 5

#------------------------------------Scenario 3--------------------------------------------------------
column1.elevatorList[0].currentFloor = 10
column1.elevatorList[0].status = 'idle'
column1.elevatorList[1].currentFloor = 3
column1.elevatorList[1].direction = 'up'
column1.elevatorList[1].status = 'moving'

results4 = scenario(column1, 3, 'down', 2)
results4["tempColumn"].elevatorList[1].currentFloor = 6
results4["tempColumn"].elevatorList[1].status = 'idle'

column1 = copy.deepcopy(results4["tempColumn"]) # update the column state with last scenario's result

results5 = scenario(column1, 10, 'down', 3)
column1 = copy.deepcopy(results5["tempColumn"]) # update the column state with last scenario's result

def test_Part_1_of_scenario_3_chooses_the_best_elevator():
    assert results4["selectedElevator"].ID is 1

def test_Part_1_of_scenario_3_picks_up_the_user():
    assert results4["pickedUpUser"] is True

def test_Part_1_of_scenario_3_brings_the_user_to_destination():
    assert results4["selectedElevator"].currentFloor is 2

def test_Part_1_of_scenario_3_ends_with_all_the_elevators_at_the_right_position():
    assert results4["tempColumn"].elevatorList[0].currentFloor is 2
    assert results4["tempColumn"].elevatorList[1].currentFloor is 6


def test_Part_2_of_scenario_3_chooses_the_best_elevator():
    assert results5["selectedElevator"].ID is 2

def test_Part_2_of_scenario_3_picks_up_the_user():
    assert results5["pickedUpUser"] is True

def test_Part_2_of_scenario_3_brings_the_user_to_destination():
    assert results5["selectedElevator"].currentFloor is 3

def test_Part_2_of_scenario_3_ends_with_all_the_elevators_at_the_right_position():
    assert results5["tempColumn"].elevatorList[0].currentFloor is 2
    assert results5["tempColumn"].elevatorList[1].currentFloor is 3