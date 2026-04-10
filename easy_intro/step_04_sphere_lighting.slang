// SPDX-License-Identifier: Apache-2.0
//
// Step 04 — 구체에 Lambert 조명
//
// 컴퓨터 그래픽스의 가장 기본 조명 모델인 Lambertian diffuse 를
// 한 픽셀 셰이더 안에서 직접 계산해 봅니다.
//
//   1. 화면 평면에 가상의 구를 하나 놓고
//   2. 픽셀이 구의 표면 위에 있는지 검사한 뒤
//   3. 그 위치의 노멀(normal)과 빛 방향의 내적으로 밝기를 결정.
//
// 레이트레이서 한 줄도 없지만 결과는 "조명이 들어간 구"가 보입니다.

import slangpy;

float3 render(int2 pixel, int2 resolution)
{
    // [-1, 1] 좌표
    float2 p = (float2(pixel) + 0.5f) / float2(resolution) * 2.0f - 1.0f;
    p.y = -p.y;

    float radius = 0.7f;
    float r2 = dot(p, p);

    // 배경 — 위쪽이 살짝 푸른 그라데이션.
    float bg_t = saturate(0.5f - p.y * 0.5f);
    float3 bg = lerp(float3(0.02f, 0.03f, 0.06f),
                     float3(0.10f, 0.15f, 0.25f),
                     bg_t);

    if (r2 > radius * radius)
        return bg;

    // 구의 노멀: (x, y, sqrt(R^2 - x^2 - y^2)) 정규화.
    float z = sqrt(radius * radius - r2);
    float3 normal = normalize(float3(p.x, p.y, z));

    // 고정된 빛 방향.
    float3 light_dir = normalize(float3(0.4f, 0.5f, 0.8f));

    // Lambert : max(0, N · L)
    float ndotl = max(0.0f, dot(normal, light_dir));

    // 살짝의 ambient 더해서 음영부도 보이게.
    float3 base_color = float3(0.85f, 0.35f, 0.45f);
    float3 ambient    = base_color * 0.12f;

    return ambient + base_color * ndotl;
}
