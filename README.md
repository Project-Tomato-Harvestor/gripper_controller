# gripper_controller

This is a controller used to control dh gripper.

## Subscribtion:
- Topic: "gripper_cmd"
- Msg type: String
- Data:
    - "0": Fully open
    - "1": 50% open
    - "2": Fully close

## Publish:
- Topic: "/gripper/ctrl"
- Msg type: GripperCtrl