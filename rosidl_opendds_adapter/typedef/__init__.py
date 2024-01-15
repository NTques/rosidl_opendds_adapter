import pkgutil
import json

from collections import OrderedDict
from rosidl_opendds_adapter.parser import parse_message_string
from rosidl_opendds_adapter.resource import expand_template



def get_idl_type_identifier(idl_type):
    return idl_type.replace('::', '__') \
        .replace('<', '__').replace('>', '') \
        .replace('[', '__').replace(']', '')

def make_typedef_idl_from_msg(package_dir, package_name, output_dir):
    typedefs = OrderedDict()
    
    json_file_path = output_dir / (package_name + "_typedef.json")
    try:
        with open(json_file_path.absolute(), 'r') as json_file:
            typedefs = json.load(json_file)
    
    except FileNotFoundError:
        return None
    except json.decoder.JSONDecodeError:
        return None
    
    define_type = ""
    include_files = ""
    for key, value in typedefs.items():
        define_type += f'      typedef {value} {key};\n'
        
        if "::msg::dds_::" in value:
            include_path = value.split("::")[-1]
            include_path = include_path.replace("_>", "") + ".idl"
            include_files += f'#include "{include_path}"\n'
    
    output_data = include_files + "\n" + \
    "module " + package_name + " {\n" + \
    "  module msg {\n" + \
    "    module dds_ {\n\n" + \
    define_type + "\n\n" + \
    "    };\n"+ \
    "  };\n"+ \
    "};\n"
    

    idl_file_path = output_dir / (package_name +  "_typedef.idl")
    with open(idl_file_path.absolute(), 'w', encoding="utf-8") as idl_file:
        idl_file.write(output_data)

def make_typedef_from_msg(package_dir, package_name, input_file, output_dir):
    from rosidl_opendds_adapter.msg import get_idl_type
    
    assert package_dir.is_absolute()
    assert not input_file.is_absolute()
    assert input_file.suffix == '.msg' or input_file.suffix == ".srv"
    
    abs_msg_input_file = package_dir / input_file
    abs_input_file = package_dir / input_file
    content = abs_input_file.read_text(encoding='utf-8')
    msg = parse_message_string(package_name, input_file.stem, content)
    
    typedefs = OrderedDict()
    
    json_file_path = output_dir / (package_name + "_typedef.json")
    try:
        with open(json_file_path.absolute(), 'r') as json_file:
            typedefs = json.load(json_file)
    
    except FileNotFoundError:
        print(f'Create new file: {json_file_path}')
    except json.decoder.JSONDecodeError:
        print(f'Create new file: {json_file_path}')
        
    for field in msg.fields:
        idl_type = get_idl_type(field.type)
        
        if field.type.is_fixed_size_array():
            idl_base_type = idl_type.split('[', 1)[0]
            idl_base_type_identifier = idl_base_type.replace('::', '__')

            # only necessary for complex types
            if idl_base_type_identifier != idl_base_type:
                if idl_base_type_identifier not in typedefs:
                    typedefs[idl_base_type_identifier] = idl_base_type
                else:
                    assert typedefs[idl_base_type_identifier] == idl_base_type

            idl_type_identifier = get_idl_type_identifier(idl_type) + '[' + str(field.type.array_size) + ']'
            
            if idl_type_identifier not in typedefs:
                typedefs[idl_type_identifier] = idl_base_type_identifier
            else:
                assert typedefs[idl_type_identifier] == idl_base_type_identifier
    
    if msg.fields:
        for i, field in enumerate(msg.fields):
            type_ = field.type
            identifier = get_idl_type(type_)
            
            if "sequence<" in identifier and not "msg::dds_" in identifier:
                typedefs[type_.type + "Seq"] = identifier

    with open(json_file_path.absolute(), 'w', encoding="utf-8") as json_file:
        json.dump(typedefs, json_file, ensure_ascii=False, indent="  ")



