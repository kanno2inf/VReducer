#!/usr/bin/env python
from typing import List


def startswith(start_match: str, targets: List[str]) -> bool:
    # リスト内要素のstartswith
    for e in targets:
        if e.startswith(start_match):
            return True
    return False


def contains(start_match: str, targets: List[str]) -> bool:
    # リスト内要素のstartswith
    for e in targets:
        if start_match in e:
            return True
    return False


def get_cloth_place(gltf: dict) -> dict:
    """
    服のテクスチャの配置を決める
    :param gltf: glTFオブジェクト(VRM拡張を含む)
    :return: 配置座標と配置サイズ
    """
    material_names = [material['name'] for material in gltf['materials']]
    has_tops = contains('_Tops_', material_names)
    has_accessory = contains('_AccessoryNeck_', material_names)
    has_shoes = contains('_Shoes_', material_names)
    has_bottom = contains('_Bottoms_', material_names)
    is_skirt = startswith('F00_001_01_Bottoms_', material_names)

    place = {}
    main = None  # 結合先マテリアル
    ox, oy = 0, 0  # オフセット
    if has_tops:
        main = '_Tops_'
        place['_Tops_'] = {'pos': (0, 0), 'size': (2048, 2048)}
        if has_accessory or has_shoes or has_bottom:
            place['_Tops_']['size'] = (1024, 1024)
        ox, oy = (1024, 1024)

    if has_bottom:
        main = main or '_Bottoms_'
        place['_Bottoms_'] = {'pos': (0, oy), 'size': (1024, 1024)}
        if is_skirt:
            place['_Bottoms_']['size'] = (1024, 512)
        ox = 1024

    oy = 0
    if has_shoes:
        main = main or '_Shoes_'
        place['_Shoes_'] = {'pos': (ox, 0), 'size': (512, 512)}
        oy = 512

    if has_accessory:
        main = main or '_AccessoryNeck_'
        place['_AccessoryNeck_'] = {'pos': (ox, oy), 'size': (256, 256)}

    if not main:
        return {}  # 素体の場合

    return {'main': main, 'place': place}