// SPDX-License-Identifier: Apache-2.0
//
// 출력 텐서를 윈도우 텍스처에 복사하는 가장 단순한 blit 셰이더.

import slangpy;

void blit(
    int2 pixel,
    int2 size,
    Tensor<float3, 2> input,
    RWTexture2D<float4> output)
{
    float3 col = input.getv(uint2(pixel));
    // sRGB 톤매핑 없이 그대로 출력 (saturate 만 적용해서 안전).
    col = saturate(col);
    output[pixel] = float4(col, 1.0f);
}
