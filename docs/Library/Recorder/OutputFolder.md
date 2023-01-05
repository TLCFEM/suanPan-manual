# Output Folder

By default, all recorders record files and store the data under the **initial** current working directory. The initial
current working directory is the working directory where the main program is executed. Note that here **initial** is
emphasized given the fact that users can use `pwd` command to change the current working directory.

Internally, the output folder is managed by an independent path that is initialised to the current working directory
when starting the program.

What if we want to manage the output folder separately to better organise the recorded data? It is possible to do so by
using the `output_folder` attribute.

## Syntax

```text
# check current output folder
peek output_folder

# change output folder
set output_folder (1)
# (1) string, absolute/relative path to the output folder
```

A few points to note:

1. The program tries to create the given output folder it does not exist. The creation itself may fail. In case of any
   failure, the output folder is not changed.
2. The output folder can be either absolute or relative (to current output folder).
3. A special token `$pwd` is available to set the output folder to the current working directory, which may have been
   changed manually.

## Example

The following are some examples to demonstrate the usage of the `output_folder` attribute.

```bash
# on entering, pwd and output_folder are set to the current working directory
suanPan ~<> pwd
/home/theodore/Demo
suanPan ~<> peek output_folder
/home/theodore/Demo
suanPan ~<> pwd ..
# change pwd does not affect output_folder
suanPan ~<> pwd
/home/theodore
suanPan ~<> peek output_folder
/home/theodore/Demo
# change output_folder, result-u folder will be created
suanPan ~<> set output_folder result-u
/home/theodore/Demo/result-u
# change to another folder, result-f folder will be created
suanPan ~<> set output_folder ../result-f
/home/theodore/Demo/result-f
suanPan ~<> peek output_folder 
/home/theodore/Demo/result-f
# change to pwd, which has been changed previously
suanPan ~<> set output_folder $pwd
/home/theodore
# change pwd and then set output_folder to pwd
suanPan ~<> pwd Demo
suanPan ~<> set output_folder $pwd
/home/theodore/Demo
# the following two folders are created by setting output_folder
suanPan ~<> terminal ls
result-f  result-u
suanPan ~<> exit
```

## Control Output Folder For Recorders

The `output_folder` attribute is a global attribute that will be accessed by recorders when the `save` command is
invoked. This means it is possible to set different folders for different recorders prior to save the data. The
following is a simple example that shows how to store displacement and resistance data in different folders.

The example model is an elastic cantilever beam with a point load at the free end.

```text
node 1 0 0
node 2 1 0

material Elastic1D 1 10 1E-4
section Rectangle2D 1 12 1 1
element B21 1 1 2 1 6 1

fix 1 P 1
cload 1 0 10 2 2

plainrecorder 1 Node U 1 2
plainrecorder 2 Node RF 1 2

step static 1 1
set ini_step_size .1
set fixed_step_size true

analyze

# when saving, change the output folder to result-u for displacement recorder
set output_folder result-u
save recorder 1
# change the output folder to result-f for resistance recorder
set output_folder ../result-f
save recorder 2

exit
```

Now when it is executed, two folders are created under the current working directory. For brevity, the `np` flag is used
to suppress the output to screen.

```text
$ tree
.
└── B21.sp

0 directories, 1 file
$ suanpan -np -f ./B21.sp 
$ tree
.
├── B21.sp
├── result-f
│         ├── R2-RF1.txt
│         └── R2-RF2.txt
└── result-u
    ├── R1-U1.txt
    └── R1-U2.txt

2 directories, 5 files
```