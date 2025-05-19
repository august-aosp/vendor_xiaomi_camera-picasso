#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import os
from extract_utils.file import File
from extract_utils.fixups_blob import (
    BlobFixupCtx,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.tools import (
    apktool_path,
    java_path,
)
from extract_utils.utils import run_cmd

def apktool_pack(input_dir: str, apk_path: str) -> None:
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory {input_dir} does not exist.")
    if os.path.exists(apk_path):
        os.remove(apk_path)

    print(f"Packing {input_dir} to {apk_path} using apktool...")
    run_cmd(
        [
            java_path,
            '-jar',
            apktool_path,
            'b',
            input_dir,
            '-o',
            apk_path,
        ],
    )

blob_fixups: blob_fixups_user_type = {
    'system/lib64/libcamera_algoup_jni.xiaomi.so': blob_fixup()
        .add_needed('libgui_shim_miuicamera.so')
        .sig_replace('08 AD 40 F9', '08 A9 40 F9'),
    'system/lib64/libcamera_mianode_jni.xiaomi.so': blob_fixup()
        .add_needed('libgui_shim_miuicamera.so'),
    'system/lib64/libmicampostproc_client.so': blob_fixup()
        .remove_needed('libhidltransport.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    "common",
    "xiaomi/camera",
    blob_fixups=blob_fixups,
    device_rel_path="vendor/xiaomi/camera",
    check_elf=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
    apktool_pack(
        input_dir="../../../MiuiCamera-smali",
        apk_path="common/proprietary/system/priv-app/MiuiCamera/MiuiCamera.apk",
    )
