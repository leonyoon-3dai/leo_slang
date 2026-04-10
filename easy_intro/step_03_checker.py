# SPDX-License-Identifier: Apache-2.0
#
# Step 03 — 체커보드 패턴
#
# 실행:  python step_03_checker.py
#
# 절차적(procedural) 패턴: 텍스처 한 장 없이 GPU 함수만으로 그립니다.

from app import App
import slangpy as spy

WIDTH, HEIGHT = 512, 512

app = App(width=WIDTH, height=HEIGHT, title="Step 03 — 체커보드")
module = spy.Module.load_from_file(app.device, "step_03_checker.slang")

while app.process_events():
    output = spy.Tensor.empty(app.device, shape=(HEIGHT, WIDTH), dtype=spy.float3)

    module.render(
        pixel=spy.call_id(),
        resolution=spy.int2(WIDTH, HEIGHT),
        _result=output,
    )

    app.blit(output)
    app.present()
