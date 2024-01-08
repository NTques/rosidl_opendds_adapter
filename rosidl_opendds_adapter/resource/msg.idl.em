// generated from rosidl_opendds_adapter/resource/msg.idl.em
// with input from @(pkg_name)/@(relative_input_file)
// generated code does not contain a copyright notice

@{
from rosidl_opendds_adapter.msg import get_include_file
include_files = set()
for field in msg.fields:
    include_file = get_include_file(field.type)
    if include_file is not None:
        include_files.add(include_file)
}@
@{
for include_file in include_files:
    inc_pkg = pkg_name+"/msg/dds_/"

    if inc_pkg in include_file:
        inc_name = include_file.replace(inc_pkg,"")
        print("#include " + "\"" + inc_name + "\"")
    else:
        print("#include " + "\"" + include_file + "\"")
}@

module @(pkg_name) {
  module msg {
    module dds_{
    
@{
TEMPLATE('struct.idl.em',msg=msg,)
}@

    };
  };
};
