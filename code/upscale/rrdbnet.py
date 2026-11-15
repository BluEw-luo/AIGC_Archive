"""Minimal RealESRGAN RRDBNet (x4plus) implementation for standalone frame upscaling."""
import torch
import torch.nn as nn
import torch.nn.functional as F


class ResidualDenseBlock(nn.Module):
    def __init__(self, num_feat=64, num_grow_ch=32):
        super().__init__()
        self.conv1 = nn.Conv2d(num_feat, num_grow_ch, 3, 1, 1)
        self.conv2 = nn.Conv2d(num_feat + num_grow_ch, num_grow_ch, 3, 1, 1)
        self.conv3 = nn.Conv2d(num_feat + 2 * num_grow_ch, num_grow_ch, 3, 1, 1)
        self.conv4 = nn.Conv2d(num_feat + 3 * num_grow_ch, num_grow_ch, 3, 1, 1)
        self.conv5 = nn.Conv2d(num_feat + 4 * num_grow_ch, num_feat, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, inplace=True)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        return x5 * 0.2 + x


class RRDB(nn.Module):
    def __init__(self, num_feat, num_grow_ch=32):
        super().__init__()
        self.rdb1 = ResidualDenseBlock(num_feat, num_grow_ch)
        self.rdb2 = ResidualDenseBlock(num_feat, num_grow_ch)
        self.rdb3 = ResidualDenseBlock(num_feat, num_grow_ch)

    def forward(self, x):
        out = self.rdb1(x)
        out = self.rdb2(out)
        out = self.rdb3(out)
        return out * 0.2 + x


class RRDBNet(nn.Module):
    def __init__(self, num_in_ch=3, num_out_ch=3, scale=4, num_feat=64, num_block=23, num_grow_ch=32):
        super().__init__()
        self.scale = scale
        self.conv_first = nn.Conv2d(num_in_ch, num_feat, 3, 1, 1)
        self.body = nn.Sequential(*[RRDB(num_feat, num_grow_ch) for _ in range(num_block)])
        self.conv_body = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_up1 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_up2 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_hr = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
        self.conv_last = nn.Conv2d(num_feat, num_out_ch, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, inplace=True)

    def forward(self, x):
        feat = self.conv_first(x)
        feat = feat + self.conv_body(self.body(feat))
        feat = self.lrelu(self.conv_up1(F.interpolate(feat, scale_factor=2, mode='nearest')))
        feat = self.lrelu(self.conv_up2(F.interpolate(feat, scale_factor=2, mode='nearest')))
        return self.conv_last(self.lrelu(self.conv_hr(feat)))


def load_model(path, device='cuda', half=True):
    sd = torch.load(path, map_location='cpu', weights_only=True)
    sd = sd.get('params_ema', sd.get('params', sd))
    model = RRDBNet()
    model.load_state_dict(sd, strict=True)
    model.eval().to(device)
    if half:
        model.half()
    for p in model.parameters():
        p.requires_grad_(False)
    return model


@torch.inference_mode()
def enhance(model, img, tile=0, tile_pad=16):
    """img: (1,3,H,W) tensor in [0,1] matching model device/dtype. Returns (1,3,4H,4W) in [0,1]."""
    scale = model.scale
    _, _, h, w = img.shape
    pad_h = (scale - h % scale) % scale
    pad_w = (scale - w % scale) % scale
    if pad_h or pad_w:
        img = F.pad(img, (0, pad_w, 0, pad_h), 'reflect')

    if not tile:
        out = model(img)
    else:
        _, _, H, W = img.shape
        out = img.new_zeros((1, 3, H * scale, W * scale))
        for y in range(0, H, tile):
            for x in range(0, W, tile):
                x0, x1 = x, min(x + tile, W)
                y0, y1 = y, min(y + tile, H)
                xp0, xp1 = max(x0 - tile_pad, 0), min(x1 + tile_pad, W)
                yp0, yp1 = max(y0 - tile_pad, 0), min(y1 + tile_pad, H)
                t = model(img[:, :, yp0:yp1, xp0:xp1])
                ox0 = (x0 - xp0) * scale
                oy0 = (y0 - yp0) * scale
                out[:, :, y0 * scale:y1 * scale, x0 * scale:x1 * scale] = \
                    t[:, :, oy0:oy0 + (y1 - y0) * scale, ox0:ox0 + (x1 - x0) * scale]
    out = out[:, :, :h * scale, :w * scale]
    return out.clamp_(0, 1)
