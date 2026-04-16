// SPDX-License-Identifier: Apache-2.0
//
// Step 03 — 체커보드 패턴
//
// "좌표를 격자로 자른 뒤, 짝/홀수 칸을 다른 색으로 칠한다"는
// 그래픽스의 가장 고전적인 절차적(procedural) 텍스처 예제입니다.
//
// 텍스처 이미지를 한 장도 사용하지 않고 GPU 가 매 픽셀마다
// 이 함수를 평가해서 무한 해상도의 패턴을 만들어 줍니다.

import slangpy;

float3 render(int2 pixel, int2 resolution)
{
    // [-1, 1] 좌표
    float2 p = (float2(pixel) + 0.5f) / float2(resolution) * 2.0f - 1.0f;

    // 8 칸짜리 격자.
    float2 cell = floor(p * 8.0f);
    // HLSL/Slang fmod 는 피제수(dividend) 부호를 따르므로
    // cell 합이 음수이면 -1 이 나올 수 있다. abs 로 항상 [0, 1] 로 맞춘다.
    float checker = abs(fmod(cell.x + cell.y, 2.0f));

    float3 a = float3(0.92f, 0.92f, 0.92f);
    float3 b = float3(0.15f, 0.20f, 0.30f);

    return lerp(a, b, checker);
}
