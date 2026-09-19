# American Circular Challenge: Circular Capture Coach

Build an AI camera assistant that helps someone photograph electronic equipment correctly. Your tool evaluates device photos for problems like blur, poor lighting, bad framing, obstructed labels, and missing required views, then explains what's wrong and tells the user exactly what to re-shoot.

American Circular will provide a dataset built entirely from their own scrap equipment (no customer photos or production data), along with the image format, required photo views, and challenge rules at kickoff. Teams build their own application, AI workflow, and interface from scratch.

Target result: a working web or mobile prototype that evaluates provided device photos and gives immediate, useful retake instructions. A live camera experience is an optional bonus, not required.

## Your prototype

Accept a group of photographs for a device. Let the user specify the intended view of each photo: front, rear/ports or label. Evaluate blur, lighting, framing and label obstruction where relevant, then compare the group with the required-view checklist to find missing views. Automatic view recognition is an optional extension; a view selector is sufficient.

For each photo, show whether it appears usable, needs a retake or needs human review. Explain any issue and suggest an action, such as: “The label is out of focus. Move closer, hold steady and tap the label to focus.” Also identify required views missing from the group.

An existing photo can need a retake without being missing. Keep those two findings distinct. A full group can still contain poor photos.

## What to submit

- A working prototype and a short demonstration of the supplied photos, including both good and poor examples.
- Source code and setup instructions in the format required by the organizers.
- A list of models, libraries and services used, including any accounts, API costs or network requirements.
- A short explanation of what your team built, where AI contributes and known limitations.

No custom model training or physical sorting hardware is required. A clear upload workflow is enough. Follow Bay Hacks' rules on existing tools and work created during the event.

See [Photo guide](PHOTO_GUIDE.md) and [Rules and judging](RULES_AND_JUDGING.md) for the proposed detailed instructions.

**Prize:** $500 cash for the winning team. Named judges and event eligibility are confirmed by the organizers. The prize does not include an internship or paid continuation project.
