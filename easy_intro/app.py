# SPDX-License-Identifier: Apache-2.0
#
# 가장 단순한 slangpy 윈도우/디바이스/스왑체인 래퍼.
# mipmap/app.py 의 축약 버전입니다 — 이 폴더에서만 동작하도록 자체 포함.

from typing import Callable, Optional
import slangpy as spy
from pathlib import Path


class App:
    def __init__(
        self,
        title: str = "easy_intro",
        width: int = 512,
        height: int = 512,
        device_type: spy.DeviceType = spy.DeviceType.automatic,
    ):
        self._window = spy.Window(width=width, height=height, title=title, resizable=False)

        self._device = spy.create_device(
            device_type,
            enable_debug_layers=False,
            include_paths=[Path(__file__).parent],
        )

        # 결과 텐서를 화면에 그리는 헬퍼 셰이더 모듈.
        self._module = spy.Module.load_from_file(self._device, "app.slang")

        self.surface = self._device.create_surface(self._window)
        self.surface.configure(width=self._window.width, height=self._window.height)

        self._output_texture: "spy.Texture" = self._device.create_texture(
            format=spy.Format.rgba16_float,
            width=width,
            height=height,
            mip_count=1,
            usage=spy.TextureUsage.shader_resource | spy.TextureUsage.unordered_access,
            label="output_texture",
        )

        self._mouse_pos = spy.float2()
        self._window.on_keyboard_event = self._on_window_keyboard_event
        self._window.on_mouse_event = self._on_window_mouse_event
        self._window.on_resize = self._on_window_resize

        self.on_keyboard_event: Optional[Callable[[spy.KeyboardEvent], None]] = None
        self.on_mouse_event: Optional[Callable[[spy.MouseEvent], None]] = None

    @property
    def device(self) -> spy.Device:
        return self._device

    @property
    def window(self) -> spy.Window:
        return self._window

    @property
    def mouse_pos(self) -> spy.float2:
        return self._mouse_pos

    @property
    def output(self) -> spy.Texture:
        return self._output_texture

    def process_events(self) -> bool:
        if self._window.should_close():
            return False
        self._window.process_events()
        return True

    def present(self) -> None:
        if not self.surface.config:
            return
        image = self.surface.acquire_next_image()
        if not image:
            return

        if (
            self._output_texture is None
            or self._output_texture.width != image.width
            or self._output_texture.height != image.height
        ):
            self._output_texture = self._device.create_texture(
                format=spy.Format.rgba16_float,
                width=image.width,
                height=image.height,
                mip_count=1,
                usage=spy.TextureUsage.shader_resource | spy.TextureUsage.unordered_access,
                label="output_texture",
            )

        command_encoder = self._device.create_command_encoder()
        command_encoder.blit(image, self._output_texture)
        command_encoder.set_texture_state(image, spy.ResourceState.present)
        self._device.submit_command_buffer(command_encoder.finish())

        del image
        self.surface.present()

    def blit(self, source: spy.Tensor) -> None:
        """결과 Tensor(float3, 2) 를 출력 텍스처에 복사."""
        if len(source.shape) != 2:
            raise ValueError("Source tensor must be 2D (height, width).")
        size = spy.int2(source.shape[1], source.shape[0])
        self._module.blit(spy.grid((size.y, size.x)), size, source, self.output)

    def _on_window_keyboard_event(self, event: spy.KeyboardEvent) -> None:
        if event.type == spy.KeyboardEventType.key_press:
            if event.key == spy.KeyCode.escape:
                self._window.close()
                return
        if self.on_keyboard_event:
            self.on_keyboard_event(event)

    def _on_window_mouse_event(self, event: spy.MouseEvent) -> None:
        if event.type == spy.MouseEventType.move:
            self._mouse_pos = event.pos
        if self.on_mouse_event:
            self.on_mouse_event(event)

    def _on_window_resize(self, width: int, height: int) -> None:
        self._device.wait()
        if width > 0 and height > 0:
            self.surface.configure(width=width, height=height)
        else:
            self.surface.unconfigure()
