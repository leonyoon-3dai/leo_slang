// SPDX-License-Identifier: Apache-2.0
//
// Step 01 — UV 좌표 시각화
// "픽셀 위치를 색으로 바꾸는" 가장 기본적인 셰이더.
//
//   화면의 각 픽셀 위치(0~1 범위로 정규화)를
//   그대로 (R, G) 채널에 매핑해서 보여줍니다.
//
//   왼쪽 아래 = 검정,  오른쪽 아래 = 빨강,
//   왼쪽 위   = 초록,  오른쪽 위   = 노랑.

import slangpy;

float3 render(int2 pixel, int2 resolution)
{
    // 픽셀 좌표 → 0~1 정규화 UV
    float2 uv = (float2(pixel) + 0.5f) / float2(resolution);

    // y 축은 위로 갈수록 커지도록 뒤집기.
    uv.y = 1.0f - uv.y;

    return float3(uv.x, uv.y, 0.0f);
}
