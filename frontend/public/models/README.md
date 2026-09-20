# Fitness trainer model contract

Place one licensed, rigged female fitness trainer GLB at:

`/public/models/fitness-trainer.glb`

The model must contain a full-body humanoid armature, PBR materials, an `Idle`
clip, and the exercise clips listed in
`src/data/exercise-animations.ts`. Clip matching is case-insensitive and also
supports the documented aliases.

For the best browser experience, export a compressed GLB with a complete body
in its bind pose, modest professional sportswear, 2K-or-smaller textures, and
loop-ready clips. Each repetition-based clip must begin and end in its natural
start position; timed clips should be a stable loop. The avatar renderer uses
cross-fading for clip changes, so retain one consistent skeleton across all
animations.

The project intentionally does not use a still image as an avatar fallback:
a static image cannot be a truthful exercise demonstration.
