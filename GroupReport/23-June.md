# 2023年6月自动化测试小队报告
## mugen测试策略

- 编写了[mugen测试策略](https://github.com/Pagerd/PLCT/blob/main/Report/June/mugen.md)

## mugen base test测试

- 对上个月剩余不通过的部分测试套进行失败分析并汇总到测试结果,以下为部分测试分析文档
  - [cli0-riscv-failed](https://github.com/weilinfox/PLCT-Working/blob/master/Done/Week2/riscv-failed.md) [cli0-x86failed.md](https://github.com/weilinfox/PLCT-Working/blob/master/Done/Week3/rv86_failed.md)
  - [cli1-riscv-failed](https://github.com/l0tk3/PLCT/tree/main/WrokReport/week3/fail.md) [cli1-x86-failed.md](https://github.com/l0tk3/PLCT/tree/main/WrokReport/week4/x86fail.md)
  - [cli2-riscvX86-failed](https://github.com/Pagerd/PLCT/blob/main/MayTestReport/README.md)
- 筛选出对选取测试mugen版本对比之前测试的mugen版本更新的测试例，以及上次测试时找不到log的测试例，并将其按进行分配，测试
  - 其中涉及123个测试套，总共1107个测试例 ，分配结果上传至[仓库](https://github.com/KotorinMinami/res_list/tree/master/NeedTest)
  - 已对包含的123个测试套进行测试，少数测试结果已合并[commit](https://github.com/KotorinMinami/res_list/commit/12f7c455eada14b1be5d4e578dad2f1c790e57bd)至[主仓库](https://github.com/KotorinMinami/res_list),部分结果尚未合并 [rest1.csv](https://github.com/l0tk3/PLCT/tree/main/WrokReport/week5/mugen_rest1/res.csv),[rest2](https://github.com/Pagerd/PLCT/blob/main/TestReport/Rest2/rest2.md),[rest0.csv](https://github.com/weilinfox/PLCT-Working/blob/master/Done/Week6/mergeFailed.csv)
## mugen base test结果整理
- 对未测试的测试例进行筛选，选出目前oe-rv仓库中未包含软件的测试例，并生成[nopkg.csv](https://github.com/KotorinMinami/res_list/blob/master/NeedTest/nopkg.csv)
- 并排查出若干测试例为复测可通过测试例，目前最新整理结果如:[commit](https://github.com/KotorinMinami/res_list/commit/12f7c455eada14b1be5d4e578dad2f1c790e57bd)
- 筛选baseOS相关测试例中在x86上成功但在riscv上失败的测试例共190个,[pr](https://gitee.com/yunxiangluo/openeuler-riscv-2303-test/pulls/82/files)

### 部分缺陷

#### smoke-basic-os

- oe_test_rpm_suffix_name
- - dnf list 获取的oetestsuite 软件仓中软件包版本号不带有oe2303的规范
- oe_test_yumgroup_001
- - oe-rv目前软件仓内并没有划分软件包组

#### podman

- oe_test_podman_25
- - 运行docker相关指令时 fatal error: lfstack.push
- oe_test_podman_28
- - 同上
- oe_test_podman_DK_25
- - 同上
- oe_test_podman_DK_28
- - 同上

### mugen测试例问题

#### os-storage

- oe_test_storage_ext3_mount_write
- - 在分盘后使用相应盘块的变量名引用错误
- oe_test_storage_ext4_mount
- - 同上
- oe_test_storage_fileCMD_mkfs
- - 同上

#### smoke-basic-os

- oe_test_rollback
- - mugen 测试代码并没有考虑到git软件包已安装时的情况

### 软件包没有预装

#### spawm-fcgi

- oe_test_service_spawn-fcgi
- - 未安装initscripts

### 软件包不在源中

#### storm

- 测试需要apache-zookeeper软件包，但其并不在源中

### 内核问题

#### smoke-basic-os

- oe_test_ip_rule_01
- - 内核编译时CONFIG_IP_MULTIPLE_TABLES is not set
- oe_test_ip_rule_02
- - 同上
- oe_test_rule_ipv6
- - 同上
- oe_test_iscsi
- - 内核编译时CONFIG_CONFIGFS_FS is not set
- oe_test_iscsid
- - can not create NETLINK_ISCSI socket [Protocol not supported]可能为内核问题
- oe_test_numactl
- - 内核编译时CONFIG_NUMA is not set

### 不属于base test 测试

#### qt5-qttools

- oe_test_qt5-qttools_qdbus-qt5
- - Unable to autolaunch a dbus-daemon without a $DISPLAY for X11，没有使用有gui的镜像，不支持测试
