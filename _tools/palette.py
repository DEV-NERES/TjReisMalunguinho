import colorsys
from collections import Counter
from PIL import Image

img = Image.open(r"C:\Users\NERES\Documents\deepseek-harness\default-workspace\tenda-jurema\assets\logo.jpg").convert("RGB")
# amostra o circulo central (ignora o fundo preto dos cantos)
w, h = img.size
px = img.load()
samples = []
cx, cy, r = w / 2, h / 2, w * 0.46
for y in range(0, h, 2):
    for x in range(0, w, 2):
        if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
            samples.append(px[x, y])

print("amostras:", len(samples))


def q(c, step=16):
    return tuple(min(255, (v // step) * step + step // 2) for v in c)


buckets = Counter(q(c) for c in samples)

print("\n== Top 24 cores quantizadas (hex | rgb | %) ==")
for c, n in buckets.most_common(24):
    hx = "#%02X%02X%02X" % c
    hh, ss, vv = colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
    print(f"{hx}  rgb{c}  {100*n/len(samples):5.2f}%  H={hh*360:5.0f} S={ss*100:3.0f} V={vv*100:3.0f}")


def family(name, pred):
    sel = [c for c in samples if pred(*colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255))]
    if not sel:
        print(f"\n{name}: nenhuma")
        return
    avg = tuple(sum(c[i] for c in sel) // len(sel) for i in range(3))
    print(f"\n{name}: n={len(sel)} ({100*len(sel)/len(samples):.1f}%)  media=#{avg[0]:02X}{avg[1]:02X}{avg[2]:02X}")
    for c, n in Counter(q(c, 24) for c in sel).most_common(5):
        print("   #%02X%02X%02X  %5.2f%%" % (c[0], c[1], c[2], 100 * n / len(sel)))


print("\n== Familias ==")
family("DOURADO/BRONZE (amarelo, saturado, claro)", lambda h, s, v: 0.09 <= h <= 0.16 and s > 0.40 and v > 0.45)
family("VERDE FOLHA", lambda h, s, v: 0.20 <= h <= 0.42 and s > 0.20 and v > 0.15)
family("MARROM/TERRA", lambda h, s, v: 0.03 <= h <= 0.12 and 0.20 < v <= 0.62)
family("ESCURO/SOMBRA (fundo)", lambda h, s, v: v <= 0.22)
family("CLARO/AREIA (realces)", lambda h, s, v: v >= 0.72)
