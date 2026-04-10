// SPDX-License-Identifier: Apache-2.0
//
// Step 02 — SDF 로 원 그리기
//
// SDF (Signed Distance Field) = 어떤 점에서 도형의 표면까지의
// "부호 있는 거리". 음수면 도형 안쪽, 0이면 표면, 양수면 바깥쪽.
//
//   원의 SDF: d(p) = length(p - center) - radius
//
// 이 한 줄로 어떤 해상도에서도 매끄러운 원을 그릴 수 있다는 것이
// 셰이더 그래픽스의 매력입니다.

import slangpy;

float sdf_circle(float2 p, float2 center, float radius)
{
    return length(p - center) - radius;
}

float3 render(int2 pixel, int2 resolution)
{
    // [-1, 1] 범위로 좌표 정규화 (정사각형 가정).
    float2 p = (float2(pixel) + 0.5f) / float2(resolution) * 2.0f - 1.0f;
    p.y = -p.y;

    float d = sdf_circle(p, float2(0.0f, 0.0f), 0.5f);

    // 거리에 따라 부드러운 안티에일리어싱.
    float aa = 1.5f / float(resolution.x);
    float inside = smoothstep(aa, -aa, d);

    float3 bg     = float3(0.05f, 0.07f, 0.10f);   // 어두운 배경
    float3 circle = float3(1.00f, 0.55f, 0.20f);   // 주황색 원

    return lerp(bg, circle, inside);
}
