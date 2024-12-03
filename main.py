import json 
import sys

def scale_rig(rig_file, output_scale):
    # Open and read the JSON file
    with open(rig_file, 'r') as file:
        data = json.load(file)

    bone_transforms = data['Data']['RootChunk']['boneTransforms']
    
    for bone in bone_transforms:
        # Scale the Scale values
        bone['Scale']['X'] *= output_scale
        bone['Scale']['Y'] *= output_scale
        bone['Scale']['Z'] *= output_scale
        
        # Scale the Translation values
        bone['Translation']['X'] *= output_scale
        bone['Translation']['Y'] *= output_scale
        bone['Translation']['Z'] *= output_scale

    with open('scaled_' + rig_file, 'w') as file:
        json.dump(data, file, indent=2)
    print(f"Scaled {rig_file} with {output_scale} and saved as scaled_{rig_file}")

def scale_ent(ent_file, output_scale):
    with open(ent_file, 'r') as file:
        data = json.load(file)
    components = data['Data']['RootChunk']['components']

    for component in components:
        if component['$type'] == 'entMeshComponent' or component['$type'] == 'entPhysicalMeshComponent':
            component['visualScale']['X'] *= output_scale
            component['visualScale']['Y'] *= output_scale
            component['visualScale']['Z'] *= output_scale

    with open('scaled_' + ent_file, 'w') as file:
        json.dump(data, file, indent=2)
    print(f"Scaled {ent_file} with {output_scale} and saved as scaled_{ent_file}")

def validate_file_extension(filename, expected_ext):
    if not filename.endswith(expected_ext):
        raise ValueError(f"Invalid file extension. Expected file ending in '{expected_ext}', got '{filename}'")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Single operation:")
        print("    python main.py [rig|ent] <filename> <scale>")
        print("    Example: python main.py rig mch_005__militech_cerberus.rig.json 0.33")
        print("\n  Both operations:")
        print("    python main.py both <rig_file> <ent_file> <scale>")
        print("    Example: python main.py both mch_005__militech_cerberus.rig.json q305_cerberus.ent.json 0.33")
        sys.exit(1)
    
    command = sys.argv[1].lower()

    try:
        if command == "both":
            if len(sys.argv) != 5:
                print("For 'both' command, please provide: rig_file ent_file scale")
                sys.exit(1)
            rig_file = sys.argv[2]
            ent_file = sys.argv[3]
            validate_file_extension(rig_file, '.rig.json')
            validate_file_extension(ent_file, '.ent.json')
            scale = float(sys.argv[4])
            scale_rig(rig_file, scale)
            scale_ent(ent_file, scale)
        else:
            if len(sys.argv) != 4:
                print("For single operations, please provide: command filename scale")
                sys.exit(1)
            filename = sys.argv[2]
            scale = float(sys.argv[3])
            
            if command == "rig":
                validate_file_extension(filename, '.rig.json')
                scale_rig(filename, scale)
            elif command == "ent":
                validate_file_extension(filename, '.ent.json')
                scale_ent(filename, scale)
            else:
                print("Invalid command. Use 'rig', 'ent', or 'both'")
                sys.exit(1)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

