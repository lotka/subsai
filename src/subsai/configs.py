#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configurations file
"""

from ffsubsync.constants import DEFAULT_MAX_SUBTITLE_SECONDS, DEFAULT_START_SECONDS, DEFAULT_MAX_OFFSET_SECONDS, \
    DEFAULT_APPLY_OFFSET_SECONDS, DEFAULT_FRAME_RATE, DEFAULT_VAD

from subsai.models.whisper_api_model import WhisperAPIModel

AVAILABLE_MODELS = {
    'API/openai/whisper': {
        'class': WhisperAPIModel,
        'description': 'API for the OpenAI large-v2 Whisper model, requires an API key.',
        'url': 'https://platform.openai.com/docs/guides/speech-to-text',
        'config_schema': WhisperAPIModel.config_schema,
    }
}

BASIC_TOOLS_CONFIGS = {
    'set time': {
        'description': 'Set time to a subtitle',
        'config_schema': {
            'h': {
                'type': float,
                'description': "hours: Integer or float values, may be positive or negative",
                'options': None,
                'default': 0,
            },
            'm': {
                'type': float,
                'description': "minutes: Integer or float values, may be positive or negative",
                'options': None,
                'default': 0,
            },
            's': {
                'type': float,
                'description': "seconds: Integer or float values, may be positive or negative",
                'options': None,
                'default': 0,
            },
            'ms': {
                'type': float,
                'description': "milliseconds: Integer or float values, may be positive or negative",
                'options': None,
                'default': 0,
            }
        }
    },
    'shift': {
        'description': 'Shift all subtitles by constant time amount',
        'config_schema': {
            'h': {
                'type': float,
                'description': "hours: Integer or float values, may be positive or negative",
                'options': None,
                'default': 0,
            },
            'm': {
                'type': float,
                'description': "minutes: Integer or float values, may be positive or negative",
                'options': None,
                'default': 0,
            },
            's': {
                'type': float,
                'description': "seconds: Integer or float values, may be positive or negative",
                'options': None,
                'default': 0,
            },
            'ms': {
                'type': float,
                'description': "milliseconds: Integer or float values, may be positive or negative",
                'options': None,
                'default': 0,
            },
            'frames': {
                'type': int,
                'description': "When specified, must be an integer number of frames",
                'options': None,
                'default': None,
            },
            'fps': {
                'type': float,
                'description': "When specified, must be a positive number.",
                'options': None,
                'default': None,
            }

        }
    },
}

ADVANCED_TOOLS_CONFIGS = {
    'ffsubsync': {
        'description': 'Language-agnostic automatic synchronization of subtitles with video, so that subtitles are '
                       'aligned to the correct starting point within the video.',
        'url': 'https://github.com/smacke/ffsubsync',
        'config_schema': {
            'vad': {
                'type': list,
                'description': "Which voice activity detector to use for speech extraction "
                               "(if using video / audio as a reference",
                'options': [
                    "subs_then_webrtc",
                    "webrtc",
                    "subs_then_auditok",
                    "auditok",
                    "subs_then_silero",
                    "silero",
                ],
                'default': DEFAULT_VAD,
            },
            'max-subtitle-seconds': {
                'type': float,
                'description': 'Maximum duration for a subtitle to appear on-screen',
                'options': None,
                'default': DEFAULT_MAX_SUBTITLE_SECONDS,
            },
            'start-seconds': {
                'type': int,
                'description': 'Start time for processing',
                'options': None,
                'default': DEFAULT_START_SECONDS,
            },
            'max-offset-seconds': {
                'type': float,
                'description': 'The max allowed offset seconds for any subtitle segment',
                'options': None,
                'default': DEFAULT_MAX_OFFSET_SECONDS,
            },
            'apply-offset-seconds': {
                'type': float,
                'description': 'Apply a predefined offset in seconds to all subtitle segments',
                'options': None,
                'default': DEFAULT_APPLY_OFFSET_SECONDS,
            },
            'suppress-output-if-offset-less-than': {
                'type': float,
                'description': 'Apply a predefined offset in seconds to all subtitle segments',
                'options': None,
                'default': None,
            },
            'frame-rate': {
                'type': int,
                'description': 'Frame rate for audio extraction',
                'options': None,
                'default': DEFAULT_FRAME_RATE,
            },
            'output-encoding': {
                'type': str,
                'description': "What encoding to use for writing output subtitles "
                               '(default=utf-8). Can indicate "same" to use same '
                               "encoding as that of the input.",
                'options': None,
                'default': "utf-8",
            },
            'skip-infer-framerate-ratio': {
                'type': bool,
                'description': 'If set, do not try to infer framerate ratio based on duration ratio.',
                'options': None,
                'default': False,
            },
            'no-fix-framerate': {
                'type': bool,
                'description': 'If specified, subsync will not attempt to correct a framerate',
                'options': None,
                'default': False,
            },
            'serialize-speech': {
                'type': bool,
                'description': 'If specified, serialize reference speech to a numpy array.',
                'options': None,
                'default': False,
            },
            'gss': {
                'type': bool,
                'description': "If specified, use golden-section search to try to find"
                               "the optimal framerate ratio between video and subtitles.",
                'options': None,
                'default': False,
            }
        }
    },
}
