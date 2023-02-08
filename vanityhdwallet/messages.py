PROGRESS_MESSAGE_LINES = [
    " · Tries: {}\n",
    " · Estimated tries (50% probability): {}\n",
    " · Time elapsed: {:.2f} s\n",
    " · Estimated time (50% probability): {:.2f} s",
]
PROGRESS_MESSAGE = f"\x1B[{len(PROGRESS_MESSAGE_LINES)}A" + "".join(
    PROGRESS_MESSAGE_LINES
)

GENERATING_MESSAGE = "Generating vanity wallet" + "\n" * len(PROGRESS_MESSAGE_LINES)

ADDRESS_GENERATED_MESSAGE = "{} vanity address generated!\n{}\n{}"
