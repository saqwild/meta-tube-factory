# Key Character and Capsule Prompt Compiler

These templates create or repair reference assets. Production scene plates must attach the approved reference images; prose alone cannot guarantee identity.

## Explorer master sheet

```text
Create a neutral 16:9 character reference sheet for CAST-001 Explorer in the Explained From Within visual style. One adult field observer with practical human proportions, orange pressure suit with restrained dark seams, white helmet, dark opaque visor, practical gloves and boots. Show full-body front, three-quarter, side and back views plus seated capsule posture and two restrained observation gestures. Identical suit geometry, helmet shape and stripe placement in every view. Warm Ivory background, even studio light, no environment, no text, no logos, no weapons, no tools, no child proportions, no exposed face, no franchise resemblance.
```

## Capsule master sheet

```text
Create a neutral 16:9 prop reference sheet for PROP-001 exploration capsule. Compact rounded matte-ivory hull, one continuous orange horizontal safety stripe, clear curved canopy, two small cyan navigation lights, two soft white headlamps and one seat sized for the approved Explorer. Show front, side, rear, three-quarter and canopy-open views with identical proportions. Practical seams and landing surfaces, no wings, no weapon, no repair arm, no logo, no text, no environment.
```

## Explorer seated in capsule

```text
Using the approved CAST-001 and PROP-001 images, compose the same Explorer seated inside the same capsule. Preserve exact suit, helmet, visor, hull, canopy, orange stripe and cyan-light geometry. Adult posture, hands resting on practical controls, clear visibility through canopy, neutral studio setting. Do not redesign either subject and do not add another person.
```

## Scene-plate compiler

Append the scene-specific environment and process state to the full style string in `VISUAL_STYLE_CONTRACT.md`, then state:

1. attached approved Explorer/capsule reference paths;
2. exact subject visibility required at frame zero;
3. camera-relative placement and fixed landmark;
4. initial process state before motion;
5. entities explicitly absent;
6. 16:9 composition and negative space needs.

Do not ask the image model to invent the Explorer or capsule from a text description when a reference exists. Do not place the capsule in every microscopic close-up merely for branding.
