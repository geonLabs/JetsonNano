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

## 7.
