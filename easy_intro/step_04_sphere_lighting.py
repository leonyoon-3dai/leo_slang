# SPDX-License-Identifier: Apache-2.0
#
# Step 04 — 구체에 Lambert 조명
#
# 실행:  python step_04_sphere_lighting.py
#
# 가장 기본적인 조명(N · L) 한 줄로 "조명이 들어간 구"를 그립니다.

from app import App
import slangpy as spy

WIDTH, HEIGHT = 512, 512

app = App(width=WIDTH, height=HEIGHT, title="Step 04 — 구 + Lambert 조명")
module = spy.Module.load_from_file(app.device, "step_04_sphere_lighting.slang")

while app.process_events():
    output = spy.Tensor.empty(app.device, shape=(HEIGHT, WIDTH), dtype=spy.float3)

    module.render(
        pixel=spy.call_id(),
        resolution=spy.int2(WIDTH, HEIGHT),
        _result=output,
    )

    app.blit(output)
    app.present()
