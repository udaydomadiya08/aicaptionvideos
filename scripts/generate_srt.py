import pysrt

def segments_to_srt(segments, output_path, max_line_length=80):
    """
    Convert transcribed segments to an SRT file with properly synced timestamps.
    
    Args:
        segments (list): List of dicts with 'start', 'end', 'text'.
        output_path (str): Path to save the output SRT file.
        max_line_length (int): Optional max characters per line for better readability.
    """
    subs = pysrt.SubRipFile()

    for i, seg in enumerate(segments, start=1):
        text = seg['text'].strip()

        # Optionally wrap long lines for readability
        if len(text) > max_line_length:
            lines = []
            while len(text) > max_line_length:
                split_at = text.rfind(' ', 0, max_line_length)
                if split_at == -1:
                    split_at = max_line_length
                lines.append(text[:split_at])
                text = text[split_at:].strip()
            lines.append(text)
            text = '\n'.join(lines)

        subs.append(
            pysrt.SubRipItem(
                index=i,
                start=pysrt.SubRipTime(seconds=seg['start']),
                end=pysrt.SubRipTime(seconds=seg['end']),
                text=text
            )
        )

    subs.save(output_path, encoding='utf-8')
    print(f"✅ SRT saved: {output_path}")
