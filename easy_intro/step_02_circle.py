# SPDX-License-Identifier: Apache-2.0
#
# Step 02 — SDF 로 원 그리기
#
# 실행:  python step_02_circle.py
#
# 거리 함수(SDF) 한 줄로 매끄러운 원을 렌더링합니다.

from app import App
import slangpy as spy

WIDTH, HEIGHT = 512, 512

app = App(width=WIDTH, height=HEIGHT, title="Step 02 — SDF 원")
module = spy.Module.load_from_file(app.device, "step_02_circle.slang")

while app.process_events():
    output = spy.Tensor.empty(app.device, shape=(HEIGHT, WIDTH), dtype=spy.float3)

    module.render(
        pixel=spy.call_id(),
        resolution=spy.int2(WIDTH, HEIGHT),
        _result=output,
    )

    app.blit(output)
    app.present()
