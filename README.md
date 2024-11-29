# Jetson Nano emmc module for ubuntu20.04 env
## Hardware and Software Spec
### Hardware
  1. Board : Jetson Nano Development 4GB
  2. HostPC : Ubuntu 20.04
  3. Camera : Luxonis OAK-D-W
  4. ssd : 256GB nvme M.2

### Software
  1. OS : Ubuntu 20.04
  2. Middle OS : ROS noetic
  3. Python Version : 3.8.10
  4. Jetpack 4.6.6
  5. L4T : 32.7.6
  6. CUDA : 10.2.300
  7. cuDNN : 8.2.1.32
  8. TensorRT : 8.2.1.9
  9. Python Binding TensorRT : 8.0

## Install
### flashing Jetson nano emmc module

1. Host PC : Ubuntu20.04

2. Download Jetson Linux Archive
  1) Invite https://developer.nvidia.com/embedded/linux-tegra-r3276  
  2) Download Driver Package(BSP) for Jetson Nano  
   ->https://developer.nvidia.com/downloads/embedded/l4t/r32_release_v7.6/t210/jetson-210_linux_r32.7.6_aarch64.tbz2  
  3) Download Sample Root Filesystem  
   -> https://developer.nvidia.com/downloads/embedded/l4t/r32_release_v7.6/t210/tegra_linux_sample-root-filesystem_r32.7.6_aarch64.tbz2  

3. Flash Jetson module  
  1) cd /Download  
  2) mkdir Jetson_project  
  3) mv Jetson-210_Linux_R32.7.6_aarch64.tbz2 ./Jetson_project  
  4) mv Tegra_Linux_Sample-Root-Filesystem_R32.7.6_aarch64.tbz2 ./Jetson_project  
  5) tar xf Jetson-210_Linux_R32.7.6_aarch64.tbz2  
  6) cd Linux_for_Tegra/rootfs/  
  7) sudo tar xpf ../../Tegra_Linux_Sample-Root-Filesystem_R32.7.6_aarch64.tbz2  
  8) cd ..  
  9) sudo ./apply_binaries.sh  
  10) sudo ./flash.sh jetson-nano-emmc mmcblk0p1  

### Jetson Nano boot for Nvme (https://wiki.seeedstudio.com/reComputer_Jetson_Memory_Expansion/)
  0) connect nvme ssd on board && boot
  1) Ctrl + F && disks
  2) Format Disk
  3) Partitioning : Compatible with...hard disks > 2TB(GPT) && Click Format..
  4) click on the mdiddle + to add a disk character
  5) click on Next
  6) Volume Name : SSD && Type Internal disk for use with Linux systems only (Ext4) && Create
  7) git clone https://github.com/limengdu/rootOnNVMe.git
  8) cd rootOnNVMe/
  9) ./copy-rootfs-ssd.sh
  10) ./setup-service.sh
  11) sudo reboot now 

### Jetpack build
  0) host pc install Docker image  
  1) https://developer.nvidia.com/sdk-manager, Docker Image Ubuntu 18.04 Download    
  2) cd Download  
  3) docker load < <(tar -c .)  
  4) jetpack_docker install (command more -> https://docs.nvidia.com/sdk-manager/docker-containers/index.html)  
   -> docker run -it --rm --privileged -v /dev/bus/usb:/dev/bus/usb/ -v /dev:/dev -v /media/$USR:/media/nvidia:slave --network host sdkmanager:2.2.0.12021-Ubuntu_18.04 --cli  
  5) Login NVIDIA Developer
  6) Install
  7) Jetson
  8) Uncheck Host Machine(press spacebar), Target Hardware
  9) Jetson Nano modules
  10) Do you want to show all release versions? | y
  11) JetPack 4.6.6 | select
  12) DeepStream 6.0.1 Uncheck
  13) Do you want to customize the install settings | y
  14) Do you want to flash Jetson Module? | n
  15) Download folder : (/home/nvidia/Downloads/nvidia/sdkm_downloads)
  16) Target HW image folder: (/home/nvidia/nvidia/nvidia_sdk)
  17) Accept the terms and conditions of all license agreements: | move 2 & enter
  18) Install JetPack 4.6.6 now | enter
  19) Allow usage data collection? | No
  20) space bar && unchech Jetson OS && enter
  21) Install
  22) Connect via | Ethernet cable (turn on Jetson Nano and connect same network on hostpc)
  23) Enter SSH connection detail to Jetson Nano Modules: | IPv4
  24) IP address: | Jetson Nano IP ex) 111.111.111.51
  25) Username: | Jetson Nano Name ex) jmnano
  26) Password: | Jetson Nano Password ex) 1234
  27) Proxy mode: | Do not set proxy
  28) enter

### Update Ubuntu20.04 (https://qengineering.eu/install-ubuntu-20.04-on-jetson-nano.html)
  1) sudo vim /etc/update-manager/release-upgrades
   -> change line Prompt=nomal
  2) sudo apt-get update
  3) sudo apt-get dist-upgrade
  4) sudo reboot
  5) sudo do-release-upgrade
  6) almost questions enter y, not to use chrominum but auto install
  7) sudo vim /etc/gdm3/custom.conf
   -> change uncomment | `WaylandEnable=false`
  8) sudo vim /etc/X11/xorg.conf
   -> chagne uncommnet | Driver "nvidia"
  9) sudo vim /erc/update-manager/release-upgrades
   -> change Prompt=never

### Ubuntu 20.04 start_settings
  1) sudo rm -rf /usr/share/vulkan/icd.d
  2) sudo apt-get update | maybe this time show error for chrominium use chatgpt how to delete chrominium (https://chatgpt.com/share/67496421-4744-800b-807b-7ab39b2b5af1)
  3) sudo apt-get upgrade
  4) sudo apt-get autoremove
  5) sudo rm /usr/share/applications/vpi1_demos\
  6) cd /usr/share/nvpmodel_indicator
  7) sudo mv nv_logo.svg no_logo.svg

### Install gcc & clang
  1) sudo apt-get install gcc-8 g++-8
  2) sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 9
  3) sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 8
  4) sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 9
  5) sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 8
  6) sudo update-alternatives --config gcc
  7) sudo update-alternatives --config g++
  8) sudo apt-get install clang-8

### Setting gnome Interface
#### Uninstall lightdm
  1) sudo apt-get purge lightdm
  2) sudo apt-get autoremove
#### Install gnome-desktop
  1) sudo dpkg-reconfigure gdm3
  2) sudo apt install ubuntu-gnome-desktop
  3) sudo apt install gnome-tweaks
  4) Alt + F2, r
  5) sudo apt install --reinstall gnome-control-center
  
### Jetson nano add swap memory
  1) git clone https://github.com/JetsonHacksNano/installSwapfile
  2) cd installSwapfile
  3) if you want to 8GB more Change number
   -> vim ./installSwapfile.sh
   -> SWAPSIZE = 8 (defalut 6)
  4) ./installSwapfile.sh

### Install Opencv with CUDA
  0) uninstall opencv * use Chatgpt
  1) wget https://github.com/Qengineering/Install-OpenCV-Jetson-Nano/raw/main/OpenCV-4-8-0.sh
  2) sudo chmod 755 ./OpenCV-4-8-0.sh
  3) vim ./OpenCV-4-8-0.sh
   -> delete v4l2ucp | use vim search : esc, /v4l2ucp and delete
   -> change Cmake command (Using gcc 8 version)
```
   # Set GCC-8 as default compiler for this build
CC=/usr/bin/gcc-8 CXX=/usr/bin/g++-8 cmake -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr \
  -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
  -D EIGEN_INCLUDE_PATH=/usr/include/eigen3 \
  -D WITH_OPENCL=OFF \
  -D CUDA_ARCH_BIN=${ARCH} \
  -D CUDA_ARCH_PTX=${PTX} \
  -D WITH_CUDA=ON \
  -D WITH_CUDNN=ON \
  -D WITH_CUBLAS=ON \
  -D ENABLE_FAST_MATH=ON \
  -D CUDA_FAST_MATH=ON \
  -D OPENCV_DNN_CUDA=ON \
  -D ENABLE_NEON=ON \
  -D WITH_QT=OFF \
  -D WITH_OPENMP=ON \
  -D BUILD_TIFF=ON \
  -D WITH_FFMPEG=ON \
  -D WITH_GSTREAMER=ON \
  -D WITH_TBB=ON \
  -D BUILD_TBB=ON \
  -D BUILD_TESTS=OFF \
  -D WITH_EIGEN=ON \
  -D WITH_V4L=ON \
  -D WITH_LIBV4L=ON \
  -D WITH_PROTOBUF=ON \
  -D OPENCV_ENABLE_NONFREE=ON \
  -D INSTALL_C_EXAMPLES=OFF \
  -D INSTALL_PYTHON_EXAMPLES=OFF \
  -D PYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages \
  -D OPENCV_GENERATE_PKGCONFIG=ON \
  -D BUILD_EXAMPLES=OFF \
  -D CMAKE_CXX_FLAGS="-march=native -mtune=native" \
  -D CMAKE_C_FLAGS="-march=native -mtune=native" ..
```
  4) ./OpenCV-4-8-0.sh

### TensorRT Python Bindings (https://elinux.org/Jetson/L4T/TRT_Customized_Example#TensorRT_Python_Bindings)
  1) sudo apt install zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev -y
  2) wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tar.xz
  3) tar xvf Python-3.8.10.tar.xz Python-3.8.10/
  4) mkdir build-python-3.8.10
  5) cd build-python-3.8.10/
  6) ../Python-3.8.10/configure --enable-optimizations
  7) make -j $(nproc)
  8) sudo -H make altinstall
  9) cd ../
  10) sudo apt-get install -y protobuf-compiler libprotobuf-dev openssl libssl-dev libcurl4-openssl-dev
  11) mkdir python3.8
  12) mkdir python3.8/include
  13) wget http://launchpadlibrarian.net/449197644/libpython3.8-dev_3.8.0-3~18.04_arm64.deb -O libpython3.8-dev_3.8.0-3~18.04_arm64.deb
  14) ar x libpython3.8-dev_3.8.0-3~18.04_arm64.deb
  15) tar -xvf data.tar.xz
  16) cp ./usr/include/aarch64-linux-gnu/python3.8/pyconfig.h python3.8/include/
  17) cp -r Python-3.8.10/Include/* python3.8/include/
  18) git clone https://github.com/pybind/pybind11.git
  19) git clone -b release/8.0 https://github.com/NVIDIA/TensorRT.git
  20) cd TensorRT
  21) git submodule update --init --recursive
  22) cd python/
  23) TRT_OSSPATH=${PWD}/.. EXT_PATH=${PWD}/../.. TARGET=aarch64 PYTHON_MINOR_VERSION=8 ./build.sh
  24) python3.8 -m pip install build/dist/tensorrt-8.0.1.6-cp38-none-linux_aarch64.whl | if you want to install venv, active venv and command this

### Install Torch & TorchVision (https://qengineering.eu/install-pytorch-on-jetson-nano.html)
#### torch
  1) sudo apt-get install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev
  2) if you want to install torch for venv active and follow
--------host python command--------                                         		--------venv python command--------  
  3) sudo -H pip3 install future							| pip3 install future
  4) sudo pip3 install -U --user wheel mock pillow					| pip3 install -U wheel mock pillow
  5) sudo -H pip3 install testresources							| pip3 install testresources
  6) sudo -H pip3 install setuptools==58.3.0						| pip3 install setuptools==58.3.0
  7) sudo -H pip3 install Cython							| pip3 install Cython
  8) sudo -H pip3 install gdown								| pip3 install gdown
  9) gdown https://drive.google.com/uc?id=1e9FDGt2zGS5C5Pms7wzHYRb0HuupngK1
  10) sudo -H pip3 install torch-1.13.0a0+git7c98e70-cp38-cp38-linux_aarch64.whl	| pip3 install torch-1.13.0a0+git7c98e70-cp38-cp38-linux_aarch64.whl
  11) rm torch-1.13.0a0+git7c98e70-cp38-cp38-linux_aarch64.whl

#### torchvision
  1) sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev
  2) sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev
  3) if you want to install torch for venv active and follow
--------host python command--------                                             	--------venv python command--------
  4) sudo pip3 install -U pillow							| pip3 install -U pillow
  5) gdown https://drive.google.com/uc?id=19UbYsKHhKnyeJ12VPUwcSvoxJaX7jQZ2
  6) sudo -H pip3 install torchvision-0.14.0a0+5ce4506-cp38-cp38-linux_aarch64.whl	| pip3 install torchvision-0.14.0a0+5ce4506-cp38-cp38-linux_aarch64.whl
  7) rm torchvision-0.14.0a0+5ce4506-cp38-cp38-linux_aarch64.whl

#### torch Install test
  0) python3 
  1) import torch
  2) torch.cuda.is_available()
   -> True

### Install YOLOv8 or YOLOv11
  1) pip install ultralytics

### Install ROS noetic(https://wiki.ros.org/noetic/Installation/Ubuntu)
  1) sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
  2) sudo apt install curl -y
  3) curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
  4) sudo apt update
  5) sudo apt install ros-noetic-desktop-full
  6) source /opt/ros/noetic/setup.bash
  7) echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
  8) source ~/.bashrc
  9) sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential -y 
  10) sudo apt install python3-rosdep -y
  11) sudo rosdep init
  12) rosdep update

### Install Luxonis Camera for ROS
  1) sudo wget -qO- https://raw.githubusercontent.com/luxonis/depthai-ros/main/install_dependencies.sh | sudo bash 
  2) sudo apt install python3-rosdep
  3) sudo rosdep init
  4) rosdep update
  5) mkdir -p dai_ws/src
  6) cd dai_ws/src
  7) git clone --branch noetic https://github.com/luxonis/depthai-ros.git
  8) cd ..
  9) rosdep install --from-paths src --ignore-src -r -y
  10) source /opt/ros/noetic/setup.bash
  11) catkin_make
  12) source devel/setup.bash

### Install Luxonis Camera for Python
  1) git clone https://github.com/luxonis/depthai-python.git
  2) cd depthai-python/examples
  3) python3 install_requirements.py










