from model.registerModel import registerModel
import os

if __name__ == "__main__":
    current_dir =  os.path.dirname(__file__)
    config_file_path =current_dir +"/config/config.py"
    print("config_file_path======",config_file_path)
    regModel=registerModel(config_file_path) 
    regModel.registerProcess()
    current_status = regModel.read_register_status()
    print("current_status=====",current_status)

    