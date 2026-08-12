#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove_arch_suffix,
    lib_fixup_vendorcompat,
    lib_fixups_user_type,
    libs_clang_rt_ubsan,
    libs_proto_3_9_1,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/samsung/a54x-common',
    'hardware/samsung',
    'hardware/samsung_slsi-linaro/exynos',
    'hardware/samsung_slsi-linaro/graphics',
    'hardware/samsung_slsi-linaro/interfaces',
    'vendor/samsung/a54x-common',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    libs_proto_3_9_1: lib_fixup_vendorcompat,
    libs_clang_rt_ubsan: lib_fixup_remove_arch_suffix,
    'libuuid': lib_fixup_vendor_suffix,
} # fmt: skip

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/bin/hw/android.hardware.security.keymint-service.samsung',
        'vendor/lib64/libskeymint10device.so',
        'vendor/lib64/libskeymint_cli.so',
    ): blob_fixup()
        .replace_needed('android.hardware.security.keymint-V1-ndk_platform.so',
            'android.hardware.security.keymint-V1-ndk.so')
        .replace_needed('android.hardware.security.secureclock-V1-ndk_platform.so',
            'android.hardware.security.secureclock-V1-ndk.so')
        .replace_needed('android.hardware.security.sharedsecret-V1-ndk_platform.so',
             'android.hardware.security.sharedsecret-V1-ndk.so')
        .add_needed('libshim_crypto.so')
        .add_needed('libshim_keymint.so'),
    'vendor/lib64/libskeymint10device.so': blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
    'vendor/lib64/libwvaidl.so': blob_fixup()
        .add_needed('libshim_binder_ndk.so'),
    (
        'vendor/lib64/ese_spi_nxp.so',
        'vendor/lib64/nfc_nci_nxpsn.so',
    ): blob_fixup()
        .add_needed('libshim_base.so'),
    (
        'vendor/lib64/libaudioparamupdate.so',
        'vendor/lib64/libaboxpcmdump.so',
    ): blob_fixup()
        .replace_needed('libaudioroute.so', 'libaudioroute_samsung.so'),
    'vendor/etc/init/android.hardware.security.keymint-service.samsung.rc': blob_fixup()
        .regex_replace(
            'android\\.hardware\\.security\\.keymint-service\n',
            'android.hardware.security.keymint-service.samsung\n'),
    'vendor/etc/init/nxp.android.hardware.nfc@1.2-service.rc': blob_fixup()
        .regex_replace(
            'interface vendor\\.samsung\\.hardware\\.nfc@2\\.0::ISehNfc default\n',
            ''),
    'vendor/etc/init/vendor.samsung.hardware.camera.provider-service_64.rc': blob_fixup()
        .regex_replace('vendor_secdir w', 'w')
        .regex_replace('vendor_secdir', 'camera'),
    'vendor/lib64/libsensorlistener.so': blob_fixup()
        .add_needed('libshim_sensorndkbridge.so'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .replace_needed('libprotobuf-cpp-lite-3.9.1.so', 'libprotobuf-cpp-full-3.9.1.so'),
    'vendor/lib64/libenn_user_driver_gpu_lib.so': blob_fixup()
        .replace_needed('libOpenCL.so', 'libGLES_mali.so'),
    (
        'vendor/lib64/sensors.grip.so',
        'vendor/lib64/sensors.inputvirtual.so',
        'vendor/lib64/sensors.sensorhub.so',
    ): blob_fixup()
        .remove_needed('libhidltransport.so')
        .add_needed('libutils-v32.so')
        .binary_regex_replace(b'_ZN7android6Thread3runEPKcim', b'_ZN7utils326Thread3runEPKcim'),
}  # fmt: skip

module = ExtractUtilsModule(
    'a54x-common',
    'samsung',
    namespace_imports=namespace_imports,
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
