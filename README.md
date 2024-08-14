# JetsonNano
## 1. WSL Ubuntu 18.04.6 설치
Windows powershell에서 `wsl --list --online` 로 배포판 확인 후 `wsl --install -d Ubuntu-18.04`로 18.04 설치 Jetson nano의 경우 18.04에서 설치 가능

## 2. WSL USB연결
https://github.com/dorssel/usbipd-win/releases 에 들어가 usbipd-win_4.3.0.msi 설치
powershell 관리자 권한으로 실행
 
```
usbipd list # 연결된 usb port 확인
usbipd bind -b 1-6 # 필자의 경우 1-6으로 확인됨
usbipd attach --wsl --busid 1-6 --auto-attach
```

## 3. 기본 라이브러리 설치
```
sudo apt-get update
sudo apt-get install nautilus x11-apps firefox ubuntu-desktop -y
```

## 4. dpkg설치 오류
```
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
sudo apt install -y binfmt-support qemu-user-static

sudo update-binfmts \
 --package qemu-user \
 --install qemu-aarch64 /usr/bin/qemu-aarch64-static \
 --magic '\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\xb7\x00' \
 --mask '\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'

wget https://github.com/qemu/qemu/raw/master/scripts/qemu-binfmt-conf.sh
chmod +x qemu-binfmt-conf.sh
sudo ./qemu-binfmt-conf.sh --qemu-path /usr/bin --qemu-suffix -static --debian
sudo update-binfmts --import qemu-aarch64
```

## 5-1. L4T Driver Package(BSP), Sample Root Filesystem 설치(방법1)
```
wget [https://developer.nvidia.com/embedded/l4t/r32_release_v7.1/t210/jetson-210_linux_r32.7.1_aarch64.tbz2](https://developer.nvidia.com/embedded/l4t/r32_release_v7.1/t210/jetson-210_linux_r32.7.1_aarch64.tbz2)
wget [https://developer.nvidia.com/embedded/l4t/r32_release_v7.1/t210/tegra_linux_sample-root-filesystem_r32.7.1_aarch64.tbz2](https://developer.nvidia.com/embedded/l4t/r32_release_v7.1/t210/tegra_linux_sample-root-filesystem_r32.7.1_aarch64.tbz2)

sudo tar xfp jetson-210_ #tab 치세요
sudo tar xfp tegra_linux_sample-root-filesystem_r32.7.1_aarch64.tbz2 -C Linux_for_Tegra/rootfs
sudo ./Linux_for_Tegra/apply_binaries.sh

cd Linux_for_Tegra
sudo ./flash.sh jetson-nano-devkit-emmc mmcblk0p1
```

## 5-2. SDKManager 사용(방법2 2024.08.13 추가)
Jetson Nano EMMC의 경우 16GB 스토리지로 제한되어 SDcard USB 부팅을 사용하여 부팅하려고 함  
이 때 EMMC의 계정과 SDcard USB부팅 계정이 일치해야한다.   
EMMC의 flash는 SDKManager를 사용하고, SDcard flash는 balenaEtcher를 사용한다  

`sdkmanager --archived-versions`  
구 버전 사용을 위해 --archived-versions 옵션을 추가해 주고 반드시 '4.6.1' 버전을 설치한다.
flash 할 때 계정은 아래와 같이 지정해 준다    
```
id : jetson  
pw : yahboom  
```

## 6. 저장공간 사이즈 100% 만들기
flash 된 SDcard 용량을 확인해 보면 16GB로 제한적인건 확인할 수 있다.  
작성일 기준 WSL에서 방법은 찾지못하였고 퓨어 리눅스에서 사용 가능하다.  
이 때 원래의 사이즈로 돌릴 수 있다. (beaglebone-ai-64 doc 참고)  
```
lsblk # /dev/sdX 이때 X 는 실제 lsblk를 입력하여 결과 값으로 나온 sd카드 위치를 찾아야 한다 ex) 32GB, 64GB등 sd 카드 용량을 기준 확인

umount /dev/sdX1

sudo parted -s /dev/sdX resizepart 1 '100%'
sudo e2fsck -f /dev/sdX2
sudo resize2fs /dev/sdX2
```

## 7. 필수 라이브러리 설치
lightdm
```
sudo apt-get update
sudo apt-get install lightdm
```
python3.8 설치  
```
1.update & upgrade
sudo apt update
sudo apt upgrade

2. 필요한 패키지 설치
sudo apt install build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev libc6-dev

3. python3.8 소스코드 받기
wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tar.xz

4. 압축 풀기
tar -xf Python-3.8.12.tar.xz
cd Python-3.8.12

5. Build
./configure --enable-optimizations
make -j4

6. 파이썬 버전에 따른 설
sudo make altinstall
python3.8 --version
```
python3.8로 기본 파이썬으로 변경  
```
$ which python3.8
/usr/local/bin/python3.8
$ ls -al /usr/local/bin/python3.8
-rwxr-xr-x 1 root root 16467456 8月  13 10:46 /usr/local/bin/python3.8
$ sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
$ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
$ sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.8 3

$ sudo update-alternatives --config python # 확인
  Selection    Path                      Priority   Status
------------------------------------------------------------
* 0            /usr/local/bin/python3.8   3         auto mode
  1            /usr/bin/python2.7         1         manual mode
  2            /usr/bin/python3.6         2         manual mode
  3            /usr/local/bin/python3.8   3         manual mode

Press <enter> to keep the current choice[*], or type selection number: 0
```

jtop  
```
sudo apt-get update
sudo apt-get install python-pip
sudo -H pip install -U jetson-stats
sudo reboot

sudo systemctl restart jtop.service
sudo systemctl enable jtop.service
systemctl is-enabled jtop.service
systemctl status jtop.service

jtop
```

opencv
```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install dphys-swapfile

----------------------------------------------------------------------------
# 두 Swap파일의 값이 다음과 같도록 값을 추가하거나, 파일 내 주석을 해제합니다.
# CONF_SWAPSIZE=4096
# CONF_SWAPFACTOR=2
# CONF_MAXSWAP=4096
----------------------------------------------------------------------------

sudo vim /sbin/dphys-swapfile
sudo vim /etc/dphys-swapfile

git clone https://github.com/JetsonHacksNano/installSwapfile
cd installSwapfile
./installSwapfile.sh

sudo reboot

sudo apt-get install -y  \
    libtesseract4 \
    libatlas3-base \
    python3-pip \
    python3.8 \
    python3.8-dev

sudo apt-get clean
python3.8 -m pip install numpy==1.19.4

----------------------------------------------------------------------------
# cmake 부분 수정
cmake  -D  CMAKE_BUILD_TYPE=RELEASE  \
-D  CMAKE_INSTALL_PREFIX=/usr  \
-D  OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules  \
-D  EIGEN_INCLUDE_PATH=/usr/include/eigen3  \
-D  WITH_OPENCL=OFF  \
-D  CUDA_ARCH_BIN=${ARCH}  \
-D  CUDA_ARCH_PTX=${PTX}  \
-D  WITH_CUDA=ON  \
-D  WITH_CUDNN=ON  \
-D  WITH_CUBLAS=ON  \
-D  ENABLE_FAST_MATH=ON  \
-D  CUDA_FAST_MATH=ON  \
-D  OPENCV_DNN_CUDA=ON  \
-D  ENABLE_NEON=ON  \
-D  WITH_QT=OFF  \
-D  WITH_OPENMP=ON  \
-D  BUILD_TIFF=ON  \
-D  WITH_FFMPEG=ON  \
-D  WITH_GSTREAMER=ON  \
-D  WITH_TBB=ON  \
-D  BUILD_TBB=ON  \
-D  BUILD_TESTS=OFF  \
-D  WITH_EIGEN=ON  \
-D  WITH_V4L=ON  \
-D  WITH_LIBV4L=ON  \
-D  WITH_PROTOBUF=ON  \
-D  OPENCV_ENABLE_NONFREE=ON  \
-D  INSTALL_C_EXAMPLES=OFF  \
-D  INSTALL_PYTHON_EXAMPLES=OFF  \
-D  PYTHON3_EXECUTABLE=/usr/local/bin/python3.8  \
-D  PYTHON3_INCLUDE_DIR=/usr/local/include/python3.8  \
-D  PYTHON3_LIBRARY=/usr/lib/aarch64-linux-gnu/libpython3.8.so  \
-D  PYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/lib/python3.8/site-packages/numpy/core/include  \
-D  PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.8/site-packages  \
-D  OPENCV_GENERATE_PKGCONFIG=ON  \
-D  BUILD_EXAMPLES=OFF  \
-D  CMAKE_CXX_FLAGS="-march=native  -mtune=native"  \
-D  CMAKE_C_FLAGS="-march=native  -mtune=native"  ..

----------------------------------------------------------------------------
```

