"""Desktop speech playback without shell interpretation."""
import logging
import shutil
import subprocess
import tempfile

from TurtleArt.taconstants import VOICES

_logger = logging.getLogger(__name__)


def speak_text(text, language_option=''):
    """Speak text literally, accepting only known legacy voice options.

    Keep the collaboration protocol's '-v voice' representation, but never
    pass arbitrary remote options to espeak. Unknown options use its default
    voice. Return False if synthesis or playback fails.
    """
    synthesizer = shutil.which('espeak') or shutil.which('espeak-ng')
    if synthesizer is None:
        _logger.warning('Speech unavailable: install espeak or espeak-ng '
                        'and ensure it is on PATH.')
        return False
    player = shutil.which('paplay') or shutil.which('aplay')
    if player is None:
        _logger.warning('Speech unavailable: install aplay or paplay '
                        'and ensure it is on PATH.')
        return False
    command = [synthesizer, '--stdin', '--stdout']
    if isinstance(language_option, str):
        parts = language_option.split()
        if (len(parts) == 2 and parts[0] == '-v'
                and parts[1] in VOICES.values()):
            command.extend(['-v', parts[1]])
    try:
        # Spool audio to disk rather than accumulating it in memory.
        with tempfile.TemporaryFile() as audio:
            subprocess.run(command, input=str(text).encode('utf-8'),
                           stdout=audio, shell=False, check=True)
            audio.seek(0)
            subprocess.run([player], stdin=audio, shell=False, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        _logger.warning('Desktop speech playback failed: %s', error)
        return False
    return True
