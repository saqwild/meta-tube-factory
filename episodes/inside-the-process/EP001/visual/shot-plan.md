# EP001 shot plan (04d)

Geometry authority: _context/blocking.json. Both prompt stages (04f,
04f2) project from it and may not re-decide pose, facing, gaze, prop
state, or camera movement. Facing is camera-relative in every clip.
12 clips, 20 s each, 38-42 spoken words per clip (03a PASS).

| Clip | Scene / ENV lock | Cast visible | Camera | Dialogue carrier |
|---|---|---|---|---|
| SC01 | Kitchen counter (ENV001) | YOU | medium wide, slow push in | Control only |
| SC02 | Dough mixed (ENV002) | Explorer | medium, slow dolly in | Explorer + Control |
| SC03 | Gluten net (ENV004) | Explorer | medium close, slight drift | Explorer + Control |
| SC04 | Foam city, first bubbles (ENV004) | Explorer | medium wide, slow dolly in | Explorer + Control |
| SC05 | Foam city inflating (ENV004) | Explorer | wide, slow tilt up | Explorer + Control |
| SC06 | Shaped loaf interior (ENV004) | Explorer | medium, slow push in | Explorer + Control |
| SC07 | Proofing dome (ENV004) | Explorer | medium wide, slight drift | Explorer + Control |
| SC08 | Oven spring (ENV006) | Explorer | wide, slow dolly in | Explorer + Control |
| SC09 | Setting crumb + crust (ENV006) | Explorer | medium close, slow push in | Explorer + Control |
| SC10 | Finished crumb (ENV006) | Explorer | medium, slight drift | Explorer + Control |
| SC11 | Cooling loaf (ENV006) | Explorer | medium, slow dolly out | Explorer + Control |
| SC12 | Sliced loaf (ENV008) | YOU | close-up push in on crumb | Control only |

Continuity: each interior clip opens where the previous clip's
end_state in blocking.json left the Explorer (position, pose, empty
hands, mouth closed). Outside clips (SC01, SC12) carry only the YOU
figure, never the Explorer.
