# SPDX-License-Identifier: Apache-2.0
#
# Step 01 — UV 좌표 시각화
#
# 실행:  python step_01_uv.py
#
# 화면의 각 픽셀 위치(0~1)를 그대로 (R, G) 색으로 보여줍니다.
# 가장 단순한 "픽셀 셰이더 한 줄" 예제입니다.

from app import App
import slangpy as spy

WIDTH, HEIGHT = 512, 512

app = App(width=WIDTH, height=HEIGHT, title="Step 01 — UV 좌표")
module = spy.Module.load_from_file(app.device, "step_01_uv.slang")

while app.process_events():
    output = spy.Tensor.empty(app.device, shape=(HEIGHT, WIDTH), dtype=spy.float3)

    module.render(
        pixel=spy.call_id(),
        resolution=spy.int2(WIDTH, HEIGHT),
        _result=output,
    )

    app.blit(output)
    app.present()
