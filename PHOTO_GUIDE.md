# Photo guide

Student package with real equipment images and populated CSV files, reviewed internally for organizer handoff. Confirm detailed event logistics with the organizers before kickoff.

## Three required views per device

| View | What should be visible | What counts as a usable photo |
| --- | --- | --- |
| front | The front of the device, including its outer edges | Device fits in the image; relevant details can be seen |
| rear_ports | The rear or connection side, including the port area | Relevant side and connectors are visible; device is not unintentionally cut off |
| label | The temporary DEMO label attached for the challenge | Complete label is readable and unobstructed |

A label close-up does not need to show the whole device. Judge framing against the intended view. Devices may have different shapes or connector layouts; examples in the release will illustrate the selected equipment.

## Quality checks

| Issue code | Meaning | Example guidance |
| --- | --- | --- |
| blur | Motion or focus makes the required detail unreadable or unclear | Hold steady and refocus on the device or label |
| underexposed | The relevant area is too dark to inspect | Add light or move to a brighter position |
| glare_or_overexposed | Reflections or excessive brightness hide required detail | Change the camera angle or move the light |
| framing | Required content is unintentionally outside the image | Step back or reposition to include the full required area |
| label_obstructed | Part of the challenge label is covered | Remove the obstruction and photograph the complete label |

Lighting has two issue codes so the retake instruction can be specific. A photo can have several issues. A dark background is not automatically a defect if the required subject is clear. A covered real serial number is intentional privacy masking and is not the challenge label; evaluate only the temporary DEMO label.

Use `usable` for photos adequate for the intended view, `retake` for clear failures, and `needs_review` when you cannot reliably decide. Explain uncertainty. Do not mark every photo uncertain to avoid evaluating it.

## Missing views

Evaluate each photo set separately. A set contains a device ID and image IDs with their intended views. If no image is supplied for a required view, report it as missing. If the front photo exists but is blurry, report a front photo requiring a retake, not an absent front photo.

Treat supplied view names as the intended views, not proof the image actually shows that view. If the content and the selected view disagree, explain that mismatch for human review. Automatic classification of device identity is outside this challenge.

## Files in the completed participant package

```text
CHALLENGE.md
PHOTO_GUIDE.md
RULES_AND_JUDGING.md
images/
manifest.csv
photo_sets.csv
practice_labels.csv
practice_set_labels.csv
```

Images are upright JPEG or PNG files with neutral names and metadata stripped. PNG is used for redacted images to preserve every decoded pixel outside the black privacy boxes. Black boxes hide original identifiers or personal names: ignore them when evaluating capture quality. Evaluate obstruction of the orange DEMO label, not these privacy masks. No installation is needed to open the photos and CSV files. Each physical device stays entirely in practice or in the judges' separate evaluation set.

### Column definitions

`manifest.csv`: `image_id,device_id,relative_path,sha256`

- `image_id`: unique neutral identifier, such as IMG-0001.
- `device_id`: fictional grouping identifier, such as DEV-001.
- `relative_path`: image location inside the package.
- `sha256`: checksum used to verify the downloaded bytes.

`photo_sets.csv`: `set_id,device_id,image_id,intended_view`

Each row assigns an image to a set and its intended view. A set can contain multiple photos for a view. Different sets can reuse an image, but every set belongs to a single device. Missing-view scenarios omit a view from that set; they need not remove the image from the entire practice library.

`practice_labels.csv`: `image_id,observed_view,status,issue_codes,reason,retake_guidance`

Issue codes are separated by semicolons. An empty issue cell with `usable` means no labeled quality problem. `observed_view` can be `front`, `rear_ports`, `label` or `uncertain`. These practice answers explain examples; they are not additional inputs your tool should require for evaluation.

`practice_set_labels.csv`: `set_id,missing_views,reason`

Missing view names are separated by semicolons. An empty cell means the set contains all three intended views. Judge answers will be kept separate from the evaluation inputs.

## Use in your prototype

Import the photo-set membership, or let a person upload its images and select intended views. Offer both per-photo feedback and a set-level checklist. You may choose your own internal data format and interface; matching the label CSV schema is not required for your output.

## Existing-photo dataset boundaries

Not every device folder has every reference view or quality defect. Missing views are intentional evaluation opportunities, not missing downloads. Use each photo set as supplied. A full library contains alternate captures, not a claim of three usable reference views for every device. Redacted areas are excluded from sharpness, exposure and OCR assessment; never attempt to recover masked text.
