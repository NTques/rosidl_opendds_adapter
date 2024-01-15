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

if msg.fields:
    for i, field in enumerate(msg.fields):
        if field.type.is_fixed_size_array():
            include_files.add(pkg_name + "_typedef.idl")
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
#include "@(pkg_name)_typedef.idl"

module @(pkg_name) {
  module msg {
    module dds_{
    
@{
TEMPLATE('struct.idl.em',msg=msg,)
}@

      typedef sequence<@(pkg_name)::msg::dds_::@(msg.msg_name)_> @(msg.msg_name)_Seq;
    };
  };
};
